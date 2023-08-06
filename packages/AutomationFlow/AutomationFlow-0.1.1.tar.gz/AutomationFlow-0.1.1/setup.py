from setuptools import find_packages, setup

setup(
    name='AutomationFlow',
    packages=find_packages(include=["AutomationFlow"]),
    version='0.1.0',
    description='A "literate" script execution framework. Makes writing more readable scripts easier.',
    author='gkegke',
    license='MIT',
    install_requires=[
        "rich",
        "loguru"
    ],
    extras_require={
        "dev": ["pytest"]
    },
    tests_require=["pytest"],
    python_requires=">=3.8",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    project_urls={
        "Homepage": "https://github.com/gkegke/AutomationFlow"
    },
)
