from setuptools import setup, find_packages

setup(
    name='mycoinlib',
    version='0.6',
    packages=find_packages('mycoinlib'),
    install_requires=[
        'bitcoinlib',
        'blockcypher',
        'requests',
        'eth_account',

    ]
)
