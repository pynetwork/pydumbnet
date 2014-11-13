#!/usr/bin/env python

import os
import sys

from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext

src = ['dnet/dnet.c']
dep = []
Libraries = []
IncludeDirs = []
LibraryDirs = []

include = "#include <dnet.h>"

if sys.platform == 'win32' or sys.platform == "nt":
    # XXX this is currently broken.
    Libraries = ["ws2_32", "advapi32", "iphlpapi", "ws2_32", "packet"]

    class BuildExtension(build_ext):
        user_options = (build_ext.user_options +
                        [("with-dnet=", None,
                          "directory where dnet is installed"),
                         ("with-winpcap=", None,
                          "directory where winpcap is installed")])
        with_dnet = None
        with_winpcap = None

        dnet_dlls = ()
        dnet_mingw = False

        def finalize_options(self):
            build_ext.finalize_options(self)
            if self.with_dnet is None:
                self.find_dnet()
            if self.with_winpcap is None:
                self.find_winpcap()
            self.find_dnet_dlls()
            self.add_dnet_compile_info()

        def find_dnet(self):
            """
            Find dnet's install directory.

            TODO get windows machine to implement this.
            """
            pass

        def find_dnet_dlls(self):
            self.dnet_dlls = []
            self.find_dnet_dll()

        def find_dnet_dll(self):
            pass

        def find_winpcap_dir(self):
            self.winpcap_dir = "/"

        def add_dnet_compile_info(self):
            self.include_dirs.append(self.with_winpcap + '/Include')
            self.library_dirs.append(self.with_winpcap + '/Lib')
            # self.include_dirs.append()
            # self.library_dirs.append()
            # self.libraries.extend(["libdnet"])

        def run(self):
            build_ext.run(self)
            for dllpath, newpath in self.dnet_dlls:
                self.copy_file(dllpath, newpath)

        def get_outputs(self):
            output = [pathpair[1] for pathpair in self.dnet_dlls]
            output.extend(build_ext.get_outputs(self))
            return output
else:
    BuildExtension = build_ext
    Libraries = ["dnet"]
    if os.path.isfile("/usr/include/dumbnet.h"):
        include = "#include <dumbnet.h>"
        Libraries = ["dumbnet"]

with open("dnet/dnet.h", "w+") as f:
    f.write(include)

dnet_extension = Extension('dnet',
                           src,
                           libraries=Libraries,
                           depends=dep,
                           include_dirs=IncludeDirs,
                           library_dirs=LibraryDirs)

setup(
    name='pydumbnet',
    version='1.12.1',
    packages=["dnet"],
    package_dir={"dnet": "dnet"},
    description='low-level networking library',
    author='Dug Song',
    author_email='dugsong@monkey.org',
    cmdclass={"build_ext": BuildExtension},
    url='http://libdnet.sourceforge.net/',
    ext_modules=[dnet_extension]
)
