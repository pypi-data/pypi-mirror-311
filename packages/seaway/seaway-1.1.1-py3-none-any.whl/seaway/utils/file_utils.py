import os


# 将模板文件写入到项目目录中
def appendTemplateFileContent(projectRelFilePath, templateRelFilePath, hasInitCallback):
    cmdDir = os.path.join(os.getcwd())
    prjectFilePath = os.path.join(cmdDir, projectRelFilePath)
    if not os.path.isfile(prjectFilePath):
        print(f"❌初始化{projectRelFilePath}失败,没有找到{projectRelFilePath}文件")
        return False

    # 读取模板文件
    templateFilePath = os.path.join(
        os.path.dirname(__file__), "../template", templateRelFilePath
    )
    # 将模板文件写入到项目目录中
    originContent = open(prjectFilePath, "r", encoding="utf-8").read()
    if hasInitCallback and hasInitCallback(originContent):
        print(f"{prjectFilePath}已经初始化")
        return
    templateContent = open(templateFilePath, "r", encoding="utf-8").read()
    allContent = originContent + "\n" + templateContent
    open(prjectFilePath, "w").write(allContent)
    print(f"✅初始化{prjectFilePath}成功")
    return True


# 复制模板文件
def copyTemplateFile(projectRelFilePath, templateRelFilePath):
    cmdDir = os.path.join(os.getcwd())
    templateFilePath = os.path.join(
        os.path.dirname(__file__), "../template", templateRelFilePath
    )
    projectFilePath = os.path.join(cmdDir, projectRelFilePath)
    open(projectFilePath, "w").write(
        open(templateFilePath, "r", encoding="utf-8").read()
    )
    print(f"✅初始化{projectRelFilePath}成功")
