from setuptools import setup, find_packages

setup(
    name='kos000113-universal',  # Your library name
    version='0.2.0',  # Version of your library
    packages=find_packages(),  # Automatically find all packages
    install_requires=["pyOpenSSL", "tgcrypto"],  # Specify dependencies, if any
    author='Kostya',  # Your name
    author_email='kostya_gorshkov_06@vk.com',  # Your email
    description='Universal library for personal use',  # Short description
    long_description=open('readme.md', encoding='utf-8').read(),  # Long description
    long_description_content_type='text/markdown',  # Format of long description
    url='https://github.com/kostya2023/kos000113-Universal',  # Link to the repository
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Specify license
        'Operating System :: OS Independent',  # Corrected Operating System classifier
    ],
    python_requires='>=3.6',  # Minimum Python version
)
