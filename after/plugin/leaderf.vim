command! -bar -nargs=0 LeaderfStars call leaderf#Stars#startExpl(g:Lf_WindowPosition)

" In order to be listed by :LeaderfSelf
call g:LfRegisterSelf("LeaderfStars", "navigate stars repos")

" Definition of 'arguments' can be similar as
" https://github.com/Yggdroot/LeaderF/blob/master/autoload/leaderf/Any.vim#L85-L140
let s:extension = {
            \   "name": "stars",
            \   "help": "navigate stars repos",
            \   "registerFunc": "leaderf#Stars#register",
            \   "arguments": [
            \   ]
            \ }
" In order that `Leaderf stars` is available
call g:LfRegisterPythonExtension(s:extension.name, s:extension)
