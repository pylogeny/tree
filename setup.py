from setuptools import setup, find_packages


setup(
    name='pylotree',
    version='0.2.0',
    license='Apache 2.0',
    description='Distance-based cluster methods for linguistic phylogenies',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    author='Johann-Mattis List',
    author_email='mattis_list@eva.mpg.de',
    url='https://github.com/pylogeny/pylotree',
    keywords='data',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    py_modules=['pylotree'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=3.6',
    install_requires=[
        "newick",
    ],
    extras_require={
        'dev': ['black', 'wheel', 'twine'],
        'test': [
            'pytest>=4.3',
            'pytest-cov',
            'coverage>=4.2',
        ],
    },
)
