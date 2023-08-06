from aclib.pyi import compile, pyipack

compile(
    srcdir='src',
    dstdir='compiled',
    exclude_scripts=['main.py'],
    dst_replace_confirm=False
)

pyipack(
    scriptpath='compiled/main.py',
    distdir='dist',
    appname='showtext',
    appversion='',
    appicon='',
    exename='launcher',
    show_console=True,
    admin_permission=True,
    one_file_mode=False,
    appfiles=['assets'],
    dst_replace_confirm=True
)
