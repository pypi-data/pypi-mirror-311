from setuptools import setup, find_packages

setup(
    name="firejson",
    version="0.1.1",
    author="Ngwashi Anthony",
    author_email="antoniokante2.0@gmail.com",
    description="A library to validate and populate JSON files in Firestore.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Madarakante/JSON_upload_to_Firestore",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "google-cloud-firestore",
        "google-auth",
        # Add other dependencies here if required
    ],
)