import setuptools

with open("Readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bulksmsng",
    version="1.0.0",
    license="MIT",
    author="Oluwaloni Emmanuel",
    author_email="emmyvera01@gmail.com",
    description="The BulkSMSNigeria API Wrapper is a Python library that provides a convenient interface for sending SMS messages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emmyvera/bulksmsng",
    keywords=["SMS", "Nigeria", "BulkSMS", "Bulk SMS Nigeria", "bulk sms"],
    install_requires=["requests"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)