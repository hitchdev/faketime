# -*- coding: utf-8 -*
from setuptools.command.install import install
from setuptools import find_packages
from setuptools import setup
import subprocess
import codecs
import faketime
import sys
import os


class CustomInstall(install):
    def run(self):
        """Compile libfaketime."""
        if sys.platform == "linux" or sys.platform == "linux2":
            libname = 'libfaketime.so.1'
            libnamemt = 'libfaketimeMT.so.1'
        elif sys.platform == "darwin":
            libname = 'libfaketime.1.dylib'
            libnamemt = 'libfaketimeMT.1.dylib'
        else:
            sys.stderr.write("WARNING : libfaketime does not support platform {}\n".format(sys.platform))
            sys.stderr.flush()
            return

        faketime_lib = os.path.join('faketime', libname)
        faketime_lib_mt = os.path.join('faketime', libnamemt)
        self.my_outputs = []

        setup_py_directory = os.path.dirname(os.path.realpath(__file__))
        faketime_directory = os.path.join(setup_py_directory, "faketime")
        os.chdir(faketime_directory)
        if sys.platform == "linux" or sys.platform == "linux2":
            subprocess.check_call(['make',])
        else:
            subprocess.check_call(['make', '-f', 'Makefile.OSX'])
        os.chdir(setup_py_directory)

        dest = os.path.join(self.install_purelib, os.path.dirname(faketime_lib))
        dest_mt = os.path.join(self.install_purelib, os.path.dirname(faketime_lib_mt))

        try:
            os.makedirs(dest)
        except OSError as e:
            if e.errno != 17:
                raise
        self.copy_file(faketime_lib, dest)

        if os.path.exists(faketime_lib_mt):
            self.copy_file(faketime_lib_mt, dest_mt)
        self.my_outputs.append(os.path.join(dest, libname))

        install.run(self)

    def get_outputs(self):
        outputs = install.get_outputs(self)
        outputs.extend(self.my_outputs)
        return outputs



def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts), 'r').read()

setup(name="faketime",
      version="0.9.6.6",
      description="Libfaketime wrapper.",
      long_description=read('README.rst'),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing',
          'Topic :: Software Development :: Libraries',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
      ],
      keywords='libfaketime faketime',
      author='Colm O\'Connor',
      author_email='colm.oconnor.github@gmail.com',
      url='https://github.com/crdoconnor/faketime/',
      license='GPLv2',
      install_requires=[],
      packages=find_packages(exclude=["docs", "*.so.1", "*.1.dylib", ]),
      package_data={},
      zip_safe=False,
      include_package_data=True,
      cmdclass={'install': CustomInstall},
)
