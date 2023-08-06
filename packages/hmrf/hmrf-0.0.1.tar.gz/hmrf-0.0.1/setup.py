import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hmrf",                     
    version="0.0.1",                       
    author="UPV",                    
    description="Package to extract keywords in one of the classes of a dataset",
    long_description=long_description,     
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      
    python_requires='>=3.6',                
    py_modules=["hmrf"],             
    package_dir={'':'hmrf/src'},     
    install_requires=["iso639-lang","numpy","scikit-learn","pandas","nltk","scipy"]
)
