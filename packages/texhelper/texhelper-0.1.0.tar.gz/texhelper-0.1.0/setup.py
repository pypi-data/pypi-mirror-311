from setuptools import setup, find_packages

setup(
    name='texhelper', 
    version='0.1.0',  
    packages=find_packages(), 
    install_requires=[  
        'numpy',  
        'pytest',  
        'regex',  
        'pandas',  
        'pyyaml', 
        'click',  
        'requests',  
        'tqdm',  
        'matplotlib',  
        'beautifulsoup4',  
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  
    description='A Python library for processing Tex files, such as formatting BibTeX titles, capitalizing words, and more.', 
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
    license='Apache License 2.0',  
)

