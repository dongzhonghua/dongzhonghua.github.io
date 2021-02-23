import os

folder = "notes"
template = '{0}* [{1}]({2})\n'

notes = os.listdir(folder)
notes.sort()

f = open("mygitbook/SUMMARY.md", "w")
f.write("# Summary\n")
f.write("* [Introduction](README.md)\n")


def create_readme(file):
    readme = file + "/README.md"
    with open(readme, "w") as rm:
        rm.write(os.path.basename(file))


def get_filelist(dir, level):
    new_dir = dir
    if os.path.isfile(dir):
        if "README" not in dir:
            text = template.format("\t" * level, os.path.basename(dir), "../" + dir)
            f.write(text)
    elif os.path.isdir(dir):
        text = template.format("\t" * level, os.path.basename(dir), "../" + dir + "/README.md")
        f.write(text)
        _listdir = os.listdir(dir)
        _listdir.sort()
        for s in _listdir:
            if s.startswith("."):
                continue
            if "README.md" not in os.listdir(dir):
                create_readme(dir)
            new_dir = os.path.join(dir, s)
            get_filelist(new_dir, level + 1)


if __name__ == '__main__':
    listdir = os.listdir(folder)
    listdir.sort()
    for d in listdir:
        if d.startswith("."):
            continue
        get_filelist(folder + "/" + d, 0)
    print(">>>>>>>开始生成SUMMARY.md")
