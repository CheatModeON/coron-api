from setuptools import setup, find_packages

requires = [
    'requests',
    'flask',
    'bs4',
    'HTMLParser'
]

setup(
    name='coron-api',
    version='0.1',
    description='Flask api',
    author='Achilleas Papakonstantinou',
    author_email='achipap@hotmail.com',
    keywords='coronavirus api',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
