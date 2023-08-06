from setuptools import find_packages, setup

setup(
    name='adversarial-test',
    packages=find_packages(),
    version='0.1.0',
    description='Adversarial test for tabular data',
    author='TuHM',
    install_requires=[
        "numpy",
        "sklearn",
        "pandas"
    ],
    tests_require=[
        "unittest",
        "catboost"
    ]
    # license='MIT',
)