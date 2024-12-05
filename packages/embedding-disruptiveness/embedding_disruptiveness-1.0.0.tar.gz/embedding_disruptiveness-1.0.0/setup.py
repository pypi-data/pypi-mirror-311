from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="embedding-disruptiveness",
    version="1.0.0",
    author="Munjung Kim, Skojaku",
    author_email="munjkim@iu.edu, skojaku@binghamton.edu",
    description="A Python package to calculate the disruption index and embedding disruptiveness measure using a citation network.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/embedding-disruptiveness",  # Replace with your project's URL
    packages=find_packages(include=["embedding_disruptiveness", "embedding_disruptiveness.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "tqdm",
        "numpy",
        "scikit-learn",
        "torch",
        "scipy",
        "numba",
    ],
    extras_require={
        "tests": ["pytest", "pytest-cov"],
    },
    include_package_data=True,
)
