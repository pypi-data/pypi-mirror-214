import setuptools

with open("Readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ebulksms",    
    version="1.0.0",
    license="MIT",
    author="Oluwaloni Emmanuel",
    author_email="emmyvera01@gmail.com",
    description="The EBulkSMS Python library provides a simple interface for sending SMS messages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emmyvera/ebulksms",
    keywords=["SMS", "Nigeria", "BulkSMS", "EBulkSMS", "bulk sms"],
    install_requires=["requests"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)