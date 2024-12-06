from setuptools import setup, find_packages

setup(
    name="PBFUS1",
    version="1.0.0",
    description="A package to handle and process ultrasound image datasets of fetal planes",
    author="Juan Pablo Barrientos",
    author_email="juan.barrientos@galileo.edu",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "pandas",
        "matplotlib",
        "PyYAML",
        "requests",
        "tqdm"
    ],
    entry_points={
        # "console_scripts": [
        #     "download_dataset=PBFUS1.data_loader:download_dataset",
        # ],
    },
    include_package_data=True,
    package_data={
        "PBFUS1": ["config.yaml"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
