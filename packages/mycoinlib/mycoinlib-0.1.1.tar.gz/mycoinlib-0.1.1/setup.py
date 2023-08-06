from setuptools import setup, find_packages

setup(
    name='mycoinlib',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'bitcoinlib',
        'blockcypher',
        'requests',
        'eth_account',

    ]
)
