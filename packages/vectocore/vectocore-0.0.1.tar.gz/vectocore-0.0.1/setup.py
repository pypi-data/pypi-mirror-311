from setuptools import setup, find_packages

setup(
    name="vectocore",
    version="0.0.1",
    description="Hyundai futurenet AI Vector database library",
    author="hd-ai-lab",
    author_email="store_admin@hyundaifuturenet.co.kr",
    url="https://www.vectocore.com/",
    install_requires=["requests"],
    package=find_packages(exclude=[]),
    keywords=["AI", "vector database", "RAG"],
    python_requires=">=3.8",
    package_data={},
    zip_safe=False,
)
