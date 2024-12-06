from setuptools import setup, find_packages

setup(
    name='aetosky_job_processing',
    version='1.0.3',
    packages=find_packages(),
    install_requires=[
        "requests",
        "aiohttp",
    ],
)