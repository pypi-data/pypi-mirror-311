from setuptools import setup, find_packages

setup(
    name="soufflesankey",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'plotly',
        'pandas',
        'numpy'
    ],
    author="Souffle2",  # From your config.py admin value
    author_email="0229gnoliah@gmail.com",  # You'll need to add this
    description="A Python package for creating Sankey diagrams with a focus on mobile app analytics",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/S0uffle/soufflesankey",  # You'll need to add this
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
