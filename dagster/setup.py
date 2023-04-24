from setuptools import find_packages, setup

setup(
    name="orchestrator",
    packages=find_packages(exclude=["orchestrator_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "sqlalchemy",
        "pycopg2-binary",
        "garminconnect",
        "requests",
        "cloudscraper",
        "minio"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
