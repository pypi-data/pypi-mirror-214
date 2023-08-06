from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ghostpip',
    version='1.1.1',
    author='Mohammad Alamin',
    author_email='akxvau@gmail.com',
    description='A Python module for interacting with the ghost.toxinum.xyz API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/illusionghost3/ghostpip',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='ghostpip api module',
    license='MIT',
)
