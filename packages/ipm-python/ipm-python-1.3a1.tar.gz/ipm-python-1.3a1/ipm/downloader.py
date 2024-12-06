import requests
from bs4 import BeautifulSoup
from ipm.progress import ProgressBar


class Downloader:
    """负责从镜像源下载文件"""

    def __init__(self, mirror_url="https://mirrors.aliyun.com/pypi/simple/"):
        self.mirror_url = mirror_url

    def download_package(self, package_name, destination, version=None):
        """下载指定包的文件"""
        package_name = package_name.lower()  # 确保包名为小写

        try:
            # 如果未指定版本，解析最新版本
            if not version:
                version = self._get_latest_version(package_name)
                print(f"解析到最新版本文件：{version}")

            # 拼接下载 URL
            url = f"{self.mirror_url}{package_name}/{version}"
            print(f"正在从 {url} 下载 {package_name}...")
            response = requests.get(url, stream=True)
            if response.status_code == 404:
                raise FileNotFoundError(f"无法找到包 {package_name} 的文件 {version}，请检查包名或版本号。")

            # 下载文件并显示进度条
            total_size = int(response.headers.get('content-length', 0))
            progress_bar = ProgressBar(total_size)

            with open(destination, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
                    progress_bar.update(len(chunk))

            progress_bar.close()
            print(f"{package_name} 下载完成，保存到 {destination}")

        except FileNotFoundError as e:
            print(f"错误：{e}")
        except Exception as e:
            print(f"下载失败：{e}")
            if os.path.exists(destination):
                os.remove(destination)
            raise

    def _get_latest_version(self, package_name):
        """解析 PyPI 页面获取最新版本文件名"""
        url = f"{self.mirror_url}{package_name}/"
        response = requests.get(url)
        if response.status_code == 404:
            raise FileNotFoundError(f"无法找到包 {package_name}。")

        soup = BeautifulSoup(response.text, "html.parser")

        # 查找页面中文件名
        links = soup.find_all("a")
        files = [link.text.strip() for link in links if link.text.endswith((".whl", ".tar.gz"))]

        if not files:
            raise ValueError(f"未找到 {package_name} 的可用文件。")

        # 返回最新的文件（按名称排序，可能需要更复杂的逻辑以确定版本）
        return sorted(files, reverse=True)[0]
