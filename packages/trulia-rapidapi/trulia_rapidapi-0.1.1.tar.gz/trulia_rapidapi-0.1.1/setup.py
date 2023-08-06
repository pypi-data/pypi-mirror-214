from setuptools import setup

setup(
    name='trulia_rapidapi',
    version='0.1.1',
    description='Trulia Real Estate API on RapidAPI',
    packages=['trulia_rapidapi', 'trulia_rapidapi.src', 'trulia_rapidapi.src.trulia_models'],
    author_email='hello@letsscrape.com',
    zip_safe=False,
    author='LetsScrape',
    keywords=['trulia', 'real estate api', 'trulia real estate', 'trulia api', 'parsing', 'scraper'],
    classifiers=[],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://letsscrape.com/scrapers/trulia-real-estate-api/',
)
