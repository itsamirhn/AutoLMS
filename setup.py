from setuptools import setup

setup(
    name="AutoLMS",
    version="0.4",
    packages=["autolms"],
    url="https://github.com/itsamirhn/AutoLMS",
    download_url="https://github.com/itsamirhn/AutoLMS/archive/refs/tags/v0.4.tar.gz",
    license="MIT",
    author="AmirMohammad Hosseini Nasab",
    author_email="awmirhn@gmail.com",
    description="Automation of getting into LMS classes",
    install_requires=[
        "selenium",
        "fire",
        "pyyaml",
        "InquirerPy",
        "schedule",
    ],
    python_requires='>=3',
    entry_points={
        "console_scripts": [
            "autolms=autolms.main:main",
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
)
