import os

#将远程文件下载到本地目录
def gitArchive(repo,repoPath):
    command = "git archive --remote=" + repo + "HEAD " + repoPath + "| tar -x"
    print(command)
    result = os.popen(command).readlines()
    print(str(result))
    
#将远程文件平铺到对应的本地目录下
def gitArchiveStrip(repo,repoPath,localDir,stripDepth):
    command = "git archive --remote=" + repo + "HEAD " + repoPath + "| tar -x -C " + localDir + "--strip-components="+stripDepth
    print(command)
    result = os.popen(command).readlines()
    print(str(result))
    