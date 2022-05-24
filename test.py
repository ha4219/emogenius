from matplotlib import font_manager
import matplotlib as mpl


for font in font_manager.fontManager.ttflist:
    if 'hangul' in font.name:
        print(font.name, font.fname)

print ('버전: ', mpl.__version__)
print ('설치 위치: ', mpl.__file__)
print ('설정 위치: ', mpl.get_configdir())
print ('캐시 위치: ', mpl.get_cachedir())

print ('설정파일 위치: ', mpl.matplotlib_fname())
