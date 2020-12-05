# Finder
_migrating from gist ..._

> This extension I created when I was using Vim as the main IDE

### Components
 - main.vim
 - schedule_source/find_and_edit.py

_Fjnd by c0nt3nt 0r b9 n@m3_

### How to user
_Implement in console mode_
```vim
:call Fv('n', '.py$', 'git log test')
" Explain:
"   n                  -> find by name
"   '.py$'             -> part name
"   'git log test'     -> excludes

:call Fh('n', '.py$', 'git log test')
" Explain:
"   c                  -> find by content
"   'def index'        -> content
"   'git log test'     -> excludes
```
