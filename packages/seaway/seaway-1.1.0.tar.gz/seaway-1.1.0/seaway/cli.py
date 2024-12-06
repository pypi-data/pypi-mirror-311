# coding=UTF-8
import argparse
from seaway.core import *
from seaway.version import *


def version():
    return "version:" + VERSION


def run():
    parser = argparse.ArgumentParser(prog="seaway")

    parser.add_argument("-v", "--version", help="查看版本号", action="store_true")

    subparsers = parser.add_subparsers(title="客户端组件化CLI")

    # 创建 init 子命令
    init_parser = subparsers.add_parser("init", help="初始化工程")
    init_subparsers = init_parser.add_subparsers(title="初始化子命令")

    # 初始化APP壳工程
    init_app_parser = init_subparsers.add_parser("app", help="初始化APP壳工程")
    init_app_parser.set_defaults(func=AppProjectInit().init)

    # 初始化组件壳工程
    init_module_p_parser = init_subparsers.add_parser("mp", help="初始化组件壳工程")
    init_module_p_parser.set_defaults(func=ModuleProjectInit().init)

    # 初始化组件模块
    init_module_parser = init_subparsers.add_parser("module", help="初始化组件模块")
    init_module_parser.add_argument(
        "-dir", "--dirPath", type=str, help="组件工程路径(默认命令运行目录)", metavar=""
    )
    init_module_parser.add_argument(
        "-g", "--group", type=str, help="maven group", metavar=""
    )
    init_module_parser.add_argument(
        "-a", "--artifact", type=str, help="maven artifact", metavar=""
    )
    init_module_parser.set_defaults(func=ModuleInit().init)

    args = parser.parse_args()
    # print("args="+str(args))

    if hasattr(args, "func"):
        args.func(args)
        return
    if args.version:
        checkVersions()
        print(version())
        return
    parser.print_help()
