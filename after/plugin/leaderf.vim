" Definition of 'arguments' can be similar as
" https://github.com/Yggdroot/LeaderF/blob/master/autoload/leaderf/Any.vim#L85-L140
let s:extension = {
      \   "name": "stars",
      \   "help": "navigate starred github repos",
      \   "manager_id": "leaderf#Stars#managerId",
      \   "arguments": [
      \   ]
      \ }


" In order that `Leaderf stars` is available
call g:LfRegisterPythonExtension(s:extension.name, s:extension)

command! -bar -nargs=0 LeaderfStarsRemoveCache call leaderf#Stars#removeCache()

command! -bar -nargs=0 LeaderfStars Leaderf stars

