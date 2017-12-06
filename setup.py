from setuptools import find_packages, setup
from VHostScan.lib.core.__version__ import __version__


def dependencies(file):
    with open(file) as f:
        return f.read().splitlines()


with open("README.md") as f:
    try:
        import numpy
        num_installed = True
    except ImportError:
        num_installed = False
    setup(
        name="VHostScan",
        license="GPLv3",
        description="A virtual host scanner that performs reverse lookups, "
                    "can be used with pivot tools, detect catch-all"
                    "scenarios, aliases and dynamic default pages.",
        long_description=f.read(),
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
