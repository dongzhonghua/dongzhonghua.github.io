git diff 高亮显示： git config --global color.ui true



git合并远程到本地

git rebase -i origin/master

强制和远程一致：git reset --hard origin/master && git pull



cherry-pick: 将做某个分支的某个提交拉到本分支。



```bash
git rebase -i commit号
```

rebase命令太强了，上面的命令既可以把多个commit合并成一个，也可以删除某个commit

```
# p, pick <commit> = use commit
# r, reword <commit> = use commit, but edit the commit message
# e, edit <commit> = use commit, but stop for amending
# s, squash <commit> = use commit, but meld into previous commit
# f, fixup <commit> = like "squash", but discard this commit's log message
# x, exec <command> = run command (the rest of the line) using shell
# b, break = stop here (continue rebase later with 'git rebase --continue')
# d, drop <commit> = remove commit
```

