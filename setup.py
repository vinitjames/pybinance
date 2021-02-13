from setuptools import setup, find_packages

setup(
        name='binancepy',
        version='0.0.1',
        packages= ['binance', 'binance.endpoints'],
        description='Binance REST API python implementation',
        url='https://github.com/vinitjames/binancepy',
        author='Vinit James',
        license='MIT',
        author_email='vinit.james24@gmail.com',
        install_requires=['requests',
                          'urllib3',
                          'certifi',
                          'cryptography',
                          'ujson',
                          'dateparser',
                          'pytz',
                          'requests'],
        keywords='binance exchange rest api bitcoin ethereum btc eth neo',
        classifiers=[
                    'Intended Audience :: Developers',
                    'License :: OSI Approved :: MIT License',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.5',
                    'Programming Language :: Python :: 3.6',
                    'Programming Language :: Python :: 3.7',
                    'Programming Language :: Python',
                    'Topic :: Software Development :: Libraries :: Python Modules',
                ],
        python_requires='>=3.0',
    )
