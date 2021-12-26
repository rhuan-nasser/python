import os

usuario = os.environ['USERNAME']

cam_dir_downloads = fr'C:/Users/{usuario}/Downloads'
cam_dir_ISO = fr'C:/Users/{usuario}/Downloads/ISO'
cam_dir_ZIPADOS = fr'C:/Users/{usuario}/Downloads/ZIPADOS'
cam_dir_EXECUTÁVEIS = fr'C:/Users/{usuario}/Downloads/EXECUTÁVEIS'
cam_dir_ARQUIVOS_GERAIS = fr'C:/Users/{usuario}/Downloads/ARQUIVOS_GERAIS'
cam_dir_IMAGENS = fr'C:/Users/{usuario}/Downloads/IMAGENS'
cam_dir_VIDEOS_E_SONS = fr'C:/Users/{usuario}/Downloads/VIDEOS_E_SONS'

dir_downloads = os.listdir(cam_dir_downloads)

for arquivo in dir_downloads:

    if '.iso' in arquivo:
        if os.path.isdir(cam_dir_ISO):
            os.rename(fr'{cam_dir_downloads}/{arquivo}', fr'{cam_dir_downloads}/ISO/{arquivo}')
        if not os.path.isdir(cam_dir_ISO):
            os.mkdir(cam_dir_ISO)
            os.rename(fr'{cam_dir_downloads}/{arquivo}', fr'{cam_dir_downloads}/ISO/{arquivo}')

    if '.zip' in arquivo or '.7z' in arquivo or '.tar' in arquivo or '.TAR' in arquivo or '.rar' in arquivo:
        if os.path.isdir(cam_dir_ZIPADOS):
            os.rename(fr'{cam_dir_downloads}/{arquivo}', fr'{cam_dir_downloads}/ZIPADOS/{arquivo}')
        if not os.path.isdir(cam_dir_ZIPADOS):
            os.mkdir(cam_dir_ZIPADOS)
            os.rename(fr'{cam_dir_downloads}/{arquivo}', fr'{cam_dir_downloads}/ZIPADOS/{arquivo}')

    if '.msi' in arquivo or '.exe' in arquivo or '.EXE' in arquivo:
        if os.path.isdir(cam_dir_EXECUTÁVEIS):
            os.rename(fr'{cam_dir_downloads}/{arquivo}', fr'{cam_dir_downloads}/EXECUTÁVEIS/{arquivo}')
        if not os.path.isdir(cam_dir_EXECUTÁVEIS):
            os.mkdir(cam_dir_EXECUTÁVEIS)
            os.rename(fr'{cam_dir_downloads}/{arquivo}', fr'{cam_dir_downloads}/EXECUTÁVEIS/{arquivo}')

    if '.pdf' in arquivo or '.odf' in arquivo or '.txt' in arquivo or '.doc' in arquivo or '.docx' in arquivo\
            or '.accdb' in arquivo or '.xlsx' in arquivo or '.log' in arquivo or '.html' in arquivo\
            or '.pub' in arquivo or '.csv' in arquivo or '.pbix' in arquivo or '.odt' in arquivo or '.ods' in arquivo \
            or '.bpm' in arquivo:

        if os.path.isdir(cam_dir_ARQUIVOS_GERAIS):
            os.rename(fr'{cam_dir_downloads}/{arquivo}', fr'{cam_dir_downloads}/ARQUIVOS_GERAIS/{arquivo}')
        if not os.path.isdir(cam_dir_ARQUIVOS_GERAIS):
            os.mkdir(cam_dir_ARQUIVOS_GERAIS)
            os.rename(fr'{cam_dir_downloads}/{arquivo}', fr'{cam_dir_downloads}/ARQUIVOS_GERAIS/{arquivo}')

    if '.jpeg' in arquivo or '.JPEG' in arquivo or '.png' in arquivo or '.PNG' in arquivo or '.jpg' in arquivo\
            or '.JPG' in arquivo:
        if os.path.isdir(cam_dir_IMAGENS):
            os.rename(fr'{cam_dir_downloads}/{arquivo}', fr'{cam_dir_downloads}/IMAGENS/{arquivo}')
        if not os.path.isdir(cam_dir_IMAGENS):
            os.mkdir(cam_dir_IMAGENS)
            os.rename(fr'{cam_dir_downloads}/{arquivo}', fr'{cam_dir_downloads}/IMAGENS/{arquivo}')

    if '.mp4' in arquivo or '.mp3' in arquivo:
        if os.path.isdir(cam_dir_VIDEOS_E_SONS):
            os.rename(fr'{cam_dir_downloads}/{arquivo}', fr'{cam_dir_downloads}/VIDEOS_E_SONS/{arquivo}')
        if not os.path.isdir(cam_dir_VIDEOS_E_SONS):
            os.mkdir(cam_dir_VIDEOS_E_SONS)
            os.rename(fr'{cam_dir_downloads}/{arquivo}', fr'{cam_dir_downloads}/VIDEOS_E_SONS/{arquivo}')