import re
import os.path
from os import path
import json
import shutil
from datetime import datetime

def IncludeAll(contents):
    match = re.search("<!--Include\(.*\)-->",contents)
    while match:
        include = match.group(0)[12:len(match.group(0))-4]
        includeHtml = ""
        if(path.exists("Includes/"+include+".html")):
            f = open("Includes/"+include+".html", "r")
            includeHtml = f.read();
            f.close()
        else:
            print("Include not found: " + "Includes/"+include+".html")
        contents = contents[:match.start(0)] + includeHtml + contents[match.end(0):]
        match = re.search("<!--Include\(.*\)-->", contents)
    return contents

def SetTestModeText(contents, testmode):
    match = re.search("<!--TestModeOnly\([\s\S]*\)-->",contents)
    while match:
        if testmode:
            include = match.group(0)[17:len(match.group(0))-4]
            contents = contents[:match.start(0)] + include  + contents[match.end(0):]
        else:
            contents = contents[:match.start(0)] + contents[match.end(0):]
        match = re.search("<!--TestModeOnly\([\s\S]*\)-->", contents)
    return contents

def InsertDir(contents, directory):
    match = re.search("<!--Dir\(\)-->",contents)
    while match:
        contents = contents[:match.start(0)] + directory + contents[match.end(0):]
        match = re.search("<!--Dir\(\)-->", contents)
    return contents


def CreateListElement(ProjectPath, Template):
    print("Project: " + ProjectPath)
    if path.exists(ProjectPath + "/meta.json"):
        if path.exists(ProjectPath + "/index.html"):
            f = open(ProjectPath + "/meta.json", "r")
            metadata = json.loads(f.read())
            f.close()

            html = Template
            html = html.replace("$Link",ProjectPath[9:] + "/index.html")
            html = html.replace("$Thumbnail",ProjectPath[9:] + "/thumbnail.jpg")
            html = html.replace("$Title",metadata['FullName'])
            html = html.replace("$Description",metadata['Description'])
            return html
        else:
            print("html file not found")
    else:
        print("Project meta file not found")
    return ""

def AddList(contents):
    match = re.search("<!--List\(.*,.*\)-->",contents)
    if match:
        params = match.group(0)[9:len(match.group(0))-4].split(",")
        if path.exists("Includes/" + params[1] + ".html"):
            f = open("Includes/" + params[1] + ".html", "r")
            template = f.read();
            f.close()
            print("Template found")
            if path.exists("Template/"+params[0]):
                print("Project folder found")
                listHtml = ""
                for project in [x[0] for x in os.walk("Template/"+params[0])][1:]:
                    listHtml+=CreateListElement(project,template)
                return contents[:match.start(0)] + listHtml + contents[match.end(0):]
            else:
                print("could not find list folder: " + "Template/"+params[0])
        else:
            print("could not find template")
    return contents

def AddPageName(contents, folder):
    match = re.search("<!--PageName\(\)-->", contents)
    while match:
        if path.exists(folder + "/meta.json"):
            f = open(folder + "/meta.json", "r")
            metadata = json.loads(f.read())
            f.close()
            contents = contents[:match.start(0)] + metadata['FullName'] + contents[match.end(0):]
        else:
            print("No meta file found for pagename: " + folder + "/meta.json")
            contents = contents[:match.start(0)] +  contents[match.end(0):]
        match = re.search("<!--PageName\(\)-->", contents)
    return contents

def Build(src, dst,testmode):
    os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            Build(s, d,testmode)
        else:
            shutil.copy2(s, d)
            if(d.rsplit('.', 1)[1]=="html"):
                f = open(d,"r")
                content = f.read();
                f.close()
                content = IncludeAll(content)
                content = AddList(content)
                content = InsertDir(content,os.path.abspath(DestinationFolder))
                content = AddPageName(content,src)
                content = SetTestModeText(content,testmode)
                f = open(d, "w")
                f.write(content);
                f.close()

testingMode=True
TemplateFolder = "Template"
DestinationFolder = "Build " + str(datetime.now().strftime("%d-%m-%Y %H.%M.%S"))
Build(TemplateFolder,DestinationFolder,testingMode)

#Documentation
#
#Including File (Must be html):
#"<!--Include(FileNameToInclude)-->"
#assumes only one list per file


#List

#"<!--List(ListFolder,ListTemplate)-->"

#creates a list for pages
#each page is a folder that contains:
# - Metadata (Json)
# - Page itself
# - Title
# TODO Priority
#
# Template