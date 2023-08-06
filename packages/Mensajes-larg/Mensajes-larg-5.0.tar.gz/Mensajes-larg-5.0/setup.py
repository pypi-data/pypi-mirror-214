from struct import pack
from setuptools import setup, find_packages


setup(
    name='Mensajes-larg',
    version='5.0',
    description='Un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Luis A Ruiz',
    author_email='luisarg59@gmail.com',
    # url='www.largrus.com',
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[paquete.strip()
                      for paquete in open('requirements.txt').readlines()],
    classifiers=[
        'Environment :: Console',
        # 'Intendend Audience :: Developers',
        # 'License :: OSI Approved :: MIT license',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities'
    ],
)
