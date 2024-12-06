from setuptools import setup, find_packages

setup(
    name='debug_sys',
    version='3.4.6',
    packages=find_packages(),
    description='A simple module to debug Python code',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Cuisset Mattéo',
    author_email='matteo.cuisset@gmail.com',
    url='https://github.com/Flyns157/debug_sys',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires=open('requirements.txt').read().splitlines(),
)
