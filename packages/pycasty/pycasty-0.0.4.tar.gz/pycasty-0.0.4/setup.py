from setuptools import setup, find_packages


VERSION = '0.0.4'
DESCRIPTION = 'Raycasting Engine using python'
LONG_DESCRIPTION = 'A package that allows to render a 2D array map into a 3D explorable map, with the help of raycasting technique'

# Setting up
setup(
    name="pycasty",
    version=VERSION,
    author="tempewda",
    author_email="tempewda@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'raycast', 'raycaster', 'pixelated', 'doom style', 'wolfenstein style'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
