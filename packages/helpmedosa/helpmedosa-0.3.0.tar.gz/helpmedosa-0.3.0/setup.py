from setuptools import setup, find_packages

setup(
    name='helpmedosa',
    version='0.3.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[            # Any dependencies your package needs
        'numpy',
        'requests',
    ],
    author='lilgoku',
    author_email='lilgoku70@gmail.com',
    description='A brief description of your package',
    long_description_content_type='text/markdown',
    url='',  # Link to the package repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
