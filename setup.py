from setuptools import find_packages, setup


def dependencies(file):
    with open(file) as f:
        return f.read().splitlines()

with open("README.md") as f:
    setup(
        name="VHostScan",
        license="GPLv3",
        description="A virtual host scanner that performs reverse lookups, "
                    "can be used with pivot tools, detect catch-all"
                    "scenarios, aliases and dynamic default pages.",
        long_description=f.read(),
        author="codingo",
        author_email="codingo@protonmail.com",
        url="http://github.com/codingo/VHostScan",
        packages=find_packages(exclude=('tests')),
        scripts=['VHostScan.py'],
        install_requires=dependencies('requirements.txt'),
        tests_require=dependencies('test-requirements.txt'),
        include_package_data=True)
