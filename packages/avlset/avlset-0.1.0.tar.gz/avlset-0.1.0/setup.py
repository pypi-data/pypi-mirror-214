from setuptools import setup, find_packages

setup(
    name='avlset',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Gabe Rust',
    author_email='gabe@rekt.run',
    description='An AVL tree set implementation in Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
