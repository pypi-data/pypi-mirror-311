import subprocess
import sys
from ipm.utils import run_command

ALIYUN_PYPI_MIRROR = "https://mirrors.aliyun.com/pypi/simple/"

class Installer:
    def install(self, package, latest=False, version=None):
        """安装软件包"""
        package_spec = package
        if version:
            package_spec += f"=={version}"
        elif latest:
            package_spec += " --upgrade"

        command = [
            sys.executable,
            "-m",
            "pip",
            "install",
            package_spec,
            "-i",
            ALIYUN_PYPI_MIRROR,
        ]
        print(f"正在安装软件包：{package_spec}")
        code, _, stderr = run_command(command, show_progress=True)
        if code == 0:
            print(f"成功安装 {package}。")
        else:
            print(f"安装失败：{stderr}")

    def uninstall(self, package):
        """卸载软件包"""
        command = [sys.executable, "-m", "pip", "uninstall", "-y", package]
        print(f"正在卸载软件包：{package}")
        code, _, stderr = run_command(command, show_progress=True)
        if code == 0:
            print(f"成功卸载 {package}。")
        else:
            print(f"卸载失败：{stderr}")

    def list_installed(self):
        """列出已安装的软件包"""
        command = [sys.executable, "-m", "pip", "list"]
        print("已安装的软件包列表：")
        _, stdout, _ = run_command(command)
        print(stdout)
