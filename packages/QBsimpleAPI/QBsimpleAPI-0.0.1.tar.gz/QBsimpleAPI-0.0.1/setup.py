from setuptools import setup, find_packages

with open("README.md", "r",encoding="utf-8") as readme_file:
    readme = readme_file.read()

requirements = ["bs4","requests"] # 这里填依赖包信息
VERSION="0.0.1"

setup(
    name="QBsimpleAPI",
    version=VERSION,
    author="slexce",
    author_email="sim69732@gmail.com",
    description="用于与qbittorrent webui通讯的简易api接口",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/small-bili/qBittorrentWebUI-simple-API",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
	"Programming Language :: Python :: 3.10",
	"License :: OSI Approved :: MIT License",
    ],
)