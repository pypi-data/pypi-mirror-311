from setuptools import setup, find_packages

setup(
    name='testpippp',
    version='0.4',
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
        "console_scripts":[
            "yo = testpip:hello"
        ]
    }
)