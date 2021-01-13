可以禁止触控板的两指清扫，但是其他的应用需要这个功能。

命令行运行这个：

defaults write com.google.Chrome AppleEnableSwipeNavigateWithScrolls -bool false

网上说这个，但是mac的没有这个参数：

chrome://flags/#overscroll-history-navigation

