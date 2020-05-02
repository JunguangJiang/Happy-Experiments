from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hepy",
    version="0.0.1",
    author="Junguang Jiang",
    description="A tool to manage experiment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JunguangJiang/Happy-Experiments/settings",
    packages=["he"],
    # py_modules=["he", 'colors'],
    include_package_data=True,
    install_requires=[
        "click",
        # Colorama is only required for Windows.
        "colorama",
        "sh",
        "jsonpickle",
        "prettytable",
        "pandas"
    ],
    entry_points="""
        [console_scripts]
        he=he.he:cli
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
