from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        requirements = [
            line.strip()
            for line in lines
            if line.strip() and not line.startswith(('#', '-e'))
        ]
    return requirements


setup(
    name="ConvexTrader",
    version="0.0.0",
    author="Liam Davis",
    author_email="ljdavis27@amherst.edu",
    description="A package for portfolio optimization using convex optimization",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/ACquantclub/Applications-of-Convex-Optimization/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=parse_requirements('./requirements.txt'),
)
