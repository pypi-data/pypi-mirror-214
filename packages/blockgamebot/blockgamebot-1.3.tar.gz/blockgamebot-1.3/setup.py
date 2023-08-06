from setuptools import setup, find_packages

VERSION = '1.3'
DESCRIPTION = 'Hypixel SkyBlock Scammer List Package'

# Setting up
setup(
    name="blockgamebot",
    version=VERSION,
    author="asov",
    author_email="<noemtdev@gmail.com>",
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['aiohttp'],
    keywords=['python', 'hypixel', 'skyblock', 'scammer list', 'block game bot', 'blockgamebot'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ],
    package_data={'blockgamebot': ['blockgamebot/*']}
)
