from setuptools import setup

setup(
    name='cc_dwh_streaming_pkg',
    version='1.0.2',
    description='serving CC dwh streaming apps',
    author='Asaf Shelach',
    packages=['cc_dwh_streaming_pkg'],
    install_requires=[
        'pyspark',
        'argparse'
    ],
)
