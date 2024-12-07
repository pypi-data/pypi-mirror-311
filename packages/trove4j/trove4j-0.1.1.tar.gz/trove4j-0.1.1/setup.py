from setuptools import setup, find_packages

setup(
    name='trove4j',
    version='0.1.1',
    author='j3ssie-bd',
    author_email='ho.jessie@bytedance.com',
    description='A simple project that act as a placeholder for project name',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'trove4j=trove4j:trove4j',
        ],
    },
)