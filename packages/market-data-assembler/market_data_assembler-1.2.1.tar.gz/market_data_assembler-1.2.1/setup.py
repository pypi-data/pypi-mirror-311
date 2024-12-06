from setuptools import setup, find_packages

setup(
    name='market-data-assembler',
    version='1.2.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'tenacity',
        'pytz',
        'pyarrow',
        'pandas'
    ],
    author='Maksym Usanin (usanin.max@gmail.com)',
    description='Market data provider',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
