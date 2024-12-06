import subprocess
import sys
from ipm.progress import download_with_progress

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
        self._run_command(command, show_progress=True)

    def uninstall(self, package):
        """卸载软件包"""
        command = [sys.executable, "-m", "pip", "uninstall", "-y", package]
        self._run_command(command, show_progress=False)

    def list_installed(self):
        """列出已安装的软件包"""
        command = [sys.executable, "-m", "pip", "list"]
        self._run_command(command, show_progress=False)

    def _run_command(self, command, show_progress=False):
        """运行命令并处理输出"""
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = process.stdout.decode('utf-8')
        stderr = process.stderr.decode('utf-8')
        
        if process.returncode == 0:
            print(stdout)
        else:
            print(stderr)
            print("错误：命令执行失败。")
