import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UmBokDong",
    version="1",
    author="Jason Choi",
    author_email="orangecolver@gmail.com",
    description="엄복동 구하기",
    long_description=open('README.md').read(),
    long_description_content_type="",
    url="",
    install_requires=[],
    include_package_data=True,
    packages = setuptools.find_packages(),
    python_requires=">=3"
)
