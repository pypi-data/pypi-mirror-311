from setuptools import setup, find_packages

short_description = ("A simple package to run a ReAct agent with Ollama and tools with privileges "
                     "to run code inside a docker container.")
# Read the contents of your README file
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = short_description

setup(
    name="pyreact-agent",  # Replace with your package name
    version="0.1.0",  # Replace with your version
    author="Cody Maughan",  # Replace with your name
    author_email="codyamaughan@gmail.com",  # Replace with your email
    description=short_description,  # Replace with a short description
    long_description=long_description,
    long_description_content_type="text/markdown",  # Optional (if README is in Markdown)
    url="",  # Replace with your GitHub or project URL
    packages=find_packages(),  # Automatically find packages in your directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Replace with your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",  # Specify the Python version your package supports
    install_requires=[
        "requests", "pydantic", "docker"
    ],
    include_package_data=True,  # Include files from MANIFEST.in
)
