import os
import zipfile
import tarfile
import pkg_resources
import site
from ipm.downloader import Downloader

class Installer:
    """负责软件包安装和管理"""
    def __init__(self, mirror_url="https://mirrors.aliyun.com/pypi/simple/"):
        self.downloader = Downloader(mirror_url)
        self.site_packages = site.getsitepackages()[0]

    def install(self, package_name, version=None):
        """安装指定包"""
        # 检查包是否已安装
        installed_version = self._check_installed(package_name)
        if installed_version:
            print(f"软件包 {package_name} 已安装，版本为 {installed_version}。")
            return

        # 下载包
        destination = f"{package_name}.downloaded"  # 临时文件
        self.downloader.download_package(package_name, destination, version)

        # 自动识别文件格式并安装
        if zipfile.is_zipfile(destination):
            self._install_wheel(destination)
        elif tarfile.is_tarfile(destination):
            self._install_tar(destination)
        else:
            print(f"错误：文件 {destination} 格式未知，无法安装。")

        # 删除临时文件
        if os.path.exists(destination):
            os.remove(destination)

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

    def uninstall(self, package_name):
        """卸载指定包"""
        # 检查包是否已安装
        installed_version = self._check_installed(package_name)
        if not installed_version:
            print(f"软件包 {package_name} 未安装，无需卸载。")
            return

        # 尝试删除包
        package_path = os.path.join(self.site_packages, package_name)
        try:
            for root, dirs, files in os.walk(package_path, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            os.rmdir(package_path)
            print(f"成功卸载软件包 {package_name}。")
        except Exception as e:
            print(f"卸载软件包 {package_name} 时发生错误：{e}")

    def list_installed(self):
        """列出已安装的软件包"""
        print("已安装的软件包列表：")
        for dist in pkg_resources.working_set:
            print(f"{dist.project_name} ({dist.version})")

    def _check_installed(self, package_name):
        """检查包是否已安装"""
        for dist in pkg_resources.working_set:
            if dist.project_name.lower() == package_name.lower():
                return dist.version
        return None
