#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os
import shutil


class BisonConan(ConanFile):
    name = "bison_installer"
    version = "3.2.4"
    description = "Bison is a general-purpose parser generator that converts an annotated context-free grammar into " \
                  "a deterministic LR or generalized LR (GLR) parser employing LALR(1) parser tables"
    topics = ("conan", "bison", "parser", "generator", "grammar")
    url = "https://github.com/bincrafters/conan-bison_installer"
    homepage = "https://www.gnu.org/software/bison/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "GPL-3.0-only"
    exports = ["LICENSE.md"]
    settings = "os_build", "arch_build", "compiler"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    requires = ("m4_installer/1.4.18@bincrafters/stable",)
    exports_sources = ["patches/*"]

    @property
    def _is_mingw_windows(self):
        return self.settings.os_build == "Windows" and self.settings.compiler == "gcc" and os.name == "nt"

    def build_requirements(self):
        if self._is_mingw_windows:
            self.build_requires("msys2_installer/latest@bincrafters/stable")

    def source(self):
        source_url = "http://ftp.gnu.org/gnu/bison/bison-%s.tar.gz" % self.version
        tools.get(source_url,
                  sha256="cb673e2298d34b5e46ba7df0641afa734da1457ce47de491863407a587eec79a")
        os.rename("bison-" + self.version, self._source_subfolder)

    def build(self):
        # https://github.com/Alexpux/MINGW-packages/tree/master/mingw-w64-bison
        tools.patch(patch_file=os.path.join("patches",
                                            "0003-create_pipe-uses-O_TEXT-not-O_BINARY-mode.patch"),
                    base_path=self._source_subfolder)
        tools.patch(patch_file=os.path.join("patches",
                                            "0004-open-source-file-in-binary-mode-MS-ftell-bug-ks-68337.patch"),
                    base_path=self._source_subfolder)

        with tools.chdir(self._source_subfolder):
            env_build = AutoToolsBuildEnvironment(self, win_bash=self._is_mingw_windows)
            env_build.configure()
            env_build.make()
            env_build.install()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        if self._is_mingw_windows:
            mingw_bin = os.path.join(self.deps_cpp_info["mingw_installer"].rootpath, "bin")
            self.copy(pattern="libwinpthread-1.dll", dst="bin", src=mingw_bin)

    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        self.env_info.BISON_PKGDATADIR = os.path.join(self.package_folder, "share", "bison")
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
