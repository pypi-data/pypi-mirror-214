# -*- coding: utf-8 -*-

import setuptools   # type: ignore

setuptools.setup(
    name="fastapi_motor",
    version="0.1.0",
    author="huihui",
    author_email="sunjiehuimail@foxmail.com",
    description="FastAPI asyncio motor MongoDB",
    long_description="FastAPI asyncio motor MongoDB",
    long_description_content_type="text/markdown",
    url="https://kgithub.com/JiehuiSun/fastapi_motor.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Framework :: AsyncIO",
    ],
    install_requires=["motor>=3.1.2", "fastapi>=0.97.0", "pytz>=2023.3"],
    python_requires=">=3.9",
)
