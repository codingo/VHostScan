""" __Doc__ File handle class """
from setuptools import find_packages, setup
from VHostScan.lib.core.__version__ import __version__


def dependencies(imported_file):
    """ __Doc__ Handles dependencies """
    with open(imported_file) as file:
        return file.read().splitlines()


with open("README.md") as file:
    try:
        NUM_INSTALLED = True
    except ImportError:
        NUM_INSTALLED = False
    setup(
        name="VHostScan",
        license="GPLv3",
        description="A virtual host scanner that performs reverse lookups, "
                    "can be used with pivot tools, detect catch-all"
                    "scenarios, aliases and dynamic default pages.",
        long_description=file.read(),
        author="codingo",
        version=__version__,
        author_email="codingo@protonmail.com",
        url="http://github.com/codingo/VHostScan",
        packages=find_packages(exclude=('tests')),
        package_data={'VHostScan': ['*.txt']},
        entry_points={
            'console_scripts': [
                'VHostScan = VHostScan.VHostScan:main'
            ]
        },
        install_requires=dependencies('requirements.txt'),
        setup_requires=['pytest-runner',
                        '' if num_installed else 'numpy==1.12.0'],
        tests_require=dependencies('test-requirements.txt'),
        include_package_data=True)
