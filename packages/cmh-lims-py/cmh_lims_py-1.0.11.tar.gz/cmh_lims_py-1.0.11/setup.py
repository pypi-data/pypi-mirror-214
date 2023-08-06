from setuptools import setup, find_packages

setup(
    name='cmh_lims_py',
    version='1.0.11',
    packages=find_packages(),
    include_package_data=True,
    author='Manish Kumar',
    author_email='mkumar1@cmh.edu',
    description='Python module for basic querying of LIMS samples, analyses, and analysis files',
    url='https://dev.azure.com/CMHResearchIS/GMC/_git/cmhlims_py',
    install_requires=[
        'pyyaml',
        'pymysql',
        'pandas'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)

