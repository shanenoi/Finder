import os

vimrc = os.popen("printf $HOME/.vimrc").read()
source = open(vimrc).read()
if "Finder" not in source:
    open(vimrc, "a").write(
            f"\n\" For Finder" +
            f"\nlet g:source_path=\"{os.getcwd()}/find_and_edit.py\""
            f"\nsource {os.getcwd()}/main.vim"
    )
