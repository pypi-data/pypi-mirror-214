from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Configure setup
setup(
    name='cryptofusepy',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Silenttttttt',
    author_email='cryptofuse.net@gmail.com',
    description='Python library for interacting with the CryptoFuse API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='cryptofuse cryptocurrency cryptoswap swap crypto',
    entry_points={
        'console_scripts': [
            'cryptofusepy = cryptofusepy.client:CryptoFuseClient',
        ],
    },
    project_urls={
        'Source Code': 'https://github.com/Os-brod/CryptoFusepy',
        # You can add more links here if needed,
        # for example, documentation, issue tracker, etc.
    }
)
