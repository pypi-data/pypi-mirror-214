from setuptools import setup, find_packages

setup(
    name='FRANECpy',
    readme = "README.md",
    version = '1.0.0',
    author='Francesco Turini',
    author_email='fturini.turini7@gmail.com',
    description='A simple library for help in the data analysis of FRANEC simulation.',
    url='https://github.com/fturini98/FRANECpy',
    license='GNU General Public License (GPL)',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'ipython',
        'matplotlib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
    ],
)