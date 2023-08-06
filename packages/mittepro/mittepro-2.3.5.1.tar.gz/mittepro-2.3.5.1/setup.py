# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='mittepro',
    version='2.3.5.1',
    install_requires=[
        'six>=1.12.0',
        'arrow>=0.12.1',
        'requests>= 2.24.0,< 2.50.0',
        'simplejson>=3.16.0',
    ],
    url='https://github.com/ThCC/mittepro-py',
    description='MittePro is a powerful marketing tool with features to help companies with their marketing goals and deliver emails from their websites and apps.',
    long_description=open("README.rst").read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    license='Apache-2.0',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],
    author='Thiago Cardoso de Castro',
    author_email='thiago.decastro2@gmail.com',
)

# python setup.py bdist_egg
# pip3 install wheel
# python setup.py sdist bdist_wheel
# sudo apt install twine
# twine upload dist/mittepro-x.y.z.tar.gz
# twine upload dist/mittepro-x.y.z-py2-none-any.whl
