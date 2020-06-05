let g:leaderf_github_stars_username = get(g:, 'leaderf_github_stars_username', executable('git') ? system('git config --global user.name') : expand('$USER'))

command! -bar -nargs=0 LeaderfStars call leaderf#Stars#startExpl(g:Lf_WindowPosition)
command! -bar -nargs=0 LeaderfStarsRemoveCache call leaderf#Stars#removeCache()

call g:LfRegisterSelf("LeaderfStars", "navigate the stars")
