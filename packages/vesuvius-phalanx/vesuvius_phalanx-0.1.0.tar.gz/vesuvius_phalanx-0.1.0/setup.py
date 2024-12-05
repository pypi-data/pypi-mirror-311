from setuptools import setup, find_packages

setup(
    name='phalanx',
    version='0.1.0',
    author="Marcel Roth",
    author_email="marcelroth100@aol.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mvrcii/phalanx",
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'tqdm',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'phalanx=phalanx.cli:cli',
        ],
    },
    python_requires=">=3.8",
)
