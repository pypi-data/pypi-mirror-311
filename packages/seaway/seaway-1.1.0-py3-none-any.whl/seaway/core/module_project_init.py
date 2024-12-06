from seaway.utils import *
from .base_project_init import BaseProjectInit


class ModuleProjectInit(BaseProjectInit):

    def init(self,args):
        self._initModuleProject()

    def _initModuleProject(self):
        # 追加gradle.properties内容
        graGropertiesSuccess =appendTemplateFileContent(
            "gradle.properties",
            "Android/ModuleProject/gradle.properties",
            super().gradlePropertiesHasInit,
        )
        # 复制build.gradle
        copyTemplateFile("build.gradle", "Android/ModuleProject/build.gradle")
        print(f"😄组件壳工程初始化完毕~")
        if graGropertiesSuccess:
            print(f"✅请在gradle.properties里面配置你的APP信息~")
