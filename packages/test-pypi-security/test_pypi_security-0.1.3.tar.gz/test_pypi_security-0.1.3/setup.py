from setuptools import setup

setup(
    name='test_pypi_security',
    version='0.1.3',
    author='Arthur Le Floch',
    author_email='alf.github@gmail.com',
    description='Test of PyPI security',
    long_description='Test of PyPI security, do not use this package blindly, it deletes a folder called delete_me in the current directory',
    url='https://github.com/ArthurLeFloch/',
    packages=[''],
    package_dir={'': 'src'},
    install_requires=[
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
