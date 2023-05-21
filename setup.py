from setuptools import setup, find_packages

setup(
    name="bsdl",
    version='0.0.0',
    packages=find_packages(),
    include_package_data=True,
    author="adithayyil",
    install_requires=[
        "click",
        "halo",
        "mutagen"
    ],
    entry_points={
        "console_scripts": [
            "bsdl = bsdl.bsdl:main",
        ],
    }
)
