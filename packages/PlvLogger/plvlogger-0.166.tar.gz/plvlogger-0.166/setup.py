from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='PlvLogger',
    version='0.166',
    packages=find_packages(),
    description='add Singleton',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='plv88',
    author_email='plv.andrey88@gmail.com',
    url='https://github.com/plv88/MyLogger',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
