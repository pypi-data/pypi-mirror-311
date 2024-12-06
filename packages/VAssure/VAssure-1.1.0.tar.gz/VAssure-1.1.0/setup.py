from setuptools import setup, find_packages

setup(
    name='VAssure',                     # Package name
    version='1.1.0',                    # Version number
    author='Sukumar Kutagulla',
    author_email='sukumar@spotline.com',
    description='VAssure: A Python-based Selenium and Robot Framework automation framework',
    long_description=open('README.md', encoding='utf-8').read(),  # Ensures UTF-8 encoding
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/VAssure',  # Replace with your actual repository URL
    packages=find_packages(),           # Automatically find and include all sub-packages
    install_requires=[
        'selenium>=4.0.0',              # Selenium dependency
        'pytest>=7.0.0',                # Pytest for test execution
        'PyYAML>=6.0',                  # YAML for configuration parsing
        'pytest-xdist>=2.5.0',          # Parallel execution support
        'pytest-html>=3.2.0',           # HTML reporting for pytest
        'bson>=0.5.10',                 # BSON for MongoDB handling
        'pymongo>=4.5.0',               # MongoDB support
        'pycryptodome>=3.18.0',         # Cryptography library
        'pytz>=2023.3',                 # Timezone support
        'requests>=2.31.0',             # HTTP requests library
        'ratelimit>=2.2.1',             # Rate-limiting library
        'robotframework-pabot>=2.0.0',  # Parallel execution for Robot Framework
        'robotframework-seleniumlibrary>=6.0.0',  # Selenium integration for Robot Framework
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',           # Python version requirement
    include_package_data=True,          # Include non-Python files like YAML
)
