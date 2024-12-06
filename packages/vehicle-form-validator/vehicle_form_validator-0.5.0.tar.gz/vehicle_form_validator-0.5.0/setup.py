from setuptools import setup, find_packages

setup(
    name="vehicle_form_validator",
    version="0.5.0",
    packages=find_packages(),
    install_requires=[],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Rhegisan Jebas",
    author_email="rhegisanjebas71@gmail.com",
    description="A library to validate vehicle and user details",
    url="https://github.com/rhegisan/vehicle_form_validator",
    classifiers=[  # PyPI classifiers to describe your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
