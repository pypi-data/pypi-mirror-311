from setuptools import setup, find_packages

setup(
    name='helpmeidli',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[            # Any dependencies your package needs
        'numpy',
        'requests',
    ],
    author='borngamer10',
    author_email='lilgoku70@gmail.com',
    description='A brief description of your package',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
