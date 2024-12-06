from setuptools import setup, find_packages

setup(
    name="TEMD",
    version="0.1.01",
    packages=find_packages(),
    install_requires=[
        'scikit-learn>=0.24.0',
        'requests>=2.25.0',
        'joblib>=0.17.0'
    ],
    
    author="EMD Team",
    author_email="adityakhair45@gmail.com",
    description="Enhanced Error Message Decoder for Python",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://raw.githubusercontent.com/Sujaykharat/python-error-dataset/main/errors_dataset.json",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        'TEMD': ['models/*.joblib'],
    },
)
