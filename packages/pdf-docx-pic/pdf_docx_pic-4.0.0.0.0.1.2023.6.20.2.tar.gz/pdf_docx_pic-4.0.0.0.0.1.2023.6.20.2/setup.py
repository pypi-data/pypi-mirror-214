from setuptools import *

a = open(".\\README.rst", mode='r', encoding = 'UTF-8').read()

setup(
    name = "pdf_docx_pic",
    version = "4.0.0.0.0.1.2023.6.20.2",
    packages = find_packages(),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "Environment :: GPU",
        "Framework :: Jupyter :: JupyterLab :: 4",
        "Framework :: Django :: 4.2",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Framework :: Jupyter :: JupyterLab :: Extensions :: Mime Renderers",
        "Operating System :: Microsoft :: Windows :: Windows 8",
        "Operating System :: Microsoft :: Windows :: Windows 8.1",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Operating System :: POSIX",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
    ],
    install_requires = [
        "ttkbootstrap>=1.10.1, <1.11",
        "pdf2docx>=0.5.5, <0.6.0", 
        "docx2pdf>=0.1.8, <0.2.0", 
        "PyMuPDF>=1.22.1, <1.23", 
        "Pillow>=9.5.0, <10.0", 
        "wheel>=0.38.2, <0.41",
    ],
    long_description = a
)
