from setuptools import setup, find_packages

setup(
    name="buaa_open_source_22371550_test_package1",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        'requests',
        'chardet',
    ],
    author="lhc",
    author_email="1500518009@qq.com",
    description="Package1 for web scraping",
    long_description="获取网页信息",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
