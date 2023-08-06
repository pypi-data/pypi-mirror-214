from setuptools import setup, find_packages

setup(
    name="gpt_heat_routes",
    version="0.1",
    packages=find_packages(),
    url='https://github.com/ChristoGH/gpt_heat_routes', # Add your package's URL here
    author='Christo Strydom', # Add your name here
    author_email='christo.w.strydom@gmail.com', # Add your email here
    install_requires=[
        "numpy",
        "networkx",
        "osmnx",
        "pandas",
        "branca",
        "matplotlib",
        "folium",
        "copy",
    ],
)
