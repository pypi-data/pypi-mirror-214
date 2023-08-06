from setuptools import setup, find_packages


setup(
    name='terminal_plus',
    version='1.0.0.dev0',
    author='ali',
    author_email='lynali@gmail.com',
    description='print plus',
    package_dir={"":"src"},
    packages=find_packages('src'),
    python_requires=">=3.7.0"
)