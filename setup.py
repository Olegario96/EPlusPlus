from setuptools import find_packages, setup

setup(
    name='eplusplus',
    packages=find_packages(),
    entry_points={
        'gui_scripts': [
            'eplusplus = eplusplus.__main__:run'
        ],
    },
    install_requires=[
        'pyDOE',
        'PyQt5'
    ],
)
