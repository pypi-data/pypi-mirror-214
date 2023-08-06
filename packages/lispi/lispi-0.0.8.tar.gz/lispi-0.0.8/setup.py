from setuptools import setup , find_packages

setup(
    name='lispi',
    version='0.0.8',
    description='Create interactive slides from Jupyter Notebook',
    author='B7M',
    author_email='ibsnetwork001@email.com',
    url='https://github.com/yourusername/your-repo',
    packages=find_packages(),
    install_requires = ['gtts', 'click','nbconvert', 'jupyter', 'shutil', 'pkg_resources', 'os', 'subprocess'],
    keywords = ['notebook','live','code','py-scripts'],
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ]
)