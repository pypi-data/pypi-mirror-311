from setuptools import setup, find_packages

setup(
    name='dtep-test',
    version='1.0.0',
    packages=find_packages(),
    description='The tool to execute tests in ICDC context',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sheick Ali',
    author_email='',
    url='https://github.com/sheicky/dtep-package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],
)