from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='dict2xlsx',
    packages=find_packages(),
    license='MIT',
    version='0.0.1',
    description='Python Package to convert dict to xlsx',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Satyam Lohiya',
    author_email='lohiyasatyam@gmail.com',
    install_requires=['openpyxl'],
    setup_requires=['wheel'],
    url='https://github.com/Satyam-2001/dict2xlsx',
    keywords=['excel','dict-to-xlsx', 'convert', 'dict2xlsx'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ]
)