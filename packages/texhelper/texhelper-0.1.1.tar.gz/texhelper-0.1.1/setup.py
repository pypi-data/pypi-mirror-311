from setuptools import setup, find_packages

setup(
    name='texhelper', 
    version='0.1.1',  
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
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    python_requires='>=3.10',  
    description='A Python library for processing Tex files, such as formatting BibTeX titles, capitalizing words, and more.', 
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
    license='Apache License 2.0',  
    author='Shuhong Dai',
    author_email='daishuhong02@gmail.com',
)
