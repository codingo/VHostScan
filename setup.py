""" __Doc__ File handle class """
import os
from setuptools import find_packages, setup


def get_version():
    """Get version from __version__.py file"""
    version_file = os.path.join(
        os.path.dirname(__file__), 
        'VHostScan', 'lib', 'core', '__version__.py'
    )
    
    version_vars = {}
    with open(version_file, encoding='utf-8') as f:
        exec(f.read(), version_vars)
    
    return version_vars['__version__']


def dependencies(imported_file):
    """ __Doc__ Handles dependencies """
    with open(imported_file, encoding='utf-8') as file:
        return file.read().splitlines()


with open("README.md", encoding='utf-8') as file:
    setup(
        name="VHostScan",
        license="GPLv3",
        description="A virtual host scanner that performs reverse lookups, "
                    "can be used with pivot tools, detect catch-all "
                    "scenarios, aliases and dynamic default pages.",
        long_description=file.read(),
        long_description_content_type="text/markdown",
        author="codingo",
        version=get_version(),
        author_email="codingo@protonmail.com",
        url="https://github.com/codingo/VHostScan",
        packages=find_packages(exclude=('tests',)),
        package_data={'VHostScan': ['*.txt', 'wordlists/*.txt', 'lib/*.txt']},
        entry_points={
            'console_scripts': [
                'VHostScan = VHostScan.VHostScan:main'
            ]
        },
        install_requires=dependencies('requirements.txt'),
        tests_require=dependencies('test-requirements.txt'),
        include_package_data=True,
        python_requires=">=3.8",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Topic :: Security",
            "Topic :: System :: Networking",
        ],
    )
