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

def InsertBaseDir(contents, directory):
    match = re.search("<!--BaseDir\(\)-->",contents)
    while match:
        contents = contents[:match.start(0)] + directory + contents[match.end(0):]
        match = re.search("<!--BaseDir\(\)-->", contents)
    return contents


def GetListHTML(ProjectsPath, Template):
    projects = [x[0] for x in os.walk(ProjectsPath)][1:]

    listItems = [] #tuple: 0=priority 1=html
    for project in projects:
        print("Project: " + project)
        if not path.exists(project + "/meta.json"):
            print("Project meta file not found")
            continue
        if not path.exists(project + "/index.html"):
            print("html file not found")
            continue

        f = open(project + "/meta.json", "r")
        metadata = json.loads(f.read())
        f.close()
        if ('Visible' in metadata.keys()) and  metadata['Visible'].lower() == 'false':
            print("Project Hidden")
            continue

        html = Template
        html = html.replace("$Link",project[9:] + "/index.html")
        html = html.replace("$Thumbnail",project[9:] + "/thumbnail.jpg")
        html = html.replace("$Title",metadata['FullName'])
        html = html.replace("$Description",metadata['Description'])
        if 'CustomCSS' in metadata.keys():
            html = html.replace("$CustomCSS",metadata['CustomCSS'])
        html = html.replace("$CSS_Class", (''.join(e for e in metadata['FullName'] if e.isalnum())))
        listItem = (metadata['Priority'],(html))#tuple: 0=priority 1=html
        #print(listItem)
        listItems.append ( listItem )

    if not len(listItem) > 0:
        print("List still empty!")
        return ""

    listItems.sort(key=lambda x: x[0], reverse=True)
    #print(listItems)
    listhtml = '\n'.join((n[1] for n in listItems))
    #print(listhtml)
    return listhtml

def AddList(contents):
    match = re.search("<!--List\(.*,.*\)-->",contents)
    if not match:
        return contents

    print("Adding List")
    params = match.group(0)[9:len(match.group(0))-4].split(",")
    if not path.exists("Includes/" + params[1] + ".html"):
        print("could not find list folder: " + "Template/" + params[0])
        return contents

    f = open("Includes/" + params[1] + ".html", "r")
    template = f.read();
    f.close()

    if not path.exists("Template/"+params[0]):
        print("Project folder not found")
        return contents

    projectspath = "Template/"+params[0]
    return contents[:match.start(0)] + GetListHTML(projectspath,template) + contents[match.end(0):]


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


def Build(src, destinationPath, testmode, baseDir=""):
    if not os.path.exists(destinationPath):
        os.makedirs(destinationPath)
    if baseDir=="":
        baseDir = os.path.abspath(destinationPath)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(destinationPath, item)
        if os.path.isdir(s):
            Build(s, d,testmode,baseDir)
        else:
            shutil.copy2(s, d)
            if(d.rsplit('.', 1)[1]=="html"):
                f = open(d,"r")
                content = f.read();
                f.close()
                content = IncludeAll(content)
                content = AddList(content)
                content = InsertBaseDir(content,baseDir)
                content = AddPageName(content,src)
                content = SetTestModeText(content,testmode)
                f = open(d, "w")
                f.write(content);
                f.close()

testingMode=True
TemplateFolder = "Template"
DestinationFolder = "Build " + str(datetime.now().strftime("%d-%m-%Y %H.%M.%S"))
Build(TemplateFolder,DestinationFolder,testmode=False)
print("Website build in: " + os.path.abspath(DestinationFolder))
Build(TemplateFolder,"LastBuild",testmode=True)
print("Website build in: " + os.path.abspath("LastBuild"))

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
#
# Template