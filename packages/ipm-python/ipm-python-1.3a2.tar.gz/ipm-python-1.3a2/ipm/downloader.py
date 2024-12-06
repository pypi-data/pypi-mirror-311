import requests
import os
from tqdm import tqdm

class Downloader:
    """负责从镜像源下载文件"""

    def __init__(self, mirrors=None):
        self.mirrors = mirrors or [
            "https://mirrors.aliyun.com/pypi/packages/",
            "https://pypi.tuna.tsinghua.edu.cn/packages/",
            "https://pypi.org/packages/"
        ]

    def download_package(self, package_name, destination, version=None):
        """从多个镜像源下载包"""
        package_name = package_name.lower()

        for mirror_url in self.mirrors:
            try:
                # 如果未指定版本，解析最新版本
                if not version:
                    version = self._get_latest_version(mirror_url, package_name)
                    print(f"解析到最新版本文件：{version}")

                # 拼接下载 URL
                url = f"{mirror_url}{package_name[0]}/{package_name[1]}/{package_name}/{version}"
                print(f"正在从 {url} 下载 {package_name}...")

                # 下载文件
                response = requests.get(url, stream=True)
                if response.status_code == 404:
                    print(f"未找到包 {package_name} 的文件 {version}，尝试下一个镜像源。")
                    continue  # 尝试下一个镜像源

                # 显示下载进度条
                total_size = int(response.headers.get('content-length', 0))
                progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

                with open(destination, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                        progress_bar.update(len(chunk))

                progress_bar.close()
                print(f"{package_name} 下载完成，保存到 {destination}")
                return  # 下载成功后退出方法

            except Exception as e:
                print(f"尝试从镜像源 {mirror_url} 下载失败：{e}")

        raise FileNotFoundError(f"无法从所有镜像源找到包 {package_name} 的文件 {version}，请检查包名或版本号。")

    def _get_latest_version(self, mirror_url, package_name):
        """从指定镜像源解析最新版本文件名"""
        url = f"{mirror_url}{package_name}/"
        response = requests.get(url)
        if response.status_code == 404:
            raise FileNotFoundError(f"无法找到包 {package_name} 在镜像源 {mirror_url} 中的目录。")

        # 在页面中提取所有可能的包文件名
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")
        files = [link.text.strip() for link in links if link.text.endswith((".whl", ".tar.gz"))]

        if not files:
            raise ValueError(f"未找到 {package_name} 的可用文件。")

        # 返回最新文件（按名称排序）
        return sorted(files, reverse=True)[0]