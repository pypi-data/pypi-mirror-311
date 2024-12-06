from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ubuntu-terminal-agent",  
    version="0.1.0",  
    author="Agents Valley",
    author_email="agentsvalley@gmail.com",
    description="A Python agent for Ubuntu that generates and executes terminal commands using Hugging Face models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ubuntu-terminal-agent",  
    packages=find_packages(), 
    install_requires=[
        "huggingface_hub>=0.14.1"  
    ],
    entry_points={
        "console_scripts": [
            "ubuntu-terminal-agent=agent.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)
