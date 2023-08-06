from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="my_chat_bot_builder",
    version="0.0.1",
    author="jack",
    author_email="jack.cx.chen@pccw.com",
    description="A chat bot builder based on Azure OpenAI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my-chat-bot-builder",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.0.1",
        "requests>=2.26.0",
        "pydantic>=1.8.2",
        "python-dotenv>=0.19.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
