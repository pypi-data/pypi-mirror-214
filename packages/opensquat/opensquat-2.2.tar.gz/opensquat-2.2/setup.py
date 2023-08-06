from setuptools import setup

setup(
    name='opensquat',
    version='2.2',
    description='The openSquat is a tool for detecting phishing domains and domain squatting.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/atenreiro/opensquat',
    author='Andre Tenreiro',
    author_email='andre@opensquat.com',
    license='GPLv3',
    install_requires=[
        'strsimpy',
        'confusable_homoglyphs',
        'homoglyphs',
        'colorama',
        'requests',
        'numpy',
        'pytest',
        'pytest-cov',
        'codecov',
        'coverage',
        'black',
        'flake8',
        'beautifulsoup4',
        'dnspython',
        'packaging',
    ],
    packages=[
        'opensquat',
        'tests',
    ],
)
