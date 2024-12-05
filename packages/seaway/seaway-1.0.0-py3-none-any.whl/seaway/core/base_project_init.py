class BaseProjectInit:

    def init(self, args):
        pass

    def settingGradleHasInit(originContent):
        return "seaway cli start" in originContent and "seaway cli end" in originContent

    def gradlePropertiesHasInit(originContent):
        return "#seaway" in originContent
