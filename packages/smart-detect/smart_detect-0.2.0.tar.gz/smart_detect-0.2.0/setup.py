from setuptools import setup, find_packages

setup(
    name="smart_detect",
    version="0.2.0",
    description="A smart pose detection package for movement analysis using OpenCV and Mediapipe",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="himanshu-kumar-jha",
    author_email="himanshukrjha004@gmail.com",
    url="https://github.com/himanshu-kr-jha",
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
