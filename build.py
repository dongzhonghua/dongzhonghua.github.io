import getopt
import os
import sys

folder = "notes"
template = '{0}* [{1}]({2})\n'

notes = os.listdir(folder)
notes.sort()

f = open("SUMMARY.md", "w")
f.write("# Summary\n")
f.write("* [前言](README.md)\n")


def create_readme(file):
    readme = file + "/README.md"
    with open(readme, "w") as rm:
        rm.write(os.path.basename(file))


def get_filelist(file, level):
    new_dir = file
    if os.path.isfile(file):
        if "README" not in file:
            text = template.format("\t" * level, os.path.basename(file), file)
            f.write(text)
    elif os.path.isdir(file):
        text = template.format("\t" * level, os.path.basename(file), file + "/README.md")
        f.write(text)
        _listdir = os.listdir(file)
        _listdir.sort()
        for s in _listdir:
            if s.startswith("."):
                continue
            if "README.md" not in os.listdir(file):
                create_readme(file)
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
    os.system("gitbook build . docs")
    if upload is not 0:
        os.system("git add . && git commit -m {} && git push origin main".format(upload))
