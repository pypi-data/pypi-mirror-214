from os import path
from setuptools import setup, find_packages

about_path = path.join(path.dirname(path.abspath(__file__)), "halc", "__about__.py")
about = {}
with open(about_path) as fp:
    exec(fp.read(), about)

setup(
    name=about["__title__"],
    version=about["__version__"],
    description="Python SDK for Happyrobot's HALC",
    long_description="Software Development Kit in Python to interact with Happyrobot's copilot (HALC)",
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    license=about["__license__"],
    keywords="happyrobot computer vision artificial intelligence foundation models large vision",
    install_requires=[
        "pyyaml==6.0",
        "requests==2.22.0",
        "tqdm==4.65.0",
        "pillow==9.5.0",
        "python-magic==0.4.27",
        "uuid==1.30",
    ],
    packages=find_packages(),
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
)
