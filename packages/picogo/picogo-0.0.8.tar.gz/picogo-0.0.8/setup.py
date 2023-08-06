from setuptools import setup

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

__project__ = 'picogo'
__packages__ = ['picogo']
__desc__ = 'A beginner-friendly library for using picogo with the Raspberry Pi Pico. '
__version__ = '0.0.8'
__author__ = "SkySLAM Co., Ltd."
__author_email__ = 'terabuilder@gmail.com'
__license__ = 'MIT'
__url__ = 'https://github.com/sunabove/PicoGo'
__keywords__ = [
    'picogo',
    'pico',
    'raspberry',
    'raspberry pi',
    'picorun',
    'skyslam',
]
__classifiers__ = [
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Programming Language :: Python :: Implementation :: MicroPython',
    ]
__long_description__ = """A beginner-friendly library for using picogo with the Raspberry Pi Pico.

```python
from picogo import Robot

robot = Robot()
robot.forward( speed = 30 )

```

Documentation is available at (https://github.com/sunabove/PicoGo/).
"""

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION

    def copy_main(self) :
        file = open( "/myMainFile.py", "w" )
        file.close()
    pass

setup(
    name=__project__,
    version=__version__,
    description=__desc__,
    long_description=__long_description__,
    long_description_content_type='text/markdown',
    url=__url__,
    author=__author__,
    author_email=__author_email__,
    license=__license__,
    classifiers=__classifiers__,
    keywords=__keywords__,
    packages=__packages__,

    cmdclass={
        'install': PostInstallCommand,
    },
)