from setuptools import setup, find_packages

setup(
    name='saate_matne',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['colorama', 'datetime'],
    description='A library for formatted time display in English and Persian with Night and Day themes',
    author='Fared Baktash',
    author_email='faredba@outlook.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)