# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path


long_description = 'A library to programmatically create, interact, encrypt and automate your data pipelines making it simple to scale to the most popular cloud plattforms.'

setup(
    name="cloudpy_org",
    version="1.6.4",
    description="Cloud data pipeline organization and automation library. Includes AWS framework manager API.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://www.cloudpy.org/",
    author="cloudpy.org",
    author_email="admin@cloudpy.org",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["cloudpy_org"],
    include_package_data=True,
    install_requires=["pandas","pandasql","requests","boto3","awswrangler","tqdm","botocore","numpy","cryptography","s3fs","pillow","flask","APScheduler","pytz","soundfile","SpeechRecognition","openai","pyttsx3","sounddevice","scipy","werkzeug","PyPDF2"]
)