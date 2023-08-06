from setuptools import setup, find_packages

setup(
    name='math_calculator',
    version='1.0.0',
    author='Your Name',
    author_email='hassenmnejja1@gmail.com',
    description='A simple math calculator package',
    long_description='A package that provides basic math calculations',
    url='https://gitlab.com/hassen_mnejja/math_calculator',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'emoji',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

