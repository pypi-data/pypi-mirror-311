from setuptools import setup, find_packages

setup(
    name="smart_detect",
    version="0.1.0",
    description="A smart pose detection package for movement analysis using OpenCV and Mediapipe",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/smart_detect",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "mediapipe",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
