import os
import requests
from ipm.progress import ProgressBar

class Downloader:
    """负责从镜像源下载文件"""
    def __init__(self, mirror_url="https://mirrors.aliyun.com/pypi/simple/"):
        self.mirror_url = mirror_url

    def download_package(self, package_name, destination, version=None):
        """下载指定包的文件"""
        url = f"{self.mirror_url}{package_name}/"
        if version:
            url += f"{version}/"

        print(f"正在从 {url} 下载 {package_name}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        progress_bar = ProgressBar(total_size)

        with open(destination, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
                progress_bar.update(len(chunk))

        progress_bar.close()
        print(f"{package_name} 下载完成，保存到 {destination}")
