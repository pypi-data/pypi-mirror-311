import argparse
from ipm.installer import Installer

def main():
    parser = argparse.ArgumentParser(description="IPM - 完全独立的 Python 软件包管理器")
    parser.add_argument("command", choices=["install", "uninstall", "list"], help="支持的命令")
    parser.add_argument("package", nargs="?", help="软件包名称")
    parser.add_argument("-v", "--version", help="指定安装的版本")
    args = parser.parse_args()

    installer = Installer()

    if args.command == "install":
        if not args.package:
            print("错误：请提供要安装的软件包名称。")
            return
        installer.install(args.package, version=args.version)
    elif args.command == "uninstall":
        if not args.package:
            print("错误：请提供要卸载的软件包名称。")
            return
        installer.uninstall(args.package)
    elif args.command == "list":
        installer.list_installed()
