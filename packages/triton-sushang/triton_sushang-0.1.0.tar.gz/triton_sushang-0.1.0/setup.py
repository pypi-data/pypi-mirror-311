from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="triton_sushang",
    version="0.1.0",
    author="goudemaoningsir",
    author_email="gf13951891236@gmail.com",
    description="A unified Triton client for speech recognition and object detection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/goudemaoningsir/triton_sushang",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "tritonclient[http]>=2.17.0",
        "ultralytics>=8.0.0",
        "pydub>=0.25.1",
    ],
    include_package_data=True,
    package_data={
    },
)
