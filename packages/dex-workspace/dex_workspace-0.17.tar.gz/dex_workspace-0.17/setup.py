# setup.py
from setuptools import setup, find_packages

setup(
    name="dex_workspace",
    version="0.17",
    packages=find_packages(),
    requires=[
        'cloudpickle', 
        'psutils', 
        'requests', 
        'remdex', 
        'fastapi', 
        'uvicorn', 
    ], 
    entry_points={
        "console_scripts": [
            "dex_workspace = dex_workspace.__main__:main",
        ],
    },
    include_package_data=True, 
)
