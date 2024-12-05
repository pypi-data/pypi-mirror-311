from google.cloud import bigquery
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import datetime
import colorsys
import traceback
import random

# Initialize BigQuery client
client = bigquery.Client(project="team-begamob")

#get list project_id for first_filter
def get_projects_for_user(client, user_id):
    query = f"""
    SELECT DISTINCT projectId 
    FROM `team-begamob.AllProjects_IAA_Detail.email_config`
    WHERE email = "{user_id}@ikameglobal.com"
    ORDER BY projectId
    """
    try:
        query_job = client.query(query)
        results = query_job.result()
        project_ids = [row.projectId for row in results]
        return project_ids
    except Exception as error:
        return {"error": str(error)}

def date_filter(var, start_date, end_date):
    conditions = []
    if start_date is not None and start_date != '':
        conditions.append(f"{var} >= '{start_date}'")
    if end_date is not None and end_date != '':
        conditions.append(f"{var} <= '{end_date}'")
    if conditions:
        return "        and " + " and ".join(conditions)
    else:
        return "        "

def gbq_str_filter(var, filter):
    if filter is None or filter == '':
        return "        "
    else:
        filter_list = filter.split(", ")
        transformed_list = [f"'{item.strip()}'" for item in filter_list]
        transformed_filter = ", ".join(transformed_list)
        return f"""        and {var} in ( {str(transformed_filter)} )"""

def gbq_int_filter(var, filter):
    if filter is None or filter == '':
        return "        "
    operators = ['>=', '<=', '=', '<', '>', 'between']
    filter = filter.strip().lower()
    if filter.startswith('between'):
        values = filter[7:].split('and')
        if len(values) == 2:
            start, end = values[0].strip(), values[1].strip()
            return f"        and {var} between {start} and {end}"
        else:
            return '        '
    for op in operators:
        if filter.startswith(op):
            value = filter[len(op):].strip()
            if op == '=' and ',' in value:
                values = [v.strip() for v in value.split(',')]
                return f"        and {var} in ({', '.join(values)})"
            return f"        and {var} {op} {value}"
    values = [v.strip() for v in filter.split(',')]
    return f"        and {var} in ({', '.join(values)})"

def dimension_select(type):
    if type == 'data_souce':
        return ['start_date', 'end_date', 'country']
    elif type == 'event':
        return ['install_start_date', 'install_end_date', 'version', 'number_day_install']
    elif type == 'user_source':
        return ['traffic_source_medium', 'traffic_source_name']
    elif type == 'to_discover':
        return ['country', 'version', 'traffic_source_medium', 'traffic_source_name']

def gbq_filter_return(data_dict, keys= None):
    if keys is None or not keys:
        keys = data_dict.keys()
    result = []
    for key in keys:
        value = data_dict.get(key, '')
        if value: 
            result.append(value)  
    return '\n'.join(result)

def gbq_list_dimension_discover_query(client, project_id, dict_source_filter, dim):
    if dim in dimension_select(type= 'user_source'):
        query = f"""
    select
        distinct {dim} as result
    from 
        `team-begamob.{project_id}_CACHED_Events_04.IDENTIFY_USER`
    where
        {dim} is not null
        {gbq_filter_return(dict_source_filter, ['install_date'])}
    order by 1 asc
        """
    else:
        query = f"""
    select
        distinct {dim} as result
    from 
        `team-begamob.{project_id}_CACHED_Events_06.Firebase_Overview_Daily_Metrics`
    where
        {dim} is not null
        {gbq_filter_return(dict_source_filter)}
    order by 1 desc
        """
    try:
        df = client.query(query).to_dataframe()
        return df['result'].tolist()
    except Exception as error:
        return {"error": str(error)}

def gbq_source_discover_query(
        project_id, 
        dict_event_filter,
        list_source_input,
        list_node_filter,
        kind,
        ):
    query_to_filter = []
    for i in range(len(list_source_input)):
        if 'CACHED_Events_02' in list_source_input[i]['table']:
            session_filter = f"""first_value(safe_cast(params_session_number as int64) ignore nulls) over (
                            partition by user_pseudo_id
                            order by event_timestamp
                            rows between current row and unbounded following
                ) as session_number,"""
        else:
            session_filter = ''

        process_source_filter = 'and ' + list_source_input[i]['filter'] if list_source_input[i]['filter'] else ''
        
        if kind == 'discover':
            filter =  f"""{gbq_filter_return(dict_event_filter, ['install_date', 'country', 'version', 'number_day_install'])}"""
        elif kind == 'sankey':
            filter =  f"""{gbq_filter_return(dict_event_filter, ['install_date', 'country', 'version', 'session_number', 'number_day_install'])}"""

        _query = f"""(
        select
            user_pseudo_id,
            session_number,
            event_timestamp,
            '{list_source_input[i]['name']}' action_type,
            {list_source_input[i]['column']} action_name
        from (
            select
                *,
                {session_filter}
            from
                `team-begamob.{project_id}_{list_source_input[i]['table']}`
            where true
                {gbq_filter_return(dict_event_filter, ['event_date'])}
        )
        where true
            {filter}
            {process_source_filter}
            {gbq_str_filter(list_source_input[i]['column'], list_node_filter[i])}
        )
        """
        query_to_filter.append(_query)
    return query_to_filter

def gbq_source_prepare_sankey_query(gbq_source_discover_query):
    _query_demo = f"""with source as (
        """
    for i, query in enumerate(gbq_source_discover_query):
        _query_demo += query
        if i < len(gbq_source_discover_query) - 1:
            _query_demo += f"""union all
        """
        else:
            _query_demo += f"""
        ),"""
    return _query_demo

def display_user_node(client, _query, _source_name):
    _query_funnel = f"""
    select
        action_name screen,
        count(user_pseudo_id) events,
        count(distinct user_pseudo_id) users,
    from {_query}
    group by 1
    order by 3 desc
    """
    try:
        df_funnel = client.query(_query_funnel).to_dataframe()
    except Exception as error:
        return None, None, str(error)

    max_user = df_funnel['users'].max()
    df_funnel['percent'] = (df_funnel['users'] / max_user) * 100
    df_funnel['percent'] = df_funnel['percent'].round(2)

    fig = make_subplots(rows=1, cols=2,
                        specs=[[{"type": "bar"}, {"type": "table"}]])
    fig.add_trace(
        go.Funnel(
            y = df_funnel['screen'],
            x = df_funnel['users'],
            textinfo = "value+percent initial",
            marker = {"color": "deepskyblue"}
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Table(
            header=dict(values=[_source_name, 'events', 'users', '% users']),
            cells=dict(values=[df_funnel.screen, df_funnel.events, df_funnel.users, df_funnel.percent])
        ),
        row=1, col=2
    )
    fig.update_layout(
        title = f"User flow for {_source_name} node",
        template="plotly_dark",
        width=1600, height=800
    )

    # Return the figure and the list of screens
    return fig, df_funnel.screen.tolist(), None

def query_process_sankey(splash_screen, project_id, dict_event_filter, number_node, kind):
    # Generate dynamic parts of the query
    gen_query_agg = ''
    gen_query_concat = ''
    gen_query_groupby = ''
    gen_query_time_diff = ''
    gen_query_time_bin = ''
    gen_query_bin_counts = ''
    gen_query_final_select = ''
    gen_query_final_order = ''

    for i in range(number_node):
        gen_query_agg += f"""
            coalesce(max(case when event_row_in_flow = {i} then action_name end), 'Drop') as s{i},
            coalesce(max(case when event_row_in_flow = {i} then event_timestamp end), max(last_timestamp)) as t{i},"""
        gen_query_concat += f"concat('{i}.', s{i}) as s{i},"
        gen_query_groupby += f"s{i}, "
        if i > 0:
            gen_query_time_diff += f"""
            IFNULL(TIMESTAMP_DIFF(t{i}, t{i-1}, MILLISECOND) / 1000.0, -1) AS t{i},"""
            gen_query_time_bin += f"""
            CASE
                WHEN t{i} = -1 THEN 'Invalid'
                WHEN t{i} >= 0 AND t{i} < 1 THEN '0s'
                WHEN t{i} >= 1 AND t{i} < 2 THEN '1s'
                WHEN t{i} >= 2 AND t{i} < 3 THEN '2s'
                WHEN t{i} >= 3 AND t{i} < 4 THEN '3s'
                WHEN t{i} >= 4 AND t{i} < 5 THEN '4s'
                WHEN t{i} >= 5 AND t{i} < 6 THEN '5s'
                WHEN t{i} >= 6 AND t{i} < 7 THEN '6s'
                WHEN t{i} >= 7 AND t{i} < 8 THEN '7s'
                WHEN t{i} >= 8 AND t{i} < 9 THEN '8s'
                WHEN t{i} >= 9 AND t{i} < 10 THEN '9s'
                WHEN t{i} >= 10 AND t{i} < 13 THEN '10s'
                WHEN t{i} >= 13 AND t{i} < 15 THEN '13s'
                WHEN t{i} >= 15 AND t{i} < 17 THEN '15s'
                WHEN t{i} >= 17 AND t{i} < 20 THEN '17s'
                WHEN t{i} >= 20 AND t{i} < 25 THEN '20s'
                WHEN t{i} >= 25 AND t{i} < 30 THEN '25s'
                WHEN t{i} >= 30 AND t{i} < 45 THEN '30s'
                WHEN t{i} >= 45 AND t{i} < 60 THEN '45s'
                WHEN t{i} >= 60 AND t{i} < 120 THEN '1m'
                WHEN t{i} >= 120 AND t{i} < 180 THEN '2m'
                WHEN t{i} >= 180 AND t{i} < 240 THEN '3m'
                WHEN t{i} >= 240 AND t{i} < 300 THEN '4m'
                WHEN t{i} >= 300 AND t{i} < 360 THEN '5m'
                WHEN t{i} >= 360 AND t{i} < 420 THEN '6m'
                WHEN t{i} >= 420 AND t{i} < 480 THEN '7m'
                WHEN t{i} >= 480 AND t{i} < 540 THEN '8m'
                WHEN t{i} >= 540 AND t{i} < 600 THEN '9m'
                WHEN t{i} >= 600 AND t{i} < 660 THEN '10m'
                WHEN t{i} >= 660 AND t{i} < 900 THEN '11m'
                WHEN t{i} >= 900 AND t{i} < 1800 THEN '15m'
                WHEN t{i} >= 1800 AND t{i} < 2700 THEN '30m'
                WHEN t{i} >= 2700 AND t{i} < 3600 THEN '45m'
                WHEN t{i} >= 3600 AND t{i} < 7200 THEN '1hr'
                WHEN t{i} >= 7200 AND t{i} < 10800 THEN '2hr'
                WHEN t{i} >= 10800 THEN '>2hr'
                ELSE 'Invalid'
            END AS t{i}_bin,"""
            gen_query_bin_counts += f"t{i}_bin AS s{i}_bin, COUNT(*) AS s{i}_count,"
            gen_query_final_select += f"s{i}_bin, s{i}_count,"
            gen_query_final_order += f"s{i}_count DESC, "

    # Remove trailing commas and spaces
    gen_query_agg = gen_query_agg.rstrip(',')
    gen_query_concat = gen_query_concat.rstrip(',')
    gen_query_groupby = gen_query_groupby.rstrip(', ')
    gen_query_time_diff = gen_query_time_diff.rstrip(',')
    gen_query_time_bin = gen_query_time_bin.rstrip(',')
    gen_query_bin_counts = gen_query_bin_counts.rstrip(',')
    gen_query_final_select = gen_query_final_select.rstrip(',')
    gen_query_final_order = gen_query_final_order.rstrip(', ')


    if kind == 'default':
        query_preprocess = f"""
    start_flow AS (
        SELECT
            user_pseudo_id,
            event_timestamp AS flow_timestamp,
            ROW_NUMBER() OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS flow_row_number,
            LEAD(event_timestamp) OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS following_flow_timestamp
        FROM source
        WHERE CONTAINS_SUBSTR(LOWER(action_name), '{splash_screen}')
    ),
    source2 AS (
        SELECT
            r.*,
            s.flow_row_number,
            s.flow_timestamp
        FROM source r
        LEFT JOIN start_flow s
            ON r.user_pseudo_id = s.user_pseudo_id
            AND r.event_timestamp BETWEEN s.flow_timestamp AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1)
            AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1) - s.flow_timestamp > 1*1000000
    ),
    source3 AS (
        SELECT
            user_pseudo_id,
            session_number,
            flow_row_number,
            action_name,
            TIMESTAMP_MICROS(event_timestamp) AS event_timestamp,
            LAG(action_name, 1, '') OVER (PARTITION BY user_pseudo_id, flow_row_number ORDER BY event_timestamp) AS action_name_filter,
            ROW_NUMBER() OVER (PARTITION BY user_pseudo_id, flow_row_number, action_name ORDER BY event_timestamp) AS row_num_filter
        FROM source2
    ),
    source4 AS (
        SELECT
            user_pseudo_id,
            session_number,
            event_timestamp,
            flow_row_number,
            action_name,
            ROW_NUMBER() OVER (PARTITION BY user_pseudo_id, flow_row_number ORDER BY event_timestamp) - 1 AS event_row_in_flow,
            MIN(event_timestamp) OVER (PARTITION BY user_pseudo_id, flow_row_number) AS first_flow_timestamp,
            LEAD(event_timestamp, 1, TIMESTAMP '2092-02-29') OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp) AS last_flow_timestamp
        FROM source3
        WHERE action_name_filter != action_name
            AND flow_row_number IS NOT NULL
    ),
    engagement AS (
        SELECT
            user_pseudo_id,
            TIMESTAMP_MICROS(event_timestamp) AS event_timestamp
        FROM `team-begamob.{project_id}_CACHED_Events_01.Firebase_Events_USER_ENGAGEMENT`
        WHERE true
        {gbq_filter_return(dict_event_filter, ['event_date', 'country'])}
    ),
    source5 AS (
        SELECT
            user_pseudo_id,
            session_number,
            event_timestamp,
            flow_row_number,
            action_name,
            event_row_in_flow,
            first_flow_timestamp,
            MAX(last_flow_timestamp) OVER (PARTITION BY user_pseudo_id, flow_row_number) AS last_flow_timestamp
        FROM source4
    ),
    identify_last_engagement_event AS (
        SELECT
            a.user_pseudo_id,
            a.flow_row_number,
            MAX(b.event_timestamp) AS last_eng_event_timestamp
        FROM source5 a
        LEFT JOIN engagement b
            ON a.user_pseudo_id = b.user_pseudo_id
            AND a.first_flow_timestamp < b.event_timestamp
            AND b.event_timestamp < a.last_flow_timestamp
        WHERE TIMESTAMP_DIFF(b.event_timestamp, a.first_flow_timestamp, HOUR) < 24
        GROUP BY 1, 2
    ),
    source6 as (
        select
            a.user_pseudo_id,
            a.session_number,
            a.flow_row_number,
            a.action_name,
            a.event_row_in_flow,
            a.event_timestamp,
            a.first_flow_timestamp first_timestamp,
            coalesce(
                last_eng_event_timestamp, 
                if(last_flow_timestamp = timestamp '2092-02-29', null, last_flow_timestamp)    
            ) as last_timestamp,
        from source5 a
        left join identify_last_engagement_event b
            on  a.user_pseudo_id = b.user_pseudo_id
            and a.flow_row_number = b.flow_row_number
    ),
        """
    elif kind == 'exact_location':
        query_preprocess = f"""
    start_flow AS (
        SELECT
            user_pseudo_id,
            event_timestamp AS flow_timestamp,
            ROW_NUMBER() OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS flow_row_number,
            LEAD(event_timestamp) OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS following_flow_timestamp
        FROM source
        WHERE CONTAINS_SUBSTR(LOWER(action_name), '{splash_screen}')
    ),
    source2 AS (
        SELECT
            r.*,
            s.flow_row_number,
            s.flow_timestamp
        FROM source r
        LEFT JOIN start_flow s
            ON r.user_pseudo_id = s.user_pseudo_id
            AND r.event_timestamp BETWEEN s.flow_timestamp AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1)
            AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1) - s.flow_timestamp > 1*1000000
    ),
    source3 AS (
        SELECT
            user_pseudo_id,
            session_number,
            flow_row_number,
            action_name,
            TIMESTAMP_MICROS(event_timestamp) AS event_timestamp,
            LAG(action_name, 1, '') OVER (PARTITION BY user_pseudo_id, flow_row_number ORDER BY event_timestamp) AS action_name_filter,
            ROW_NUMBER() OVER (PARTITION BY user_pseudo_id, flow_row_number, action_name ORDER BY event_timestamp) AS row_num_filter
        FROM source2
    ),
    source4 AS (
        SELECT
            user_pseudo_id,
            session_number,
            event_timestamp,
            flow_row_number,
            action_name,
            ROW_NUMBER() OVER (PARTITION BY user_pseudo_id, flow_row_number ORDER BY event_timestamp) - 1 AS event_row_in_flow,
            MIN(event_timestamp) OVER (PARTITION BY user_pseudo_id, flow_row_number) AS first_flow_timestamp,
            LEAD(event_timestamp, 1, TIMESTAMP '2092-02-29') OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp) AS last_flow_timestamp
        FROM source3
        WHERE action_name_filter != action_name
            AND flow_row_number IS NOT NULL
    ),
    source_lead as (
    select
        *,
        lag(event_timestamp) over (partition by user_pseudo_id order by event_timestamp asc) as lag_timestamp,
        max(event_timestamp) over (partition by user_pseudo_id, flow_row_number) as end_ss_timestamp
    from source4
    where true

    ),
    
    start_flowb as (
        select
            user_pseudo_id,
            event_timestamp,
            row_number() over (partition by user_pseudo_id order by event_timestamp asc) as flowb_number,
            lag_timestamp as start_timestamp,
            end_ss_timestamp as end_timestamp,
        from source_lead
        where true
        and action_name = 'main'
    ),
    
    source4b as (
        select
            r.* except(event_row_in_flow),
            flowb_number,
            row_number() over (partition by r.user_pseudo_id, flowb_number order by r.event_timestamp asc) - 1 as event_row_in_flow
        from source_lead r
        join start_flowb s
            on r.user_pseudo_id = s.user_pseudo_id
            and r.event_timestamp between s.start_timestamp and s.end_timestamp
        where true
    ),

    engagement AS (
        SELECT
            user_pseudo_id,
            TIMESTAMP_MICROS(event_timestamp) AS event_timestamp
        FROM `team-begamob.{project_id}_CACHED_Events_01.Firebase_Events_USER_ENGAGEMENT`
        WHERE true
        {gbq_filter_return(dict_event_filter, ['event_date', 'country'])}
    ),
    source5 AS (
        SELECT
            user_pseudo_id,
            session_number,
            event_timestamp,
            flow_row_number,
            action_name,
            event_row_in_flow,
            first_flow_timestamp,
            MAX(last_flow_timestamp) OVER (PARTITION BY user_pseudo_id, flow_row_number) AS last_flow_timestamp
        FROM source4b
    ),
    identify_last_engagement_event AS (
        SELECT
            a.user_pseudo_id,
            a.flow_row_number,
            MAX(b.event_timestamp) AS last_eng_event_timestamp
        FROM source5 a
        LEFT JOIN engagement b
            ON a.user_pseudo_id = b.user_pseudo_id
            AND a.first_flow_timestamp < b.event_timestamp
            AND b.event_timestamp < a.last_flow_timestamp
        WHERE TIMESTAMP_DIFF(b.event_timestamp, a.first_flow_timestamp, HOUR) < 24
        GROUP BY 1, 2
    ),
    source6 as (
        select
            a.user_pseudo_id,
            a.session_number,
            a.flow_row_number,
            a.action_name,
            a.event_row_in_flow,
            a.event_timestamp,
            a.first_flow_timestamp first_timestamp,
            coalesce(
                last_eng_event_timestamp, 
                if(last_flow_timestamp = timestamp '2092-02-29', null, last_flow_timestamp)    
            ) as last_timestamp,
        from source5 a
        left join identify_last_engagement_event b
            on  a.user_pseudo_id = b.user_pseudo_id
            and a.flow_row_number = b.flow_row_number
    ),
        """
    # Construct the full query
    query = f"""

    pivot AS (
        SELECT
            user_pseudo_id,
            flow_row_number,
            {gen_query_agg}
        FROM source6
        where true
        {gbq_filter_return(dict_event_filter, ['session_number'])}
        GROUP BY 1, 2
    ),
    time_diff AS (
        SELECT
            user_pseudo_id,
            flow_row_number,
            {gen_query_concat},
            0 AS t0,
            {gen_query_time_diff}
        FROM pivot
    ),
    binned_time AS (
        SELECT
            {gen_query_groupby},
            {gen_query_time_bin}
        FROM time_diff
    ),
    bin_counts AS (
        SELECT
            {gen_query_groupby},
            {gen_query_bin_counts}
        FROM binned_time
        GROUP BY {gen_query_groupby}, {', '.join([f't{i}_bin' for i in range(1, number_node)])}
    )
    SELECT
        {gen_query_groupby},
        {gen_query_final_select}
    FROM bin_counts
    """

    return query_preprocess + query

def query_process_sankey_reverse(splash_screen, project_id, dict_event_filter, number_node, kind):
    # Generate dynamic parts of the query
    gen_query_agg = f"'{kind}' as s0,\n"
    gen_query_agg += "coalesce(max(case when event_row_in_flow = 1 then event_timestamp end), max(last_timestamp)) as t0,\n"
    gen_query_concat = "concat('0.', s0) as s0,"
    gen_query_groupby = 's0, '
    gen_query_time_diff = ''
    gen_query_time_bin = ''
    gen_query_bin_counts = ''
    gen_query_final_select = ''
    gen_query_final_order = ''

    for i in range(1, number_node):
        gen_query_agg += f"""
            coalesce(max(case when event_row_in_flow = {i} then action_name end), 'NA') as s{i},
            max(case when event_row_in_flow = {i} then event_timestamp end) as t{i},"""
        gen_query_concat += f"concat('{i}.', s{i}) as s{i},"
        gen_query_groupby += f"s{i}, "
        gen_query_time_diff += f"""
            IFNULL(TIMESTAMP_DIFF(t{i-1}, t{i}, MILLISECOND) / 1000.0, -1) AS t{i},"""
        gen_query_time_bin += f"""
            CASE
                WHEN t{i} = -1 THEN 'Invalid'
                WHEN t{i} >= 0 AND t{i} < 1 THEN '0s'
                WHEN t{i} >= 1 AND t{i} < 2 THEN '1s'
                WHEN t{i} >= 2 AND t{i} < 3 THEN '2s'
                WHEN t{i} >= 3 AND t{i} < 4 THEN '3s'
                WHEN t{i} >= 4 AND t{i} < 5 THEN '4s'
                WHEN t{i} >= 5 AND t{i} < 6 THEN '5s'
                WHEN t{i} >= 6 AND t{i} < 7 THEN '6s'
                WHEN t{i} >= 7 AND t{i} < 8 THEN '7s'
                WHEN t{i} >= 8 AND t{i} < 9 THEN '8s'
                WHEN t{i} >= 9 AND t{i} < 10 THEN '9s'
                WHEN t{i} >= 10 AND t{i} < 13 THEN '10s'
                WHEN t{i} >= 13 AND t{i} < 15 THEN '13s'
                WHEN t{i} >= 15 AND t{i} < 17 THEN '15s'
                WHEN t{i} >= 17 AND t{i} < 20 THEN '17s'
                WHEN t{i} >= 20 AND t{i} < 25 THEN '20s'
                WHEN t{i} >= 25 AND t{i} < 30 THEN '25s'
                WHEN t{i} >= 30 AND t{i} < 45 THEN '30s'
                WHEN t{i} >= 45 AND t{i} < 60 THEN '45s'
                WHEN t{i} >= 60 AND t{i} < 120 THEN '1m'
                WHEN t{i} >= 120 AND t{i} < 180 THEN '2m'
                WHEN t{i} >= 180 AND t{i} < 240 THEN '3m'
                WHEN t{i} >= 240 AND t{i} < 300 THEN '4m'
                WHEN t{i} >= 300 AND t{i} < 360 THEN '5m'
                WHEN t{i} >= 360 AND t{i} < 420 THEN '6m'
                WHEN t{i} >= 420 AND t{i} < 480 THEN '7m'
                WHEN t{i} >= 480 AND t{i} < 540 THEN '8m'
                WHEN t{i} >= 540 AND t{i} < 600 THEN '9m'
                WHEN t{i} >= 600 AND t{i} < 660 THEN '10m'
                WHEN t{i} >= 660 AND t{i} < 900 THEN '11m'
                WHEN t{i} >= 900 AND t{i} < 1800 THEN '15m'
                WHEN t{i} >= 1800 AND t{i} < 2700 THEN '30m'
                WHEN t{i} >= 2700 AND t{i} < 3600 THEN '45m'
                WHEN t{i} >= 3600 AND t{i} < 7200 THEN '1hr'
                WHEN t{i} >= 7200 AND t{i} < 10800 THEN '2hr'
                WHEN t{i} >= 10800 THEN '>2hr'
                ELSE 'Invalid'
            END AS t{i}_bin,"""
        gen_query_bin_counts += f"t{i}_bin AS s{i}_bin, COUNT(*) AS s{i}_count,"
        gen_query_final_select += f"s{i}_bin, SUM(s{i}_count) AS s{i}_count,"
        gen_query_final_order += f"SUM(s{i}_count) DESC, "

    source_remove = f"""
     last_session as(
        select
            user_pseudo_id,
            max(session_number) session_number
        from
            `team-begamob.cast_glitter_CACHED_Events_01.Firebase_Events_APP_REMOVE`
        where true
        {gbq_filter_return(dict_event_filter, ['event_date', 'country'])}
        group by 1
    ),
    source0 as (
        select
            a.*
        from source a
        inner join last_session b
            on a.user_pseudo_id = b.user_pseudo_id
            and a.session_number = b.session_number
    ),
    start_flow AS (
        SELECT
            user_pseudo_id,
            event_timestamp AS flow_timestamp,
            ROW_NUMBER() OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS flow_row_number,
            LEAD(event_timestamp) OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS following_flow_timestamp
        FROM source
        WHERE CONTAINS_SUBSTR(LOWER(action_name), 'splash')
    ),
    source2 AS (
        SELECT
            r.*,
            s.flow_row_number,
            s.flow_timestamp
        FROM source r
        LEFT JOIN start_flow s
            ON r.user_pseudo_id = s.user_pseudo_id
            AND r.event_timestamp BETWEEN s.flow_timestamp AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1)
            AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1) - s.flow_timestamp > 1*1000000
    ),
    source3 AS (
        SELECT
            user_pseudo_id,
            session_number,
            flow_row_number,
            action_name,
            TIMESTAMP_MICROS(event_timestamp) AS event_timestamp,
            LAG(action_name, 1, '') OVER (PARTITION BY user_pseudo_id, flow_row_number ORDER BY event_timestamp) AS action_name_filter,
            ROW_NUMBER() OVER (PARTITION BY user_pseudo_id, flow_row_number, action_name ORDER BY event_timestamp) AS row_num_filter
        FROM source2
    ),
    source4 AS (
        SELECT
            a.user_pseudo_id,
            a.session_number,
            a.event_timestamp,
            a.flow_row_number,
            a.action_name,
            ROW_NUMBER() OVER (PARTITION BY a.user_pseudo_id, a.flow_row_number ORDER BY a.event_timestamp desc) AS event_row_in_flow,
            MIN(a.event_timestamp) OVER (PARTITION BY a.user_pseudo_id, a.flow_row_number) AS first_flow_timestamp,
            LEAD(a.event_timestamp, 1, TIMESTAMP '2092-02-29') OVER (PARTITION BY a.user_pseudo_id ORDER BY a.event_timestamp) AS last_flow_timestamp
        FROM source3 a
        inner join (
            select
                user_pseudo_id,
                max(flow_row_number) flow_row_number,
            from source3
                where flow_row_number is not null
            group by 1
        ) b
        on a.user_pseudo_id = b.user_pseudo_id
        and a.flow_row_number = b.flow_row_number
        WHERE action_name_filter != action_name
            AND a.flow_row_number IS NOT NULL
    ),
    """
    
    source_drop = f"""
    start_flow AS (
        SELECT
            user_pseudo_id,
            event_timestamp AS flow_timestamp,
            ROW_NUMBER() OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS flow_row_number,
            LEAD(event_timestamp) OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS following_flow_timestamp
        FROM source
        WHERE CONTAINS_SUBSTR(LOWER(action_name), 'splash')
    ),
    source2 AS (
        SELECT
            r.*,
            s.flow_row_number,
            s.flow_timestamp
        FROM source r
        LEFT JOIN start_flow s
            ON r.user_pseudo_id = s.user_pseudo_id
            AND r.event_timestamp BETWEEN s.flow_timestamp AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1)
            AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1) - s.flow_timestamp > 1*1000000
    ),
    source3 AS (
        SELECT
            user_pseudo_id,
            session_number,
            flow_row_number,
            action_name,
            TIMESTAMP_MICROS(event_timestamp) AS event_timestamp,
            LAG(action_name, 1, '') OVER (PARTITION BY user_pseudo_id, flow_row_number ORDER BY event_timestamp) AS action_name_filter,
            ROW_NUMBER() OVER (PARTITION BY user_pseudo_id, flow_row_number, action_name ORDER BY event_timestamp) AS row_num_filter
        FROM source2
    ),
    source4 AS (
        SELECT
            a.user_pseudo_id,
            a.session_number,
            a.event_timestamp,
            a.flow_row_number,
            a.action_name,
            ROW_NUMBER() OVER (PARTITION BY a.user_pseudo_id, a.flow_row_number ORDER BY a.event_timestamp desc) AS event_row_in_flow,
            MIN(a.event_timestamp) OVER (PARTITION BY a.user_pseudo_id, a.flow_row_number) AS first_flow_timestamp,
            LEAD(a.event_timestamp, 1, TIMESTAMP '2092-02-29') OVER (PARTITION BY a.user_pseudo_id ORDER BY a.event_timestamp) AS last_flow_timestamp
        FROM source3 a
    ),
    """
    # Construct the full query
    query = f"""
    engagement AS (
        SELECT
            user_pseudo_id,
            session_number,
            TIMESTAMP_MICROS(event_timestamp) AS event_timestamp
        FROM `team-begamob.cast_glitter_CACHED_Events_01.Firebase_Events_USER_ENGAGEMENT`
        WHERE true
        {gbq_filter_return(dict_event_filter, ['event_date', 'country'])}
    ),
    source5 AS (
        SELECT
            user_pseudo_id,
            session_number,
            event_timestamp,
            flow_row_number,
            action_name,
            event_row_in_flow,
            first_flow_timestamp,
            MAX(last_flow_timestamp) OVER (PARTITION BY user_pseudo_id, flow_row_number) AS last_flow_timestamp
        FROM source4
    ),
    identify_last_engagement_event AS (
        SELECT
            a.user_pseudo_id,
            a.session_number,
            a.flow_row_number,
            MAX(b.event_timestamp) AS last_eng_event_timestamp
        FROM source5 a
        LEFT JOIN engagement b
            ON a.user_pseudo_id = b.user_pseudo_id
            AND a.first_flow_timestamp < b.event_timestamp
            AND b.event_timestamp < a.last_flow_timestamp
        WHERE TIMESTAMP_DIFF(b.event_timestamp, a.first_flow_timestamp, HOUR) < 24
        GROUP BY 1, 2, 3
    ),
    source6 as (
        select
            a.user_pseudo_id,
            a.session_number,
            a.flow_row_number,
            a.action_name,
            a.event_row_in_flow,
            a.event_timestamp,
            a.first_flow_timestamp first_timestamp,
            coalesce(
                last_eng_event_timestamp, 
                if(last_flow_timestamp = timestamp '2092-02-29', null, last_flow_timestamp)    
            ) as last_timestamp,
        from source5 a
        left join identify_last_engagement_event b
            on  a.user_pseudo_id = b.user_pseudo_id
            and a.flow_row_number = b.flow_row_number
    ),
    pivot AS (
        SELECT
            user_pseudo_id,
            flow_row_number,
            {gen_query_agg}
        FROM source6
        where true
        {gbq_filter_return(dict_event_filter, ['session_number'])}
        GROUP BY 1, 2
    ),
    time_diff AS (
        SELECT
            user_pseudo_id,
            flow_row_number,
            {gen_query_concat}
            {gen_query_time_diff}
        FROM pivot
    ),
    binned_time AS (
        SELECT
            {gen_query_groupby}
            {gen_query_time_bin}
        FROM time_diff
    ),
    bin_counts AS (
        SELECT
            {gen_query_groupby}
            {gen_query_bin_counts}
        FROM binned_time
        GROUP BY {gen_query_groupby} {', '.join([f't{i}_bin' for i in range(1, number_node)])}
    )
    SELECT
        {gen_query_groupby}
        {gen_query_final_select}
    FROM bin_counts
    GROUP BY {gen_query_groupby} {', '.join([f's{i}_bin' for i in range(1, number_node)])}
    """
    if kind == 'Drop':
        return source_drop + query
    elif kind == 'Remove':
        return source_remove + query
    else:
        return ""

def query_process_sankey_combined(splash_screen, project_id, dict_event_filter, number_node, kind, direction='forward', event_start = 'main'):
    # Generate dynamic parts of the query
    gen_query_agg = ''
    gen_query_concat = ''
    gen_query_groupby = ''
    gen_query_time_diff = ''
    gen_query_time_bin = ''
    gen_query_bin_counts = ''
    gen_query_final_select = ''
    gen_query_final_order = ''

    if direction == 'forward':
        for i in range(number_node):
            gen_query_agg += f"""
                coalesce(max(case when event_row_in_flow = {i} then action_name end), 'Drop') as s{i},
                coalesce(max(case when event_row_in_flow = {i} then event_timestamp end), max(last_timestamp)) as t{i},"""
            gen_query_concat += f"concat('{i}.', s{i}) as s{i},"
            gen_query_groupby += f"s{i}, "
            if i > 0:
                gen_query_time_diff += f"""
                IFNULL(TIMESTAMP_DIFF(t{i}, t{i-1}, MILLISECOND) / 1000.0, -1) AS t{i},"""
                gen_query_time_bin += f"""
                CASE
                    WHEN t{i} = -1 THEN 'Invalid'
                    WHEN t{i} >= 0 AND t{i} < 1 THEN '0s'
                    WHEN t{i} >= 1 AND t{i} < 2 THEN '1s'
                    WHEN t{i} >= 2 AND t{i} < 3 THEN '2s'
                    WHEN t{i} >= 3 AND t{i} < 4 THEN '3s'
                    WHEN t{i} >= 4 AND t{i} < 5 THEN '4s'
                    WHEN t{i} >= 5 AND t{i} < 6 THEN '5s'
                    WHEN t{i} >= 6 AND t{i} < 7 THEN '6s'
                    WHEN t{i} >= 7 AND t{i} < 8 THEN '7s'
                    WHEN t{i} >= 8 AND t{i} < 9 THEN '8s'
                    WHEN t{i} >= 9 AND t{i} < 10 THEN '9s'
                    WHEN t{i} >= 10 AND t{i} < 13 THEN '10s'
                    WHEN t{i} >= 13 AND t{i} < 15 THEN '13s'
                    WHEN t{i} >= 15 AND t{i} < 17 THEN '15s'
                    WHEN t{i} >= 17 AND t{i} < 20 THEN '17s'
                    WHEN t{i} >= 20 AND t{i} < 25 THEN '20s'
                    WHEN t{i} >= 25 AND t{i} < 30 THEN '25s'
                    WHEN t{i} >= 30 AND t{i} < 45 THEN '30s'
                    WHEN t{i} >= 45 AND t{i} < 60 THEN '45s'
                    WHEN t{i} >= 60 AND t{i} < 120 THEN '1m'
                    WHEN t{i} >= 120 AND t{i} < 180 THEN '2m'
                    WHEN t{i} >= 180 AND t{i} < 240 THEN '3m'
                    WHEN t{i} >= 240 AND t{i} < 300 THEN '4m'
                    WHEN t{i} >= 300 AND t{i} < 360 THEN '5m'
                    WHEN t{i} >= 360 AND t{i} < 420 THEN '6m'
                    WHEN t{i} >= 420 AND t{i} < 480 THEN '7m'
                    WHEN t{i} >= 480 AND t{i} < 540 THEN '8m'
                    WHEN t{i} >= 540 AND t{i} < 600 THEN '9m'
                    WHEN t{i} >= 600 AND t{i} < 660 THEN '10m'
                    WHEN t{i} >= 660 AND t{i} < 900 THEN '11m'
                    WHEN t{i} >= 900 AND t{i} < 1800 THEN '15m'
                    WHEN t{i} >= 1800 AND t{i} < 2700 THEN '30m'
                    WHEN t{i} >= 2700 AND t{i} < 3600 THEN '45m'
                    WHEN t{i} >= 3600 AND t{i} < 7200 THEN '1hr'
                    WHEN t{i} >= 7200 AND t{i} < 10800 THEN '2hr'
                    WHEN t{i} >= 10800 THEN '>2hr'
                    ELSE 'Invalid'
                END AS t{i}_bin,"""
                gen_query_bin_counts += f"t{i}_bin AS s{i}_bin, COUNT(*) AS s{i}_count,"
                gen_query_final_select += f"s{i}_bin, s{i}_count,"
                gen_query_final_order += f"s{i}_count DESC, "
    else:  # reverse
        gen_query_agg = f"'{kind}' as s0,\n"
        gen_query_agg += "coalesce(max(case when event_row_in_flow = 1 then event_timestamp end), max(last_timestamp)) as t0,\n"
        gen_query_concat = "concat('0.', s0) as s0,"
        gen_query_groupby = 's0, '
        for i in range(1, number_node):
            gen_query_agg += f"""
                coalesce(max(case when event_row_in_flow = {i} then action_name end), 'NA') as s{i},
                max(case when event_row_in_flow = {i} then event_timestamp end) as t{i},"""
            gen_query_concat += f"concat('{i}.', s{i}) as s{i},"
            gen_query_groupby += f"s{i}, "
            gen_query_time_diff += f"""
                IFNULL(TIMESTAMP_DIFF(t{i-1}, t{i}, MILLISECOND) / 1000.0, -1) AS t{i},"""
            gen_query_time_bin += f"""
                CASE
                    WHEN t{i} = -1 THEN 'Invalid'
                    WHEN t{i} >= 0 AND t{i} < 1 THEN '0s'
                    WHEN t{i} >= 1 AND t{i} < 2 THEN '1s'
                    WHEN t{i} >= 2 AND t{i} < 3 THEN '2s'
                    WHEN t{i} >= 3 AND t{i} < 4 THEN '3s'
                    WHEN t{i} >= 4 AND t{i} < 5 THEN '4s'
                    WHEN t{i} >= 5 AND t{i} < 6 THEN '5s'
                    WHEN t{i} >= 6 AND t{i} < 7 THEN '6s'
                    WHEN t{i} >= 7 AND t{i} < 8 THEN '7s'
                    WHEN t{i} >= 8 AND t{i} < 9 THEN '8s'
                    WHEN t{i} >= 9 AND t{i} < 10 THEN '9s'
                    WHEN t{i} >= 10 AND t{i} < 13 THEN '10s'
                    WHEN t{i} >= 13 AND t{i} < 15 THEN '13s'
                    WHEN t{i} >= 15 AND t{i} < 17 THEN '15s'
                    WHEN t{i} >= 17 AND t{i} < 20 THEN '17s'
                    WHEN t{i} >= 20 AND t{i} < 25 THEN '20s'
                    WHEN t{i} >= 25 AND t{i} < 30 THEN '25s'
                    WHEN t{i} >= 30 AND t{i} < 45 THEN '30s'
                    WHEN t{i} >= 45 AND t{i} < 60 THEN '45s'
                    WHEN t{i} >= 60 AND t{i} < 120 THEN '1m'
                    WHEN t{i} >= 120 AND t{i} < 180 THEN '2m'
                    WHEN t{i} >= 180 AND t{i} < 240 THEN '3m'
                    WHEN t{i} >= 240 AND t{i} < 300 THEN '4m'
                    WHEN t{i} >= 300 AND t{i} < 360 THEN '5m'
                    WHEN t{i} >= 360 AND t{i} < 420 THEN '6m'
                    WHEN t{i} >= 420 AND t{i} < 480 THEN '7m'
                    WHEN t{i} >= 480 AND t{i} < 540 THEN '8m'
                    WHEN t{i} >= 540 AND t{i} < 600 THEN '9m'
                    WHEN t{i} >= 600 AND t{i} < 660 THEN '10m'
                    WHEN t{i} >= 660 AND t{i} < 900 THEN '11m'
                    WHEN t{i} >= 900 AND t{i} < 1800 THEN '15m'
                    WHEN t{i} >= 1800 AND t{i} < 2700 THEN '30m'
                    WHEN t{i} >= 2700 AND t{i} < 3600 THEN '45m'
                    WHEN t{i} >= 3600 AND t{i} < 7200 THEN '1hr'
                    WHEN t{i} >= 7200 AND t{i} < 10800 THEN '2hr'
                    WHEN t{i} >= 10800 THEN '>2hr'
                    ELSE 'Invalid'
                END AS t{i}_bin,"""
            gen_query_bin_counts += f"t{i}_bin AS s{i}_bin, COUNT(*) AS s{i}_count,"
            gen_query_final_select += f"s{i}_bin, SUM(s{i}_count) AS s{i}_count,"
            gen_query_final_order += f"SUM(s{i}_count) DESC, "

    # Remove trailing commas and spaces
    gen_query_agg = gen_query_agg.rstrip(',')
    gen_query_concat = gen_query_concat.rstrip(',')
    gen_query_groupby = gen_query_groupby.rstrip(', ')
    gen_query_time_diff = gen_query_time_diff.rstrip(',')
    gen_query_time_bin = gen_query_time_bin.rstrip(',')
    gen_query_bin_counts = gen_query_bin_counts.rstrip(',')
    gen_query_final_select = gen_query_final_select.rstrip(',')
    gen_query_final_order = gen_query_final_order.rstrip(', ')

    # Determine the appropriate preprocessing query
    if direction == 'forward':
        if kind == 'default':
            query_preprocess = f"""
            start_flow AS (
                SELECT
                    user_pseudo_id,
                    event_timestamp AS flow_timestamp,
                    ROW_NUMBER() OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS flow_row_number,
                    LEAD(event_timestamp) OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS following_flow_timestamp
                FROM source
                WHERE CONTAINS_SUBSTR(LOWER(action_name), '{splash_screen}')
            ),
            source2 AS (
                SELECT
                    r.*,
                    s.flow_row_number,
                    s.flow_timestamp
                FROM source r
                LEFT JOIN start_flow s
                    ON r.user_pseudo_id = s.user_pseudo_id
                    AND r.event_timestamp BETWEEN s.flow_timestamp AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1)
                    AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1) - s.flow_timestamp > 1*1000000
            ),
            source3 AS (
                SELECT
                    user_pseudo_id,
                    session_number,
                    flow_row_number,
                    action_name,
                    TIMESTAMP_MICROS(event_timestamp) AS event_timestamp,
                    LAG(action_name, 1, '') OVER (PARTITION BY user_pseudo_id, flow_row_number ORDER BY event_timestamp) AS action_name_filter,
                    ROW_NUMBER() OVER (PARTITION BY user_pseudo_id, flow_row_number, action_name ORDER BY event_timestamp) AS row_num_filter
                FROM source2
            ),
            source4 AS (
                SELECT
                    user_pseudo_id,
                    session_number,
                    event_timestamp,
                    flow_row_number,
                    action_name,
                    ROW_NUMBER() OVER (PARTITION BY user_pseudo_id, flow_row_number ORDER BY event_timestamp) - 1 AS event_row_in_flow,
                    MIN(event_timestamp) OVER (PARTITION BY user_pseudo_id, flow_row_number) AS first_flow_timestamp,
                    LEAD(event_timestamp, 1, TIMESTAMP '2092-02-29') OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp) AS last_flow_timestamp
                FROM source3
                WHERE action_name_filter != action_name
                    AND flow_row_number IS NOT NULL
            ),
            engagement AS (
                SELECT
                    user_pseudo_id,
                    TIMESTAMP_MICROS(event_timestamp) AS event_timestamp
                FROM `team-begamob.{project_id}_CACHED_Events_01.Firebase_Events_USER_ENGAGEMENT`
                WHERE true
                {gbq_filter_return(dict_event_filter, ['event_date', 'country'])}
            ),
            source5 AS (
                SELECT
                    user_pseudo_id,
                    session_number,
                    event_timestamp,
                    flow_row_number,
                    action_name,
                    event_row_in_flow,
                    first_flow_timestamp,
                    MAX(last_flow_timestamp) OVER (PARTITION BY user_pseudo_id, flow_row_number) AS last_flow_timestamp
                FROM source4
            ),
            identify_last_engagement_event AS (
                SELECT
                    a.user_pseudo_id,
                    a.flow_row_number,
                    MAX(b.event_timestamp) AS last_eng_event_timestamp
                FROM source5 a
                LEFT JOIN engagement b
                    ON a.user_pseudo_id = b.user_pseudo_id
                    AND a.first_flow_timestamp < b.event_timestamp
                    AND b.event_timestamp < a.last_flow_timestamp
                WHERE TIMESTAMP_DIFF(b.event_timestamp, a.first_flow_timestamp, HOUR) < 24
                GROUP BY 1, 2
            ),
            source6 as (
                select
                    a.user_pseudo_id,
                    a.session_number,
                    a.flow_row_number,
                    a.action_name,
                    a.event_row_in_flow,
                    a.event_timestamp,
                    a.first_flow_timestamp first_timestamp,
                    coalesce(
                        last_eng_event_timestamp, 
                        if(last_flow_timestamp = timestamp '2092-02-29', null, last_flow_timestamp)    
                    ) as last_timestamp,
                from source5 a
                left join identify_last_engagement_event b
                    on  a.user_pseudo_id = b.user_pseudo_id
                    and a.flow_row_number = b.flow_row_number
            ),
            """
        elif kind == 'exact_location':
            query_preprocess = f"""
            start_flow AS (
                SELECT
                    user_pseudo_id,
                    event_timestamp AS flow_timestamp,
                    ROW_NUMBER() OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS flow_row_number,
                    LEAD(event_timestamp) OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS following_flow_timestamp
                FROM source
                WHERE CONTAINS_SUBSTR(LOWER(action_name), '{splash_screen}')
            ),
            source2 AS (
                SELECT
                    r.*,
                    s.flow_row_number,
                    s.flow_timestamp
                FROM source r
                LEFT JOIN start_flow s
                    ON r.user_pseudo_id = s.user_pseudo_id
                    AND r.event_timestamp BETWEEN s.flow_timestamp AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1)
                    AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1) - s.flow_timestamp > 1*1000000
            ),
            source3 AS (
                SELECT
                    user_pseudo_id,
                    session_number,
                    flow_row_number,
                    action_name,
                    TIMESTAMP_MICROS(event_timestamp) AS event_timestamp,
                    LAG(action_name, 1, '') OVER (PARTITION BY user_pseudo_id, flow_row_number ORDER BY event_timestamp) AS action_name_filter,
                    ROW_NUMBER() OVER (PARTITION BY user_pseudo_id, flow_row_number, action_name ORDER BY event_timestamp) AS row_num_filter
                FROM source2
            ),
            source4 AS (
                SELECT
                    user_pseudo_id,
                    session_number,
                    event_timestamp,
                    flow_row_number,
                    action_name,
                    ROW_NUMBER() OVER (PARTITION BY user_pseudo_id, flow_row_number ORDER BY event_timestamp) - 1 AS event_row_in_flow,
                    MIN(event_timestamp) OVER (PARTITION BY user_pseudo_id, flow_row_number) AS first_flow_timestamp,
                    LEAD(event_timestamp, 1, TIMESTAMP '2092-02-29') OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp) AS last_flow_timestamp
                FROM source3
                WHERE action_name_filter != action_name
                    AND flow_row_number IS NOT NULL
            ),
            source_lead as (
            select
                *,
                lag(event_timestamp) over (partition by user_pseudo_id order by event_timestamp asc) as lag_timestamp,
                max(event_timestamp) over (partition by user_pseudo_id, flow_row_number) as end_ss_timestamp
            from source4
            where true
            ),
            start_flowb as (
                select
                    user_pseudo_id,
                    event_timestamp,
                    row_number() over (partition by user_pseudo_id order by event_timestamp asc) as flowb_number,
                    lag_timestamp as start_timestamp,
                    end_ss_timestamp as end_timestamp,
                from source_lead
                where true
                and action_name = '{event_start}'
            ),
            source4b as (
                select
                    r.* except(event_row_in_flow),
                    flowb_number,
                    row_number() over (partition by r.user_pseudo_id, flowb_number order by r.event_timestamp asc) - 1 as event_row_in_flow
                from source_lead r
                join start_flowb s
                    on r.user_pseudo_id = s.user_pseudo_id
                    and r.event_timestamp between s.start_timestamp and s.end_timestamp
                where true
            ),
            engagement AS (
                SELECT
                    user_pseudo_id,
                    TIMESTAMP_MICROS(event_timestamp) AS event_timestamp
                FROM `team-begamob.{project_id}_CACHED_Events_01.Firebase_Events_USER_ENGAGEMENT`
                WHERE true
                {gbq_filter_return(dict_event_filter, ['event_date', 'country'])}
            ),
            source5 AS (
                SELECT
                    user_pseudo_id,
                    session_number,
                    event_timestamp,
                    flow_row_number,
                    action_name,
                    event_row_in_flow,
                    first_flow_timestamp,
                    MAX(last_flow_timestamp) OVER (PARTITION BY user_pseudo_id, flow_row_number) AS last_flow_timestamp
                FROM source4b
            ),
            identify_last_engagement_event AS (
                SELECT
                    a.user_pseudo_id,
                    a.flow_row_number,
                    MAX(b.event_timestamp) AS last_eng_event_timestamp
                FROM source5 a
                LEFT JOIN engagement b
                    ON a.user_pseudo_id = b.user_pseudo_id
                    AND a.first_flow_timestamp < b.event_timestamp
                    AND b.event_timestamp < a.last_flow_timestamp
                WHERE TIMESTAMP_DIFF(b.event_timestamp, a.first_flow_timestamp, HOUR) < 24
                GROUP BY 1, 2
            ),
            source6 as (
                select
                    a.user_pseudo_id,
                    a.session_number,
                    a.flow_row_number,
                    a.action_name,
                    a.event_row_in_flow,
                    a.event_timestamp,
                    a.first_flow_timestamp first_timestamp,
                    coalesce(
                        last_eng_event_timestamp, 
                        if(last_flow_timestamp = timestamp '2092-02-29', null, last_flow_timestamp)    
                    ) as last_timestamp,
                from source5 a
                left join identify_last_engagement_event b
                    on  a.user_pseudo_id = b.user_pseudo_id
                    and a.flow_row_number = b.flow_row_number
            ),
            """
    else:  # reverse
        if kind == 'drop':
            query_preprocess = f"""
            start_flow AS (
                SELECT
                    user_pseudo_id,
                    event_timestamp AS flow_timestamp,
                    ROW_NUMBER() OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS flow_row_number,
                    LEAD(event_timestamp) OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS following_flow_timestamp
                FROM source
                WHERE CONTAINS_SUBSTR(LOWER(action_name), 'splash')
            ),
            source2 AS (
                SELECT
                    r.*,
                    s.flow_row_number,
                    s.flow_timestamp
                FROM source r
                LEFT JOIN start_flow s
                    ON r.user_pseudo_id = s.user_pseudo_id
                    AND r.event_timestamp BETWEEN s.flow_timestamp AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1)
                    AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1) - s.flow_timestamp > 1*1000000
            ),
            source3 AS (
                SELECT
                    user_pseudo_id,
                    session_number,
                    flow_row_number,
                    action_name,
                    TIMESTAMP_MICROS(event_timestamp) AS event_timestamp,
                    LAG(action_name, 1, '') OVER (PARTITION BY user_pseudo_id, flow_row_number ORDER BY event_timestamp) AS action_name_filter,
                    ROW_NUMBER() OVER (PARTITION BY user_pseudo_id, flow_row_number, action_name ORDER BY event_timestamp) AS row_num_filter
                FROM source2
            ),
            source4 AS (
                SELECT
                    a.user_pseudo_id,
                    a.session_number,
                    a.event_timestamp,
                    a.flow_row_number,
                    a.action_name,
                    ROW_NUMBER() OVER (PARTITION BY a.user_pseudo_id, a.flow_row_number ORDER BY a.event_timestamp desc) AS event_row_in_flow,
                    MIN(a.event_timestamp) OVER (PARTITION BY a.user_pseudo_id, a.flow_row_number) AS first_flow_timestamp,
                    LEAD(a.event_timestamp, 1, TIMESTAMP '2092-02-29') OVER (PARTITION BY a.user_pseudo_id ORDER BY a.event_timestamp) AS last_flow_timestamp
                FROM source3 a
            ),
            engagement AS (
                SELECT
                    user_pseudo_id,
                    session_number,
                    TIMESTAMP_MICROS(event_timestamp) AS event_timestamp
                FROM `team-begamob.cast_glitter_CACHED_Events_01.Firebase_Events_USER_ENGAGEMENT`
                WHERE true
                {gbq_filter_return(dict_event_filter, ['event_date', 'country'])}
            ),
            source5 AS (
                SELECT
                    user_pseudo_id,
                    session_number,
                    event_timestamp,
                    flow_row_number,
                    action_name,
                    event_row_in_flow,
                    first_flow_timestamp,
                    MAX(last_flow_timestamp) OVER (PARTITION BY user_pseudo_id, flow_row_number) AS last_flow_timestamp
                FROM source4
            ),
            identify_last_engagement_event AS (
                SELECT
                    a.user_pseudo_id,
                    a.session_number,
                    a.flow_row_number,
                    MAX(b.event_timestamp) AS last_eng_event_timestamp
                FROM source5 a
                LEFT JOIN engagement b
                    ON a.user_pseudo_id = b.user_pseudo_id
                    AND a.first_flow_timestamp < b.event_timestamp
                    AND b.event_timestamp < a.last_flow_timestamp
                WHERE TIMESTAMP_DIFF(b.event_timestamp, a.first_flow_timestamp, HOUR) < 24
                GROUP BY 1, 2, 3
            ),
            source6 as (
                select
                    a.user_pseudo_id,
                    a.session_number,
                    a.flow_row_number,
                    a.action_name,
                    a.event_row_in_flow,
                    a.event_timestamp,
                    a.first_flow_timestamp first_timestamp,
                    coalesce(
                        last_eng_event_timestamp, 
                        if(last_flow_timestamp = timestamp '2092-02-29', null, last_flow_timestamp)    
                    ) as last_timestamp,
                from source5 a
                left join identify_last_engagement_event b
                    on  a.user_pseudo_id = b.user_pseudo_id
                    and a.flow_row_number = b.flow_row_number
            ),
            """
        elif kind == 'remove':
            query_preprocess = f"""
            last_session as(
                select
                    user_pseudo_id,
                    max(session_number) session_number
                from
                    `team-begamob.{project_id}_CACHED_Events_01.Firebase_Events_APP_REMOVE`
                where true
                {gbq_filter_return(dict_event_filter, ['event_date', 'country'])}
                group by 1
            ),
            source0 as (
                select
                    a.*
                from source a
                inner join last_session b
                    on a.user_pseudo_id = b.user_pseudo_id
                    and a.session_number = b.session_number
            ),
            start_flow AS (
                SELECT
                    user_pseudo_id,
                    event_timestamp AS flow_timestamp,
                    ROW_NUMBER() OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS flow_row_number,
                    LEAD(event_timestamp) OVER (PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS following_flow_timestamp
                FROM source
                WHERE CONTAINS_SUBSTR(LOWER(action_name), 'splash')
            ),
            source2 AS (
                SELECT
                    r.*,
                    s.flow_row_number,
                    s.flow_timestamp
                FROM source r
                LEFT JOIN start_flow s
                    ON r.user_pseudo_id = s.user_pseudo_id
                    AND r.event_timestamp BETWEEN s.flow_timestamp AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1)
                    AND (COALESCE(s.following_flow_timestamp, UNIX_MICROS(CURRENT_TIMESTAMP())) - 1) - s.flow_timestamp > 1*1000000
            ),
            source3 AS (
                SELECT
                    user_pseudo_id,
                    session_number,
                    flow_row_number,
                    action_name,
                    TIMESTAMP_MICROS(event_timestamp) AS event_timestamp,
                    LAG(action_name, 1, '') OVER (PARTITION BY user_pseudo_id, flow_row_number ORDER BY event_timestamp) AS action_name_filter,
                    ROW_NUMBER() OVER (PARTITION BY user_pseudo_id, flow_row_number, action_name ORDER BY event_timestamp) AS row_num_filter
                FROM source2
            ),
            source4 AS (
                SELECT
                    a.user_pseudo_id,
                    a.session_number,
                    a.event_timestamp,
                    a.flow_row_number,
                    a.action_name,
                    ROW_NUMBER() OVER (PARTITION BY a.user_pseudo_id, a.flow_row_number ORDER BY a.event_timestamp desc) AS event_row_in_flow,
                    MIN(a.event_timestamp) OVER (PARTITION BY a.user_pseudo_id, a.flow_row_number) AS first_flow_timestamp,
                    LEAD(a.event_timestamp, 1, TIMESTAMP '2092-02-29') OVER (PARTITION BY a.user_pseudo_id ORDER BY a.event_timestamp) AS last_flow_timestamp
                FROM source3 a
                inner join (
                    select
                        user_pseudo_id,
                        max(flow_row_number) flow_row_number,
                    from source3
                        where flow_row_number is not null
                    group by 1
                ) b
                on a.user_pseudo_id = b.user_pseudo_id
                and a.flow_row_number = b.flow_row_number
                WHERE action_name_filter != action_name
                    AND a.flow_row_number IS NOT NULL
            ),
            engagement AS (
                SELECT
                    user_pseudo_id,
                    session_number,
                    TIMESTAMP_MICROS(event_timestamp) AS event_timestamp
                FROM `team-begamob.cast_glitter_CACHED_Events_01.Firebase_Events_USER_ENGAGEMENT`
                WHERE true
                {gbq_filter_return(dict_event_filter, ['event_date', 'country'])}
            ),
            source5 AS (
                SELECT
                    user_pseudo_id,
                    session_number,
                    event_timestamp,
                    flow_row_number,
                    action_name,
                    event_row_in_flow,
                    first_flow_timestamp,
                    MAX(last_flow_timestamp) OVER (PARTITION BY user_pseudo_id, flow_row_number) AS last_flow_timestamp
                FROM source4
            ),
            identify_last_engagement_event AS (
                SELECT
                    a.user_pseudo_id,
                    a.session_number,
                    a.flow_row_number,
                    MAX(b.event_timestamp) AS last_eng_event_timestamp
                FROM source5 a
                LEFT JOIN engagement b
                    ON a.user_pseudo_id = b.user_pseudo_id
                    AND a.first_flow_timestamp < b.event_timestamp
                    AND b.event_timestamp < a.last_flow_timestamp
                WHERE TIMESTAMP_DIFF(b.event_timestamp, a.first_flow_timestamp, HOUR) < 24
                GROUP BY 1, 2, 3
            ),
            source6 as (
                select
                    a.user_pseudo_id,
                    a.session_number,
                    a.flow_row_number,
                    a.action_name,
                    a.event_row_in_flow,
                    a.event_timestamp,
                    a.first_flow_timestamp first_timestamp,
                    coalesce(
                        last_eng_event_timestamp, 
                        if(last_flow_timestamp = timestamp '2092-02-29', null, last_flow_timestamp)    
                    ) as last_timestamp,
                from source5 a
                left join identify_last_engagement_event b
                    on  a.user_pseudo_id = b.user_pseudo_id
                    and a.flow_row_number = b.flow_row_number
            ),
            """
        else:
            return ""  # Invalid kind for reverse direction


    # Construct the full query
    query = f"""
    {query_preprocess}
    pivot AS (
        SELECT
            user_pseudo_id,
            flow_row_number,
            {gen_query_agg}
        FROM source6
        where true
        {gbq_filter_return(dict_event_filter, ['session_number'])}
        GROUP BY 1, 2
    ),
    time_diff AS (
        SELECT
            user_pseudo_id,
            flow_row_number,
            {gen_query_concat},
            {gen_query_time_diff},
        FROM pivot
    ),
    binned_time AS (
        SELECT
            {gen_query_groupby},
            {gen_query_time_bin},
        FROM time_diff
    ),
    bin_counts AS (
        SELECT
            {gen_query_groupby},
            {gen_query_bin_counts},
        FROM binned_time
        GROUP BY {gen_query_groupby}, {', '.join([f't{i}_bin' for i in range(1, number_node)])}
    )
    SELECT
        *
    FROM bin_counts
    """

    # if direction == 'reverse':
    #     query += f"""
    #     GROUP BY {gen_query_groupby}, {', '.join([f's{i}_bin' for i in range(1, number_node)])}
    #     """

    return query

#Sankey phase
def calculate_grouped_median(group):
    # Remove 'Invalid' bin
    group = group[group['bin'] != 'Invalid']
    
    # Calculate the total count
    total = group['count'].sum()
    
    # If total is 0 after removing 'Invalid', return None
    if total == 0:
        return None
    
    # Calculate the median point
    median_point = total / 2
    
    # Define bin order
    bin_order = ['0s', '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 
                 '10s', '13s', '15s', '17s', '20s', '25s', '30s', '45s', 
                 '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m', '10m', '11m', 
                 '15m', '30m', '45m', '1hr', '2hr', '>2hr']
    
    # Create a category for bin order
    group['bin_order'] = pd.Categorical(group['bin'], categories=bin_order, ordered=True)
    
    # Sort and group by bin
    grouped = group.groupby('bin_order', observed=True)['count'].sum().reset_index()
    grouped = grouped.sort_values('bin_order')
    
    # Find the median bin
    cumulative_sum = 0
    for _, row in grouped.iterrows():
        cumulative_sum += row['count']
        if cumulative_sum >= median_point:
            return row['bin_order']
    
    # If we haven't returned by now, return the last bin
    return bin_order[-1]

COLOR_PALETTE = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
]

def generate_colors(n):
    return [random.choice(COLOR_PALETTE) for _ in range(n)]

def sankey(
    df,
    destination='',
    is_included_Drop_flow=False,
    complexity=1000,
    min_link=3,
    arrangement='snap',
    title='Sankey Diagram'
):
    try:
        # Identify the correct column names
        cat_cols = [col for col in df.columns if col.startswith('s') and col[1:].isdigit()]
        count_cols = [col for col in df.columns if col.endswith('_count')]
        bin_cols = [col for col in df.columns if col.endswith('_bin')]

        if destination:
            def process_row(row):
                destination_found = False
                for i, col in enumerate(cat_cols):
                    if not destination_found:
                        if destination in row[col]:
                            row[col] = destination
                            destination_found = True
                    else:
                        row[col] = 'Drop'
                return row
          
            df = df.apply(process_row, axis=1)
      
        df_view = pd.DataFrame()
        
        for i in range(len(cat_cols) - 1):
            temp_df = df[[cat_cols[i], cat_cols[i+1], count_cols[i], bin_cols[i]]]
            temp_df.columns = ['source', 'target', 'count', 'bin']
            df_view = pd.concat([df_view, temp_df])

        # Group by source and target, then calculate the median bin and total count
        df_grouped = df_view.groupby(['source', 'target']).apply(
            lambda x: pd.Series({
                'count': x['count'].sum(),
                'bin': calculate_grouped_median(x)
            })
        ).reset_index()

        df_grouped = df_grouped[~df_grouped['source'].str.contains('Drop', na=False)]
        df_grouped.loc[df_grouped['target'].str.contains('Drop', na=False), 'target'] = 'Drop'

        # Remove rows where bin is None (this happens when all bins were 'Invalid')
        df_grouped = df_grouped.dropna(subset=['bin'])

        if not is_included_Drop_flow:
            df_grouped = df_grouped[~df_grouped['target'].eq('Drop')]


        df_output = df_grouped[df_grouped['count'] >= min_link]
        df_output = df_output.sort_values(by='count', ascending=False).head(complexity)

        label_list = sorted(set(df_output['source'].tolist() + df_output['target'].tolist()))
        label_dict = {label: i for i, label in enumerate(label_list)}

        df_output['source_id'] = df_output['source'].map(label_dict)
        df_output['target_id'] = df_output['target'].map(label_dict)

        node_colors = generate_colors(len(label_list))

        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "#a3a3a3", width = 1),
            label = label_list,
            color = node_colors,
            hovertemplate = '%{label}<br />Amount: %{value}'
            
        )

        link = dict(
            source = df_output['source_id'].tolist(),
            target = df_output['target_id'].tolist(),
            value = df_output['count'].astype(int).tolist(),
            customdata = df_output['bin'].tolist(),
            # label = [f"{source} → {target}<br>Amount: {int(count)}<br>Median Time: {bin}"
            #          for source, target, count, bin in zip(df_output['source'], df_output['target'], 
            #                                                df_output['count'], df_output['bin'])]
            hovertemplate = '%{source.label} → %{target.label}<br />' +
                            'Amount: %{value} <br />' +
                            'Median time: %{customdata}'
        )

        data = go.Sankey(
            node = node,
            link = link,
            arrangement = arrangement
        )
        
        fig = go.Figure(data)

        fig.update_layout(
            title = {
                'text': title,
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20)
            },
            font_size = 10,
            template = "plotly_dark",
            width=1600, height=900
        )

        return df_grouped, fig, label_list

    except Exception as e:
        print(f"Error in sankey function: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise

def sankey_reverse(
    df,
    splash_screen='splash',
    destination='',
    complexity=1000,
    min_link=3,
    arrangement='snap',
    title='Sankey Diagram'
):
    try:
        # Identify the correct column names
        cat_cols = [col for col in df.columns if col.startswith('s') and col[1:].isdigit()]
        count_cols = [col for col in df.columns if col.endswith('_count')]
        bin_cols = [col for col in df.columns if col.endswith('_bin')]

        # Group all splash screens into the specified splash_screen value
        def transform_splash(value):
            parts = value.split('.')
            if len(parts) == 2 and parts[1].lower().endswith(splash_screen):
                return splash_screen
            return value

        df[cat_cols] = df[cat_cols].map(transform_splash)

        # Remove 'NA' steps
        for col in cat_cols:
            df = df[df[col] != 'NA']

        df_view = pd.DataFrame()
        
        for i in range(len(cat_cols) - 1):
            temp_df = df[[cat_cols[i+1], cat_cols[i], count_cols[i], bin_cols[i]]]  # Reverse order of cat_cols
            temp_df.columns = ['source', 'target', 'count', 'bin']
            df_view = pd.concat([df_view, temp_df])

        # Group by source and target, then calculate the median bin and total count
        df_grouped = df_view.groupby(['source', 'target']).apply(
            lambda x: pd.Series({
                'count': x['count'].sum(),
                'bin': calculate_grouped_median(x)
            })
        ).reset_index()

        # Remove rows where bin is None (this happens when all bins were 'Invalid')
        df_grouped = df_grouped.dropna(subset=['bin'])

        df_output = df_grouped[df_grouped['count'] >= min_link]
        df_output = df_output.sort_values(by='count', ascending=False).head(complexity)

        label_list = sorted(set(df_output['source'].tolist() + df_output['target'].tolist()))
        label_dict = {label: i for i, label in enumerate(label_list)}

        df_output['source_id'] = df_output['source'].map(label_dict)
        df_output['target_id'] = df_output['target'].map(label_dict)

        node_colors = generate_colors(len(label_list))

        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "#a3a3a3", width = 1),
            label = label_list,
            color = node_colors,
            hovertemplate = '%{label}<br />Amount: %{value}'
        )

        link = dict(
            source = df_output['source_id'].tolist(),
            target = df_output['target_id'].tolist(),
            value = df_output['count'].astype(int).tolist(),
            customdata = df_output['bin'].tolist(),
            hovertemplate = '%{source.label} → %{target.label}<br />' +
                            'Amount: %{value} <br />' +
                            'Median time: %{customdata}'
        )

        data = go.Sankey(
            node = node,
            link = link,
            arrangement = arrangement
        )
        
        fig = go.Figure(data)

        fig.update_layout(
            title = {
                'text': title,
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20)
            },
            font_size = 10,
            template = "plotly_dark",
            width=1600, height=900
        )

        return df_grouped, fig, label_list

    except Exception as e:
        print(f"Error in sankey function: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise

# def detail_at_one_node(source_target_df, node):
#     # First, let's check the structure of our DataFrame
#     # print("Columns in source_target_df:", source_target_df.columns)
#     # print("First few rows of source_target_df:")
#     # print(source_target_df.head())

#     # Check if required columns exist
#     required_columns = ['source', 'target', 'count']
#     missing_columns = [col for col in required_columns if col not in source_target_df.columns]
    
#     if missing_columns:
#         raise ValueError(f"The following required columns are missing: {', '.join(missing_columns)}")

#     total_flow_start = source_target_df[source_target_df['target'] == node]['count'].sum()
#     total_flow_end = source_target_df[source_target_df['source'] == node]['count'].sum()

#     if total_flow_start == 0:
#         total_flow_start = total_flow_end

#     df_to = source_target_df[source_target_df['source'] == node][['source','target', 'count']]
#     df_to = df_to.groupby(['source', 'target'])['count'].sum().reset_index().sort_values('count', ascending=False)

#     with np.errstate(divide='ignore'):
#         df_to['%'] = np.round(df_to['count'] * 100 / total_flow_start, 2)

#     df_from = source_target_df[source_target_df['target'] == node][['source','target', 'count']]
#     df_from = df_from.groupby(['source', 'target'])['count'].sum().reset_index().sort_values('count', ascending=False)
    
#     with np.errstate(divide='ignore'):
#         df_from['%'] = np.round(df_from['count'] * 100 / total_flow_start, 2)

#     # Create subplots with 1 row and 2 columns
#     fig = make_subplots(rows=1, cols=2,
#                         subplot_titles=("From node", "To node"),
#                         specs=[[{"type": "table"}, {"type": "table"}]])

#     # Add the table to the first subplot
#     fig.add_trace(
#         go.Table(
#             header=dict(values=['source', 'target', 'count', '%'],
#                         align='center'),
#             cells=dict(values=[df_from['source'], df_from['target'], df_from['count'], df_from['%']],
#                        align=['left', 'left', 'right', 'right'],
#                        fill_color='rgba(37,39,41,50)',
#                        height=24)),
#         row=1, col=1
#     )

#     # Add the table to the second subplot
#     fig.add_trace(
#         go.Table(
#             header=dict(values=['source', 'target', 'count', '%'],
#                         align='center'),
#             cells=dict(values=[df_to['source'], df_to['target'], df_to['count'], df_to['%']],
#                        align=['left', 'left', 'right', 'right'],
#                        fill_color='rgba(37,39,41,50)',
#                        height=24)),
#         row=1, col=2
#     )

#     # Update layout for better presentation
#     fig.update_layout(
#         title={
#             'text': f"Detail at node: {node}",
#             'y': 0.95,
#             'x': 0.5,
#             'xanchor': 'center',
#             'yanchor': 'top',
#             'font': dict(size=24)
#         },
#         template="plotly_dark"
#     )

#     return fig

def sankey(
    df,
    direction='forward',
    splash_screen='splash',
    destination='',
    is_included_Drop_flow=True,
    complexity=1000,
    min_link=3,
    arrangement='snap',
    title='Sankey Diagram'
):
    try:
        # Identify the correct column names
        cat_cols = [col for col in df.columns if col.startswith('s') and col[1:].isdigit()]
        count_cols = [col for col in df.columns if col.endswith('_count')]
        bin_cols = [col for col in df.columns if col.endswith('_bin')]

        # Group all splash screens into the specified splash_screen value
        def transform_splash(value):
            parts = value.split('.')
            if len(parts) == 2 and parts[1].lower().endswith(splash_screen):
                return f"{parts[0]}.{splash_screen}"
            return value

        for col in cat_cols:
            df[col] = df[col].map(transform_splash)

        # Remove 'NA' steps
        for col in cat_cols:
            df = df[df[col] != 'NA']

        if destination and direction == 'forward':
            def process_row(row):
                destination_found = False
                for i, col in enumerate(cat_cols):
                    if not destination_found:
                        if destination in row[col]:
                            row[col] = destination
                            destination_found = True
                    else:
                        row[col] = 'Drop'
                return row
            
            df = df.apply(process_row, axis=1)

        df_view = pd.DataFrame()
        
        for i in range(len(cat_cols) - 1):
            if direction == 'forward':
                temp_df = df[[cat_cols[i], cat_cols[i+1], count_cols[i], bin_cols[i]]]
            else:
                temp_df = df[[cat_cols[i+1], cat_cols[i], count_cols[i], bin_cols[i]]]
            temp_df.columns = ['source', 'target', 'count', 'bin']
            df_view = pd.concat([df_view, temp_df])

        # Group by source and target, then calculate the median bin and total count
        df_grouped = df_view.groupby(['source', 'target']).apply(
            lambda x: pd.Series({
                'count': x['count'].sum(),
                'bin': calculate_grouped_median(x)
            })
        ).reset_index()

        if direction == 'forward':
            df_grouped = df_grouped[~df_grouped['source'].str.contains('Drop', na=False)]
            df_grouped.loc[df_grouped['target'].str.contains('Drop', na=False), 'target'] = 'Drop'
            if not is_included_Drop_flow:
                df_grouped = df_grouped[~df_grouped['target'].eq('Drop')]
        else:
            if not is_included_Drop_flow:
                df_grouped = df_grouped[~df_grouped['source'].eq('Drop')]

        # Remove rows where bin is None (this happens when all bins were 'Invalid')
        df_grouped = df_grouped.dropna(subset=['bin'])

        df_output = df_grouped[df_grouped['count'] >= min_link]
        df_output = df_output.sort_values(by='count', ascending=False).head(complexity)

        label_list = sorted(set(df_output['source'].tolist() + df_output['target'].tolist()))
        label_dict = {label: i for i, label in enumerate(label_list)}

        df_output['source_id'] = df_output['source'].map(label_dict)
        df_output['target_id'] = df_output['target'].map(label_dict)

        node_colors = generate_colors(len(label_list))

        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "#a3a3a3", width = 1),
            label = label_list,
            color = node_colors,
            hovertemplate = '%{label}<br />Amount: %{value}'
        )

        link = dict(
            source = df_output['source_id'].tolist(),
            target = df_output['target_id'].tolist(),
            value = df_output['count'].astype(int).tolist(),
            customdata = df_output['bin'].tolist(),
            hovertemplate = '%{source.label} → %{target.label}<br />' +
                            'Amount: %{value} <br />' +
                            'Median time: %{customdata}'
        )

        data = go.Sankey(
            node = node,
            link = link,
            arrangement = arrangement
        )
        
        fig = go.Figure(data)

        fig.update_layout(
            title = {
                'text': title,
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20)
            },
            font_size = 10,
            template = "plotly_dark",
            width=1600, height=900
        )

        return df_grouped, fig, label_list

    except Exception as e:
        print(f"Error in sankey function: {str(e)}")
        print(traceback.format_exc())
        raise



def detail_at_one_node(source_target_df, node):
    # Check if required columns exist
    required_columns = ['source', 'target', 'count', 'bin']
    missing_columns = [col for col in required_columns if col not in source_target_df.columns]
    
    if missing_columns:
        raise ValueError(f"The following required columns are missing: {', '.join(missing_columns)}")

    # Calculate total flows
    total_flow_start = source_target_df[source_target_df['target'] == node]['count'].sum()
    total_flow_end = source_target_df[source_target_df['source'] == node]['count'].sum()

    if total_flow_start == 0:
        total_flow_start = total_flow_end

    # Process flows to the node
    df_to = source_target_df[source_target_df['source'] == node][['source', 'target', 'count', 'bin']]
    df_to = df_to.groupby(['source', 'target', 'bin'])['count'].sum().reset_index().sort_values('count', ascending=False)

    with np.errstate(divide='ignore'):
        df_to['%'] = np.round(df_to['count'] * 100 / total_flow_start, 2)

    # Process flows from the node
    df_from = source_target_df[source_target_df['target'] == node][['source', 'target', 'count', 'bin']]
    df_from = df_from.groupby(['source', 'target', 'bin'])['count'].sum().reset_index().sort_values('count', ascending=False)
    
    with np.errstate(divide='ignore'):
        df_from['%'] = np.round(df_from['count'] * 100 / total_flow_start, 2)

    # Create subplots with 1 row and 2 columns
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=(f"From node (Total: {total_flow_start})", 
                                      f"To node (Total: {total_flow_end})"),
                        specs=[[{"type": "table"}, {"type": "table"}]])

    # Add the table for flows from other nodes
    fig.add_trace(
        go.Table(
            header=dict(values=['Source', 'Target', 'Count', '%', 'Median Time'],
                       align='center',
                       font=dict(size=12, color='white')),
            cells=dict(values=[df_from['source'], 
                             df_from['target'],
                             df_from['count'],
                             df_from['%'],
                             df_from['bin']],
                      align=['left', 'left', 'right', 'right', 'center'],
                      fill_color='rgba(37,39,41,50)',
                      font=dict(size=11),
                      height=24)),
        row=1, col=1
    )

    # Add the table for flows to other nodes
    fig.add_trace(
        go.Table(
            header=dict(values=['Source', 'Target', 'Count', '%', 'Median Time'],
                       align='center',
                       font=dict(size=12, color='white')),
            cells=dict(values=[df_to['source'],
                             df_to['target'],
                             df_to['count'],
                             df_to['%'],
                             df_to['bin']],
                      align=['left', 'left', 'right', 'right', 'center'],
                      fill_color='rgba(37,39,41,50)',
                      font=dict(size=11),
                      height=24)),
        row=1, col=2
    )

    # Update layout for better presentation
    fig.update_layout(
        title={
            'text': f"Detail at node: {node}",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=24)
        },
        template="plotly_dark",
        height=800  # Increased height to accommodate the additional column
    )

    return fig

def filter_by_prefix(data_list, n):
    if not isinstance(data_list, list) or not isinstance(n, int):
        return ""  # Handle invalid input

    if not data_list:  # Handle empty input list
        return ""
        
    prefix = str(n) + "."

    filtered_list = [item for item in data_list if isinstance(item, str) and item.startswith(prefix) and (len(item) == len(prefix) or item[len(prefix)] != '.')]

    return ", ".join(filtered_list)
