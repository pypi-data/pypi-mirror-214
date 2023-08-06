from setuptools import setup, find_packages

setup(
    name='Cashooo',
    version='1.1.0',
    description='Custom errors and middlewares',
    author='yash ',
    author_email='yash.m@royalecheese.com',
    packages=find_packages(),
    install_requires=[
        'Django>=3.2',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
)
