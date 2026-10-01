import os


def getAbsPathLocatedFromCurFile(curFilePath: str, filepath: str):
    return os.path.join(os.path.dirname(os.path.abspath(curFilePath)), filepath)
