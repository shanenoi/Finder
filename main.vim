function! Fs(type_window, type_search, values, excludes)
python3 << EOF
import vim
import sys
import os

def vim_index_input():
    vim.command(f"let b:index = input('index: ')")
    return vim.eval("b:index")

def vim_editor_vertical_mode(path):
    vim.command(f"vs {path}")

def vim_editor_horizonal_mode(path):
    vim.command(f"sp {path}")

MAP_WINDOW = {"v": vim_editor_vertical_mode,
              "h": vim_editor_horizonal_mode}

source_path = vim.eval("g:source_path")
type_search = vim.eval("a:type_search")
type_window = vim.eval("a:type_window")
values = vim.eval("a:values")
_ = vim.eval("a:excludes")
excludes = [] if not _ else _.split(" ")

sys.path.append(os.path.dirname(source_path))
Finder = __import__(os.path.splitext(os.path.basename(source_path))[0])
Finder.disable_color()

if type_search == "n":
    Finder.FindByName(values, excludes)\
        .find(index_input=vim_index_input,
              editor=MAP_WINDOW[type_window])
elif type_search == "c":
    Finder.FindByContent(values, excludes)\
        .find(index_input=vim_index_input,
              editor=MAP_WINDOW[type_window])

EOF
endfunction

function! Fv(type_search, values, excludes)
    call Fs("v", a:type_search, a:values, a:excludes)
endfunction


function! Fh(type_search, values, excludes)
    call Fs("h", a:type_search, a:values, a:excludes)
endfunction
