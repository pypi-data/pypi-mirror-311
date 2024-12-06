from setuptools import setup, find_packages
import os

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

def readme():
    rst_text = read_md('README.md')
    with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'w+') as f:
        f.write(rst_text)

setup(
    name='dynmap_lens',
    version='1.0.0',
    description='Capture the contents of a Minecraft server\'s Dynmap. (Fork of dynmap_timemachine.)',
    long_description='This package captures the contents of a Minecraft server\'s Dynmap page; fork of dynmap_timemachine with added support for JPG tile formats.',
    long_description_content_type='text/plain',
    url='https://github.com/martinsik/minecraft-dynmap-timemachine',
    # Note: This package is based on the work of Martin Sikora's dynmap_timemachine.
    # https://github.com/martinsik/minecraft-dynmap-timemachine/
    author='AtomicAirin',
    author_email='',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        'Topic :: Games/Entertainment',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Utilities',
    ],
    install_requires=[
        'Pillow',
        'requests',
    ],
    tests_require=[
        'nose',
    ],
    scripts=['dynmap-lens.py'],
    test_suite='tests',
)
