import os
import zipfile
import tarfile
import site
from ipm.downloader import Downloader

class Installer:
    """负责软件包安装和管理"""
    def __init__(self, mirror_url="https://mirrors.aliyun.com/pypi/simple/"):
        self.downloader = Downloader(mirror_url)
        self.site_packages = site.getsitepackages()[0]

    def install(self, package_name, version=None):
        """安装指定包"""
        destination = f"{package_name}.whl"  # 假设为 .whl 格式
        self.downloader.download_package(package_name, destination, version)

        if destination.endswith(".whl"):
            self._install_wheel(destination)
        elif destination.endswith(".tar.gz"):
            self._install_tar(destination)
        else:
            print("未知文件格式，无法安装。")

    def _install_wheel(self, wheel_file):
        """安装 .whl 文件"""
        print(f"正在安装 {wheel_file} 到 {self.site_packages}...")
        with zipfile.ZipFile(wheel_file, 'r') as zip_ref:
            zip_ref.extractall(self.site_packages)
        print(f"{wheel_file} 安装完成。")

    def _install_tar(self, tar_file):
        """安装 .tar.gz 文件"""
        print(f"正在安装 {tar_file} 到 {self.site_packages}...")
        with tarfile.open(tar_file, 'r:gz') as tar_ref:
            tar_ref.extractall(self.site_packages)
        print(f"{tar_file} 安装完成。")
