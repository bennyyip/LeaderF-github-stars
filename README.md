# LeaderF-github-stars

This Plugin use LeaderF to navigate to a repository that you stared on GitHub.

# Requirements

 - vim7.3 or higher. Only support vim7.4.330 or higher after [v1.01](https://github.com/Yggdroot/LeaderF/releases/tag/v1.01).
 - vim compiled with Python support, you can check by using `echo has('python')` or `echo has('python3')` to see if the result is `1`; Make sure that your python2 version is Python **2.7** or higher and python3 version is Python **3.1** or higher.
 - wcwidth(for text align)
# Usage

Place following line in your vim config:
```Vim
let gs#username='your github username'
" Max length of line, default is 100.
" If maxline is less than the longest repository name, only the repository name is shown.
" So you may set it to 0 to disable description.
let gs#maxline=80
```
Try:
```Vim
:LeaderfStars
```
Press `F1` to get more help

# LICENSE
MIT

