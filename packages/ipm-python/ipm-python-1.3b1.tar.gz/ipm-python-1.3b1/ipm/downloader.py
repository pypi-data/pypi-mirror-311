def download_package(self, package_name, destination, version=None):
    """下载指定包的文件"""
    package_name = package_name.lower()  # 确保包名为小写
    try:
        # 如果未指定版本，解析最新版本
        if not version:
            version = self._get_latest_version(package_name)
            print(f"解析到最新版本：{version}")

        # 拼接下载 URL
        file_extension = version.split('.')[-1]
        if file_extension == "gz":
            url = f"{self.mirror_url}{package_name}/{package_name}-{version}"
        else:
            url = f"{self.mirror_url}{package_name}/{package_name}-{version}-py3-none-any.whl"

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

    except Exception as e:
        print(f"下载失败：{e}")
        if os.path.exists(destination):
            os.remove(destination)
        raise
