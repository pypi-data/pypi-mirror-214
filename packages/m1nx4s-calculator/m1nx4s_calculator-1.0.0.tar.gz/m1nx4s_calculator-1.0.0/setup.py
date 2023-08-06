import setuptools
setuptools.setup(
    name='m1nx4s_calculator',
    author='Mindaugas Kancevicius',
    description='my first calculator package',
    long_description='A much longer explanation of the project and helpful resources',
    url='https://github.com/m1nx4s/calculator',
    keywords='development, setup, setuptools',
    python_requires='>=3.7, <4',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src')
)