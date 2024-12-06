import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README_pypi = (HERE / "README_pypi.md").read_text()

requires = ["numpy", "matplotlib", "scipy", "tqdm"]

# This call to setup() does all the work
setup(
    name="CI_methods_analyser",
    version="1.1.0.post1",
    description="Analyse efficacy of your own confidence interval (CI) methods",

    long_description=README_pypi,
    long_description_content_type="text/markdown",

    url="https://github.com/Kukuster/CI_methods_analyser",

    author="Kukuster",
    author_email="KukusterMOP@gmail.com",
    license="MIT",
    # classifiers=[
    #     "License :: OSI Approved :: MIT License",
    #     "Programming Language :: Python :: 3",
    #     "Programming Language :: Python :: 3.7",
    # ],

    packages=['CI_methods_analyser'],
    setup_requires=requires,
    install_requires=requires,

    include_package_data=True,
    # entry_points={
    #     "console_scripts": [
    #         "realpython=reader.__main__:main",
    #     ]
    # },
)
