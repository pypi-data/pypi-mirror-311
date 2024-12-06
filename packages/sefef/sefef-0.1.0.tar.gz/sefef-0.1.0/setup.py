from setuptools import setup, find_packages


with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name='sefef',
    version='0.1.0',
    license="BSD 3-clause",
    description='SeFEF: Seizure Forecast Evaluation Framework',
    readme="README.rst",
    author="Ana Sofia Carmo",
    author_email="anascacais@gmail.com",
    packages=find_packages(include=['sefef', 'sefef.*']),
    install_requires=required,
    setup_requires=['pytest-runner', 'flake8'],
    test_suite="tests",
    tests_require=['pytest'],
)
