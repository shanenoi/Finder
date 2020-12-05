function! Fs(type_search, values, excludes)
python3 << EOF
import vim
import sys
import os

source_path = vim.eval("g:source_path")
type_search = vim.eval("a:type_search")
values = vim.eval("a:values")
excludes = vim.eval("a:excludes")

sys.path.append(os.path.dirname(source_path))
Finding = __import__(os.path.splitext(os.path.basename(source_path))[0])
Finding.disable_color()

result_arrays = Finding.main([
    f"v{type_search}",
    values,
    excludes.split(" ")
])

vim.command(f"let b:results = {result_arrays}")
EOF
    return b:results
endfunction


function! InputValidatetion(exp)
python3 << EOF
import vim
var = 1 if vim.eval("a:exp").isdigit() else 0
vim.command(f"let b:result =  {var}")
EOF
    return b:result
endfunction

function! UnletVar()
    unlet b:results
    unlet b:index
    unlet b:result
endfunction


function! Fv(type_search, values, excludes)
    let b:results = Fs(a:type_search, a:values, a:excludes)
    let b:index = input("index: ")
    if InputValidatetion(b:index) == 1
        execute "vs " . b:results[str2nr(b:index)]
        call UnletVar()
    endif
endfunction


function! Fh(type_search, values, excludes)
    let b:results = Fs(a:type_search, a:values, a:excludes)
    let b:index = input("index: ")
    if InputValidatetion(b:index) == 1
        execute "sp " . results[str2nr(b:index)]
        call UnletVar()
    endif
endfunction
