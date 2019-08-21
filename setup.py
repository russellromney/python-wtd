from setuptools import setup, find_packages


setup(
    name = 'python-wtd',
    version = '0.1.3',
    description = 'Python wrapper for World Trading Data API',
    keywords = ' python finance trading stocks prices worldtradingdata wtd alphavantage iex',
    url = 'https://github.com/russellromney/python-wtd',
    download_url = 'https://github.com/russellromney/python-wtd/archive/v0.1.3.tar.gz',
    author = 'Russell Romney',
    author_email = 'russellromney@gmail.com',
    license = 'MIT',
    packages = find_packages(),
    install_requires = [
        'pandas',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    include_package_data = False,
    zip_safe = False
)
