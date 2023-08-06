from setuptools import setup, find_packages

setup(
    name='lottry',
    package_dir={'': 'lottry'},
    packages=find_packages('lottry'),
    version='0.1',
    license='MIT',
    description='Python SDK of the lord of the rings API',
    author='David Borsodi',
    author_email='zellermester@gmail.com',
    url='https://github.com/celerymen/lottry',
    download_url='https://github.com/celerymen/lottry/archive/v_01.tar.gz',
    keywords=['LoTR', 'SDK'],
    install_requires=[
        'httpx',
        'pydantic',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
