from setuptools import setup, find_packages

setup(
    name='facekiapiclientv2',
    version='1.0',
    packages=find_packages(),
    install_requires=['requests'],
    description='FACEKI KYC Api Library',
    author='Faceki',
    author_email='haziq@faceki.com',
    keywords=['api', 'client', 'library'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)