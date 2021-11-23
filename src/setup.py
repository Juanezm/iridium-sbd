from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='wmts_extractor',
    packages=['iridium_sbd'],
    python_requires='>=3.7, <4',
    install_requires=required,
    entry_points={
        'console_scripts': ['iridium-sbd=iridium_sbd.cli:cli'],
    }
)
