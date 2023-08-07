from setuptools import setup, find_packages

setup(
    name="haberpy",
    version="0.0.3",
    description="Haber sitelerinden bildirimleri kolay sekilde alabilmeniz icin tasarlanmis bir Python API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Meinos10/haberpy",
    author="Emre",
    author_email="rewoxirewo@gmail.com",
    license="MIT",
    #classifiers = [
    #"Programming Language :: Python :: 3",
    #"License :: OSI Approved :: MIT License",
    #"Operating System :: OS Independent",
    #],
    keywords=["haberpy","haberpython", "haber", "haber-python", "haber-py", "sondakika", "son-dakika"],
    packages=find_packages(),
    requires=["requests", "beautifulsoup4"]
)