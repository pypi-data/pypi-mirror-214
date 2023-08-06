# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipycrawl",
    version="0.0.0",
    author="innovata",
    author_email="iinnovata@gmail.com",
    description='파일 다운로드 및 각종 RESTful OpenAPI 를 사용하여 데이타를 수집하는 Innovata Web Crawler 라이브러리 패키지',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/innovata/iCrawler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"src"},
    packages=setuptools.find_packages('src'),
    python_requires=">=3.8",
)
