from setuptools import setup

setup(
    name="he",
    version="1.0",
    packages=["he"],
    # py_modules=["he", 'colors'],
    include_package_data=True,
    install_requires=[
        "click",
        # Colorama is only required for Windows.
        "colorama",
        "sh",
        "jsonpickle",
        "prettytable"
    ],
    entry_points="""
        [console_scripts]
        he=he.he:cli
    """,
)
