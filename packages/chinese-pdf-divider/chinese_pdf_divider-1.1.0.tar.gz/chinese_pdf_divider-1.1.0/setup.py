from setuptools import setup, find_packages

setup(
    name='chinese_pdf_divider',
    version='1.1.0',
    author='yunsi lin',
    author_email='yunsi0115@gmail.com',
    description='divide chinese pdf file into blocks within 512',
    packages=find_packages(),
    install_requires=[
        'pymupdf',
        'fitz',
        'pandas',
        'numpy'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)