if leaderf#versionCheck() == 0
    finish
endif

exec g:Lf_py "import vim, sys, os.path"
exec g:Lf_py "cwd = vim.eval('expand(\"<sfile>:p:h\")')"
exec g:Lf_py "sys.path.insert(0, os.path.join(cwd, 'python'))"
exec g:Lf_py "from starsExpl import *"

function! leaderf#Stars#Maps()
    nmapclear <buffer>
    nnoremap <buffer> <silent> <F1>          :exec g:Lf_py "starsExplManager.toggleHelp()"<CR>
    nnoremap <buffer> <silent> <F5>          :exec g:Lf_py "starsExplManager.refresh()"<CR>
    nnoremap <buffer> <silent> o             :exec g:Lf_py "starsExplManager.accept()"<CR>
    nnoremap <buffer> <silent> <2-LeftMouse> :exec g:Lf_py "starsExplManager.accept()"<CR>
    nnoremap <buffer> <silent> q             :exec g:Lf_py "starsExplManager.quit()"<CR>
    nnoremap <buffer> <silent> i             :exec g:Lf_py "starsExplManager.input()"<CR>
endfunction

function! leaderf#Stars#removeCache(...)
    call leaderf#LfPy('starsExplManager.removeCache()')
endfunction

function! leaderf#Stars#startExpl(win_pos, ...)
    call leaderf#LfPy("starsExplManager.startExplorer('".a:win_pos."')")
endfunction

function! leaderf#Stars#open(filename) abort
  let filename = fnamemodify(a:filename, ':p')

  let s:is_windows = has('win32') || has('win64')
  let s:is_unix = has('unix')
  let s:is_cygwin = has('win32unix')
  let s:is_mac = !s:is_windows && !s:is_cygwin
        \ && (has('mac') || has('macunix') || has('gui_macvim') ||
        \   (!isdirectory('/proc') && executable('sw_vers')))

  " Detect desktop environment.
  if s:is_windows
    " For URI only.
    " Note:
    "   # and % required to be escaped (:help cmdline-special)
    silent execute printf(
          \ '!start rundll32 url.dll,FileProtocolHandler %s',
          \ escape(filename, '#%'),
          \)
  elseif s:is_cygwin
    " Cygwin.
    call system(printf('%s %s', 'cygstart',
          \ shellescape(filename)))
  elseif executable('xdg-open')
    " Linux.
    call system(printf('%s %s &', 'xdg-open',
          \ shellescape(filename)))
  elseif executable('lemonade')
    call system(printf('%s %s &', 'lemonade open',
          \ shellescape(filename)))
  elseif exists('$KDE_FULL_SESSION') && $KDE_FULL_SESSION ==# 'true'
    " KDE.
    call system(printf('%s %s &', 'kioclient exec',
          \ shellescape(filename)))
  elseif exists('$GNOME_DESKTOP_SESSION_ID')
    " GNOME.
    call system(printf('%s %s &', 'gnome-open',
          \ shellescape(filename)))
  elseif executable('exo-open')
    " Xfce.
    call system(printf('%s %s &', 'exo-open',
          \ shellescape(filename)))
  elseif s:is_mac && executable('open')
    " Mac OS.
    call system(printf('%s %s &', 'open',
          \ shellescape(filename)))
  else
    " Give up.
    throw 'Not supported.'
  endif
endfunction



function! leaderf#Stars#register(name)
exec g:Lf_py "<< EOF"
from leaderf.anyExpl import anyHub
anyHub.addPythonExtension(vim.eval("a:name"), starsExplManager)
EOF
endfunction
