from setuptools import setup, find_packages

setup(
    name='trading_deque_2',
    version='1.0',
    author='Alan MH Beem',
    author_email='Alan.Beem@seattlecolleges.edu',
    description='This is a refactored project from the CS DS Program at NSC',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AlanBeem/TradingDeque_2/tree/main',
    packages=find_packages(exclude=['tests', 'docs']), # Automatically finds all packages
    install_requires=[
        'dependency1>=1.0.0',
        'dependency2',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
