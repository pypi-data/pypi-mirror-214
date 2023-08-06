from setuptools import setup, find_packages

setup(
    name='the-one-sdk',
    version='0.1.0',
    description="LOTR SDK for interacting with the Lord of the Rings API",
    author='Olayiwola Ayoola',
    author_email='olusameze@email.com',
    packages=find_packages(),
    install_requires=[
        'requests',  # Example dependency
    ],
)
