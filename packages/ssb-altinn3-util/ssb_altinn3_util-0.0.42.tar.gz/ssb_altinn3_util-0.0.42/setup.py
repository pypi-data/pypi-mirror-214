import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssb_altinn3_util",
    version="0.0.42",
    author="Team Cumulus",
    author_email="nhk@ssb.no, lrb@ssb.no, gij@ssb.no, rsa@ssb.no",
    description="A small library package containing various tools and utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/statisticsnorway/ssb-altinn3-util",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_data={"": ["py.typed"]},
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'fastapi',
        'google-cloud-pubsub',
        'google-cloud-secret-manager',
        'pydantic',
        'sqlalchemy',
        'sqlalchemy-spanner',
        'pg8000',
        'cloud-sql-python-connector[pg8000]',
        'python-json-logger',
        'defusedxml',
        'opentelemetry-exporter-gcp-trace',
        'opentelemetry-propagator-gcp',
        'opentelemetry-instrumentation',
        'opentelemetry-instrumentation-logging'
    ],

    python_requires=">=3.6",
)
