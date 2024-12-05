from setuptools import setup, find_packages

setup(
    name="nidhi_tts",  # Name of your project
    version="4.2.2",  # Initial version
    author="Sandesh Kumar",
    author_email="connect@sandeshai.in",
    description="A perfect Text To Speech TTS engine for tts tasks and variety of neural voices",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://sandeshai.in/nidhi-tts",  # Project URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  # Minimum Python version
    install_requires=open("requirements.txt").readlines(),  # Dependencies
)
