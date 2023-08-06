import setuptools

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setuptools.setup(
	name= "GmailBox",
	version= "0.0.2",
	author= "Hamo",
    keywords=["gmail","mail","GmailBox","inbox"],
    install_requires=['requests','beautifulsoup4'],
    long_description=readme,
    long_description_content_type="text/markdown",
	description= "With this library, you can create random Gmail and receive messages",
	packages=setuptools.find_packages(),
    license="LGPLv3",
	classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)