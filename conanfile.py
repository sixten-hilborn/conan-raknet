from conans import ConanFile, CMake
from conans.tools import get, patch
import os
import fnmatch


def apply_patches(source, dest):
    for root, dirnames, filenames in os.walk(source):
        for filename in fnmatch.filter(filenames, '*.patch'):
            patch_file = os.path.join(root, filename)
            dest_path = os.path.join(dest, os.path.relpath(root, source))
            patch(base_path=dest_path, patch_file=patch_file)


class RaknetConan(ConanFile):
    name = "RakNet"
    description = 'Game networking middleware'
    version = "4.081"
    folder = "RakNet-master"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False]
    }
    default_options = "shared=True"
    exports = ["CMakeLists.txt", 'patches*']
    generators = "cmake"
    url = "https://github.com/sixten-hilborn/conan-raknet"
    license = "BSD - https://opensource.org/licenses/BSD-3-Clause"

    def source(self):
        get("https://github.com/OculusVR/RakNet/archive/master.zip")
        apply_patches('patches', self.folder)

    def build(self):
        cmake = CMake(self.settings)
        enable_dll = 1
        enable_static = 1
        if self.options.shared:
            enable_static = 0
        else:
            enable_dll = 0
        options = [
            '-DRAKNET_ENABLE_DLL={0}'.format(enable_dll),
            '-DRAKNET_ENABLE_STATIC={0}'.format(enable_static)
        ]
        build_options = ''
        self.run_and_print('cmake . %s %s' % (cmake.command_line, ' '.join(options)))
        self.run_and_print("cmake --build . %s %s" % (cmake.build_config, build_options))
        
    def package(self):
        self.copy("*.h", dst="include/RakNet", src="{0}/source".format(self.folder))
        self.copy("*.lib", dst="lib", src="lib", keep_path=False)
        self.copy("*.a", dst="lib", src="lib", keep_path=False)
        self.copy("*.so", dst="lib", src="lib", keep_path=False)
        self.copy("*.dll", dst="bin", src="bin", keep_path=False)
        self.copy("*.dylib", dst="bin", src="bin", keep_path=False)

    def package_info(self):
        if self.options.shared:
            self.cpp_info.libs = ["RakNetDLL"]
        else:
            self.cpp_info.libs = ["RakNetLibStatic"]
            if self.settings.os == 'Windows':
                self.cpp_info.libs.append('ws2_32')
            elif self.settings.os == 'Linux':
				self.cpp_info.libs.append('pthread')

    def run_and_print(self, command):
        self.output.warn(command)
        self.run(command)
