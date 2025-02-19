from setuptools import find_packages, setup

setup(
    name="calllogdb",
    version="0.1.0",
    description="Библиотека для работы с call_log",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="miomelliot, Alexeyalexeyalexm, deydysh",
    author_email="s89652158910@gmail.com",  # укажите тут свои почты связанные с GitHub
    url="https://github.com/Mcn-BPA/CallLogDB",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    license="Proprietary - internal use only",
    python_requires=">=3.12",
)
