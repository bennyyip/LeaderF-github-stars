command! -bar -nargs=0 LeaderfStars call leaderf#Stars#startExpl(g:Lf_WindowPosition)
command! -bar -nargs=0 LeaderfStarsRemoveCache call leaderf#Stars#removeCache()

call g:LfRegisterSelf("LeaderfStars", "navigate the stars")
