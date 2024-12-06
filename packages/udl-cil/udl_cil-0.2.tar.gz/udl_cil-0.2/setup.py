# setup.py
from setuptools import setup, find_packages

setup(
    name="udl_cil",
    version="0.2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    description="General parallel runner and manager, initially designed for https://github.com/XiaoXiao-Woo/UDL",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="XiaoXiao-Woo",
    author_email="wxwsx1997@gmail.com",
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "udl_cil=v2.udl_cil:parser_args",  # 指定可执行脚本的入口
        ],
    },
    # data_files=("", ["example/configs/*.yaml"]),
    package_data={"": ["*.py"]},
    install_requires=[
        "hydra-core",
        "optuna",
        "omegaconf",
        "GPUtil",
        "rich",
        "yapf==0.40.2",
        "hydra-joblib-launcher",
        "colorlog",
    ],
    license="GPLv3",
)
