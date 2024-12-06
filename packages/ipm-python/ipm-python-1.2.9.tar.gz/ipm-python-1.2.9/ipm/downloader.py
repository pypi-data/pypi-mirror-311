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
                print(f"解析到最新版本：{version}")

            # 拼接下载 URL
            url = f"{self.mirror_url}{package_name}/{package_name}-{version}-py3-none-any.whl"
            print(f"正在从 {url} 下载 {package_name}...")
            response = requests.get(url, stream=True)
            response.raise_for_status()

            # 下载文件并显示进度条
            total_size = int(response.headers.get('content-length', 0))
            progress_bar = ProgressBar(total_size)

            with open(destination, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
                    progress_bar.update(len(chunk))

            progress_bar.close()
            print(f"{package_name} 下载完成，保存到 {destination}")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"错误：无法找到包 {package_name}。请检查包名是否正确。")
            else:
                print(f"下载失败：{e}")
        except Exception as e:
            print(f"下载过程中发生错误：{e}")

    def _get_latest_version(self, package_name):
        """解析 PyPI 页面获取最新版本"""
        url = f"{self.mirror_url}{package_name}/"
        response = requests.get(url)
        if response.status_code == 404:
            raise ValueError(f"无法找到包 {package_name}。")

        soup = BeautifulSoup(response.text, "html.parser")
        # 查找页面中最新版本号
        links = soup.find_all("a")
        versions = [link.text.strip() for link in links if link.text]
        if not versions:
            raise ValueError(f"未找到 {package_name} 的可用版本。")
        return sorted(versions, reverse=True)[0]  # 返回最新版本
