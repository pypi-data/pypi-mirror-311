from seaway.utils import *
from .base_project_init import BaseProjectInit
import os


class ModuleInit(BaseProjectInit):

    def init(self, args):
        self._initModule(args)

    def _initModule(self, args):
        moduleDirPath = args.dirPath

        cmdDir = os.path.join(os.getcwd())
        if not moduleDirPath:
            moduleDirPath = cmdDir
        moduleGradleFilePath = os.path.join(moduleDirPath, "build.gradle")
        if not os.path.isfile(moduleGradleFilePath):
            print(f"❌请检查模块路径是否正确!!!")
        moduleNexusFilePath = os.path.join(moduleDirPath, "nexus.properties")
        if os.path.isfile(moduleNexusFilePath):
            print(f"已经初始化 {moduleNexusFilePath}")
            return

        self.checkMustArgs(args)
        group = args.group
        artifactId = args.artifact
        print(f"init module group={group} artifactId={artifactId}")
        if not group or not artifactId:
            print(f"❌请输入正确的group artifactId !!!")
            return
        # 将group和artifactId写入moduleNexusFilePath文件中
        with open(moduleNexusFilePath, "w") as file:
            file.write(f"nexus_groupId={group}\n")
            file.write(f"nexus_artifactId={artifactId}")

    def checkMustArgs(self, args):
        group = args.group
        artifactId = args.artifactId
        if not group:
            args.group = input("请输入 maven group: ")
        if not artifactId:
            args.artifactId = input("请输入 maven artifact: ")
