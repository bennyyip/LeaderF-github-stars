let g:gs#username = get(g:, 'gs#username', executable('git') ? system('git config --global user.name') : expand('$USER'))

command! -bar -nargs=0 LeaderfStars call leaderf#Stars#startExpl(g:Lf_WindowPosition)
command! -bar -nargs=0 LeaderfStarsRemoveCache call leaderf#Stars#removeCache()

call g:LfRegisterSelf("LeaderfStars", "navigate the stars")
