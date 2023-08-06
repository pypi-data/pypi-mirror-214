from itertools import chain
from setuptools import find_packages, setup

setup(
    name="rush-serving",
    author="RUSH.AI",
    author_email="ratchaphonboss@gmail.com",
    version="0.1",
    description="serving api wrapper",
    url="https://github.com/rushai-dev/serving",
    license="GPL",
    license_files=["LICENSE"],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "uvicorn<=0.20.0",
        "fastapi<=0.92.0",
        "nest-asyncio<=1.5.6",
        "pyngrok<=6.0.0"
    ],
    zip_safe=False,
)