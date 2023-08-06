from setuptools import setup
import setuptools
setup(
    name="bcdup",
    version='2.2',
    author="CintagramABP",
    description="BCSFE_Python personal api",
    long_description="BCSFE_Python personal api",
    url="",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "colored==1.4.4",
        "tk",
        "python-dateutil",
        "requests",
        "pyyaml",
        "aiohttp",
        "bcsfe-discord"
    ],
    include_package_data=True,
    extras_require={
        "testing": [
            "pytest",
            "pytest-cov",
        ],
    },
    package_data={"bc_acc_dup": ["py.typed"]},
    flake8={"max-line-length": 160},
)
