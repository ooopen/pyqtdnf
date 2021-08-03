if __name__ == '__main__':
    from PyInstaller.__main__ import run
    #opts=['music.py','--path=C:\\Python35\\Lib\\site-packages\\PyQt5\\Qt\\bin','--clean','-y']
    opts=[
        'DnfNew.py',
        '--clean',
        '-y',#覆盖
        '-w',#调试模式
        '-F',#是否单exe
        '--add-data=dnfimg/*;./dnfimg/',
        '--add-data=ui/*;./ui/',

    ]
    run(opts)