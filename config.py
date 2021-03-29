from setuptools import setup, find_packages

requires = [
    'flask',
    'spotipy',
    'html5lib',
    'requests',
    'requests_html',
    'beautifulsoup4',
    'pathlib',
    'pandas',
]

setup(
    name='SpotifyProject',
    version='1.0',
    description='College thesis project - Machine learning and data analysis using the Million Song Playlist dataset to create a custom recommended songs playlist for the user',
    author='Dylan Hannon',
    keywords='web flask',
    packages=find_packages(),
    include_package_data='True',
    install_requires=requires

)

