from setuptools import setup, find_packages

setup(
    name="artypy",
    version="0.11.0",
    author="artypy team",
    author_email="ahmatovbulat@gmail.com",
    description="Lightweight library for artistic filters",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/artypy/arty",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=[
        "numpy",
        "matplotlib",
        "tqdm",
        "opencv-python",
        "progressbar",
        "scipy",
        "scikit-learn"
    ],
    extras_require={
        "cuda": ["torch"],
    },
)
