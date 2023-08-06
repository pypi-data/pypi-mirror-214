from setuptools import setup

setup(
    name="pgqmini",
    version="0.0.2",
    description="pgqmini is a lightweight, easy-to-use Python library for managing PostgreSQL message queues.",
    url="http://github.com/over-engineers/pgqmini",
    author="Kajago",
    author_email="jangsc0000@gmail.com",
    license="MIT",
    packages=["pgqmini"],
    zip_safe=False,
    install_requires=["psycopg2-binary"],
)
