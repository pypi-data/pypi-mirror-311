def install(self, package_name, version=None):
    """安装指定包，默认安装最新版本"""
    # 检查包是否已安装
    installed_version = self._check_installed(package_name)
    if installed_version:
        print(f"软件包 {package_name} 已安装，版本为 {installed_version}。")
        return

    # 下载包
    if version:
        print(f"正在安装 {package_name} 的指定版本：{version}...")
        destination = f"{package_name}-{version}.downloaded"
    else:
        print(f"正在安装 {package_name} 的最新版本...")
        destination = f"{package_name}-latest.downloaded"

    self.downloader.download_package(package_name, destination, version)

    # 确认文件是否存在
    if not os.path.exists(destination):
        print(f"错误：文件 {destination} 未下载成功。请检查网络或包名是否正确。")
        return

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
