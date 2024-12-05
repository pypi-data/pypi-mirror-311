from seaway.utils import *
from .base_project_init import BaseProjectInit


class AppProjectInit(BaseProjectInit):

    def init(self, args):
        self._initAndroidProject()

    def _initAndroidProject(self):
        # 追加settings.gradle内容
        appendTemplateFileContent(
            "settings.gradle",
            "Android/AppProject/settings.gradle",
            super().settingGradleHasInit,
        )
        # 追加gradle.properties内容
        graGropertiesSuccess = appendTemplateFileContent(
            "gradle.properties",
            "Android/AppProject/gradle.properties",
            super().gradlePropertiesHasInit,
        )
        # 复制build.gradle
        copyTemplateFile("build.gradle", "Android/AppProject/build.gradle")
        print(f"😄APP壳工程初始化完毕~")
        if graGropertiesSuccess:
            print(f"✅请在gradle.properties里面配置你的APP信息~")
