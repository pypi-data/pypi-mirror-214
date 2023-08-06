from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='facekiapiclientv2',
    version='1.1',
    packages=find_packages(),
    install_requires=['requests'],
    description='FACEKI KYC Api Library',
    long_description=long_description,
    long_description_content_type="text/markdown",
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