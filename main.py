import subprocess
import git
from pathlib import Path
import re
import os

def rmdir(directory):
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()


resultPath = 'diff_result'
if os.path.exists(resultPath):
    rmdir(Path(resultPath))
else:
    os.mkdir(resultPath)
result = subprocess.run(['git', '--version'], capture_output=True)
print(result.stdout.decode('utf-8'))

gitBinPath = '/home/a97410985new/Documents/git_fork/git'
exludePathBlobPatterns = [':!dist', ':!packages', ':!deps']
matchFileExtensions = ['*.js']
diffPathPattern = exludePathBlobPatterns + matchFileExtensions
hunkHeaderRegex = r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@(.*)"

for dir in os.listdir('observed_projects'):
    print(dir)
    repoPath = './observed_projects/' + dir
    repo = git.Repo(repoPath)
    # print(repo.active_branch)
    # print(repo.iter_commits())
    # print(repo._get_config_path(config_level='repository'))
    hasVisitedGitDiff = set()
    visitCommitLimit = 50
    for curCommitIndex, commit in enumerate(repo.iter_commits()):
        if curCommitIndex == visitCommitLimit:
            break
        diffIndex: git.DiffIndex = commit.diff('HEAD~1', paths=diffPathPattern)
        with open(os.path.join(resultPath, dir + '_result.diff'), 'a') as f, open(os.path.join(resultPath, dir + '_content.txt'), 'a') as f2:

            for diff_item in diffIndex.iter_change_type('M'):
                # print("A blob:\n{}".format(diff_item.a_blob.data_stream.read().decode('utf-8')))
                # print("B blob:\n{}".format(diff_item.b_blob.data_stream.read().decode('utf-8'))) 
                print(diff_item.a_blob)
                print(diff_item.b_blob)
        

                with open(os.path.join(repoPath, 'a.js'), 'w') as tempFileA:
                    tempFileA.write(diff_item.a_blob.data_stream.read().decode('utf-8'))

                with open(os.path.join(repoPath, 'b.js'), 'w') as tempFileA:
                    tempFileA.write(diff_item.b_blob.data_stream.read().decode('utf-8'))
                
                result = subprocess.run(['sudo', gitBinPath, 'diff', '--no-index' , 'a.js', 'b.js'], capture_output=True, cwd=repoPath)
                if result.stderr:
                    raise Exception(result.stderr)
                # print(result.stdout.decode('utf-8'))
                diffContent = result.stdout.decode('utf-8')
                diffCmdLine = diff_item.a_blob.hexsha + '-' + diff_item.b_blob.hexsha
                if diffCmdLine in hasVisitedGitDiff:
                    continue
                else:
                    hasVisitedGitDiff.add(diffCmdLine)

                # print(diffContent.split('\n',5))
                hunkHeaders = list(filter(lambda line: re.match(hunkHeaderRegex, line), diffContent.split('\n')))            
                f.write(diffContent)
                for hunkHeader in hunkHeaders:
                    print(hunkHeader)
                    match = re.match(hunkHeaderRegex, hunkHeader)
                    hunkLine = 0
                    endLine = 0
                    hunkSize = 0
                    hunkText = ''
                    if match is not None:
                        for groupNum in range(0, len(match.groups())):
                            if groupNum == 0:
                                print(hunkHeader[match.start(groupNum+1):match.end(groupNum+1)])
                                hunkLine = int(hunkHeader[match.start(groupNum+1):match.end(groupNum+1)])
                            elif groupNum == 1:
                                hunkSize = int(hunkHeader[match.start(groupNum+1):match.end(groupNum+1)])
                            elif groupNum == 4:
                                hunkText = hunkHeader[match.start(groupNum+1):match.end(groupNum+1)]
                    lines = diff_item.a_blob.data_stream.read().decode('utf-8').split('\n')
                    hunkTextLine = hunkLine
                    for index,line in enumerate(lines[hunkLine::-1]):
                        if line.strip(' \t').find(hunkText.strip(' \t')) != -1:
                            hunkTextLine -= index
                            break
                    startLine = hunkTextLine - 5
                    if startLine < 0:
                        startLine = 0
                    contentLines = diff_item.a_blob.data_stream.read().decode('utf-8').split('\n', hunkLine+hunkSize)[startLine:hunkLine+hunkSize]
                    f2.write(diffContent[:diffContent.find('\n')]+ '\n' + hunkHeader + "\nA blob:" + diff_item.a_blob.hexsha + 
                            "\n{}".format('\n'.join(contentLines)) + '\n')
