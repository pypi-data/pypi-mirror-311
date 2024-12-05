from setuptools import setup, find_packages

setup(
    name='azauthlib',
    version="1.0.2b1",  
    author='Cedric Moore Jr.',
    author_email='cedricmoorejunior5@gmail.com',
    description='A Python library simplifying Azure Microsoft Graph authentication. Provides an intuitive interface for acquiring access tokens through interactive login, silent authentication, device code flow, and client credentials flow. Includes utilities for seamless token storage and refresh management.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cedricmoorejr/azauthlib/tree/v1.0.2b1',
    project_urls={
        'Source Code': 'https://github.com/cedricmoorejr/azauthlib/releases/tag/v1.0.2-beta.1',
    },
    entry_points={
        "console_scripts": [
            "azauthlib-app = azauthlib.config_app:main",
        ],
    },
    package_data={
        'azauthlib': [
            'assets/*.ico', 
            'assets/*.png'
        ],
    },    
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
    install_requires=[
        'python-dotenv',    	
        'portalocker',
        'msal',
    ],
    license='Apache Software License',
    include_package_data=True,
)
