#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conans import ConanFile, CMake
import os


class TestPackageConan(ConanFile):

    generators = ["cmake"]

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        self.run("bison --version")

        bin_path = os.path.join("bin", "test_package")
        self.run(bin_path, run_environment=True)
