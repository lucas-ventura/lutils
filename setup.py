from setuptools import setup, find_packages

setup(
    name="lutils",
    version="0.1",
    packages=find_packages(),
    install_requires=["opencv-python", "Pillow", "pandas", "ruamel-yaml"],
    author="Lucas Ventura",
    author_email="lucas.ventura.r@gmail.com",
    description="A package for file and frame processing",
    url="https://github.com/lucas-ventura/lutils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
