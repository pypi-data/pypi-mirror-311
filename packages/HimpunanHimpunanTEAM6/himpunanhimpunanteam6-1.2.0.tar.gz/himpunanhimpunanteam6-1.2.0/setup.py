from setuptools import setup, find_packages

setup(
    name="HimpunanHimpunanTEAM6", 
    version="1.2.0",  
    author="Team 6_Leonard_Apryadi", 
    author_email="leowidj@gmail.com",
    description="Package Python untuk operasi himpunan menggunakan teori himpunan dasar",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/leowdij08/Team-6_Diskrit_Himpunan.git",  
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
