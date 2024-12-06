from setuptools import setup, find_packages

setup(
    name="directory-visualizer", 
    version="0.1.0",  
    author="Md. Rasel Meya",
    author_email="raselmeya2194@gmail.com",
    description="A CLI tool to visualize directory structures as Markdown or Mermaid diagrams",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/raselmeya94/directory-visualizer", 
    packages=find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "directory-visualizer=directory_visualizer.visualizer:run_visualizer",
        ],
    },
    include_package_data=True,
)
