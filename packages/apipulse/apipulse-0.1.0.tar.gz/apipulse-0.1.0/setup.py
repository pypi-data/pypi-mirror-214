import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def read(f):
    with open(f, 'r', encoding='utf-8') as file:
        return file.read()


setup(
    name='apipulse',
    version='0.1.0',
    packages=['apipulse'],
    include_package_data=True,
    license='MIT',
    description='Universal test framework to test REST API',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/quillcraftsman/apipulse',
    author='quillcraftsman',
    author_email='quill@craftsman.lol',
    keywords=['test', 'api', 'framework', 'rest'],
    python_requires='>=3',
)
