from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()
setup(
    name="pgqmini",
    version="0.0.4",
    description="pgqmini is a lightweight, easy-to-use Python library for managing PostgreSQL message queues.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/over-engineers/pgqmini",
    author="Kajago",
    author_email="jangsc0000@gmail.com",
    license="MIT",
    packages=["pgqmini"],
    zip_safe=False,
    install_requires=["psycopg2-binary"],
)
