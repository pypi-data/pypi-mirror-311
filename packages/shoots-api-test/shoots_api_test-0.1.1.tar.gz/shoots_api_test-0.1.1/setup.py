from setuptools import setup, find_packages

setup(
    name='shoots-api-test',
    version='0.1.1',
    author='j3ssie-bd',
    author_email='ho.jessie@bytedance.com',
    description='A simple project that act as a placeholder for project name',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'shoots-api-test=shoots_api_test:shoots_api_test',
        ],
    },
)