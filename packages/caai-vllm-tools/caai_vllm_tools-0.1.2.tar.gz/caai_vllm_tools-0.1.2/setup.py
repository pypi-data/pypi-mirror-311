from setuptools import setup, find_packages

setup(
    name="caai_vllm_tools",  # Package name
    version="0.1.2",  # Initial version
    author="valogan",
    author_email="vaiden.logan@yahoo.com",
    description="A tool that allows you to use the OpenAI API with vLLM generate function",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",  # Repository URL
    packages=find_packages(),
    install_requires=[
        "vllm>=0.6.3.post1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
