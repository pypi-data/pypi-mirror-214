from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="basic_task_manager",
    version="1.0.0",
    author="GautamSagarMallela",
    description="A task manager application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["basic_task_manager"],
)
