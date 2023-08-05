from pyconju.xlsx import Excelx as merger
import os
path = os.getcwd()
print(path)

fileList = ["file1.xlsx","file2.xlsx"]
merger.merge_xlsx(fileList,path)