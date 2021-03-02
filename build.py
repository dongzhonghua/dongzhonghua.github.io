import getopt
import os
import sys
import time

folder = "notes"
template = '{0}* [{1}]({2})\n'

notes = os.listdir(folder)
notes.sort()

f = open("SUMMARY.md", "w")
f.write("# Summary\n")
f.write("* [前言](README.md)\n")

readme_template = '{0}* [{1}]({2})\n'


def write_readme(q, file, level):
    new_dir = file
    _listdir = os.listdir(file)
    _listdir.sort()
    _listdir.remove("README.md")
    for s in _listdir:
        if s.startswith("."):
            continue
        filename = os.path.basename(s)
        new_dir = os.path.join(file, s)
        if os.path.isfile(new_dir):
            text = template.format("\t" * level, filename, filename)
            q.write(text)
            print(q.name + file + ">>>>>>>1" + text)
        elif os.path.isdir(new_dir):
            text = template.format("\t" * level, filename, filename + '/README.md')
            q.write(text)
            write_readme(open(new_dir + "/README.md", 'w'), new_dir, level + 1)


def get_filelist(file, level):
    new_dir = file
    if os.path.isfile(file):
        if "README" not in file:
            text = template.format("\t" * level, os.path.basename(file), file)
            f.write(text)
    elif os.path.isdir(file):
        text = template.format("\t" * level, os.path.basename(file), file + "/README.md")
        write_readme(open(file + "/README.md", 'w'), file, 0)
        f.write(text)
        _listdir = os.listdir(file)
        _listdir.sort()
        for s in _listdir:
            if s.startswith("."):
                continue
            new_dir = os.path.join(file, s)
            get_filelist(new_dir, level + 1)


if __name__ == '__main__':
    upload = 0
    try:
        options, args = getopt.getopt(sys.argv[1:], "-u:", ["upload"])
    except getopt.GetoptError:
        sys.exit()
    for name, value in options:
        if name in ("-u", "--upload"):
            upload = value
    listdir = os.listdir(folder)
    listdir.sort()
    print(">>>>>>>开始生成SUMMARY.md")
    for d in listdir:
        if d.startswith("."):
            continue
        get_filelist(folder + "/" + d, 0)
    os.system("git install && gitbook build . docs")
    if upload is not 0:
        time.sleep(3)
        os.system("git add . && git commit -m {} && git push origin main".format(upload))
