class BaseProjectInit:

    def init(self, args):
        pass

    def settingGradleHasInit(self,originContent):
        return "seaway cli start" in originContent and "seaway cli end" in originContent

    def gradlePropertiesHasInit(self,originContent):
        return "#seaway" in originContent
