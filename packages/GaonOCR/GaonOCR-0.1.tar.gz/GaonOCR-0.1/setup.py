from setuptools import setup, find_packages

setup(
    name='GaonOCR',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    description='A OCR library for T4 documents',
    long_description=open('README.md').read(),
    install_requires=['pdf2image', 'opencv-python', 'pytesseract', 'numpy', 'pandas', 'Pillow'], # add other required packages
    author='Gaon.ai',
)
