from setuptools import setup, find_packages

setup(
    name='fastapienv',
    version='1.0.1',
    description='A Python module that creates a Python environment and generates FastAPI boilerplate code.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Gautam Sagar Mallela',
    author_email='gautamsagar.mallela99@gmail.com',
    keywords='python module fastapi boilerplate',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'fastapienv = fastapienv.main:main',
        ],
    },
)
