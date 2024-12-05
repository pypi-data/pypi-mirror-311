from setuptools import setup, find_packages

setup(
    name='maya_rabbitmq_package',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'pika',
    ],
    author='Asifaa Sulthana',
    author_email='asifaa_sulthanan@trimble.com',
    description='A package for handling RabbitMQ operations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Trimble-Construction/project-maya/tree/dev/Cloud/RabbitmqHandler',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)