from pytube import YouTube
import os
import re
import keyboard

def folderInitializer():
    if os.path.exists('downloads') == False:
        os.mkdir('downloads')


def urlReceiver():
    url = urlFilter(input('\nEnter Video URL:\n'))
    if url == '':
        return url
    
    if urlValidity(url) == False:
        print("\nInvalid URL, try again")
        return urlReceiver()

    return url

def urlValidity(url):
    try:
        YouTube(url)
        return True
    except:
        return False

def urlFilter(url):
    url = list(url)
    if len(url) == 0 : return ''
    if url[0] == "'" and url[-1] == "'":
        url = url[1:-1]
    elif url[0] == '"' and url[-1] == '"':
        url = url[1:-1]
    return ''.join(url)


def titleMaker(ytTitle):
    return ' '.join(list(filter(lambda x: x != '' ,re.split(r'[\"\'\`\/\|\\\s]',ytTitle))))


def fileNameMaker(path, title, extsn, count = 1):
    repeatCount = ''
    if count > 1:
        repeatCount = f'({count})'
    
    fileName = f'{title+repeatCount}.{extsn}'

    if os.path.exists(f'{path}\\{fileName}'):
        return fileNameMaker(path, title, extsn, count + 1)
    else:
        return fileName



def downloader(url,single = True):
    folderInitializer()
    
    yt = YouTube(url)
    audio = yt.streams.get_audio_only()
    extnsn = audio.mime_type.split("/")[1]
    
    title = titleMaker(yt.title)
    fileName = fileNameMaker('downloads',title, extnsn)
    
    print(f'Downloading {fileName}')
    audio.download(filename = f'downloads\\{fileName}')

    print(f'\nDownload complete')
    print(f"Video saved as '{fileName}' in downloads\n")
    if single:
        print('\nPress Enter to download another video\nPress esc to exit')

def main():
    downloadPattern = input('Download multiple files?[y/n]\n')

    if downloadPattern == 'n' :
        url = urlReceiver()
        downloader(url)
    elif downloadPattern == 'y' :
        listURL = []
        print('\nEnter a url. Then press Enter to add another\nEnter blank url to stop')
        while True:
            url = urlReceiver()
            if url == '':
                break
            else:
                listURL.append(url)

        for url in listURL:
            downloader(url,False)
        print('\nPress Enter to download another video\nPress esc to exit')
        
        
    else:
        print("Enter 'y' or 'n' only\n  y stands for yes\n  n stands for no")
        main()

main()

while True:
    if keyboard.is_pressed('esc'):
        print('\nProgram finished')
        quit()
    if keyboard.is_pressed('enter'):
        input()
        print('\nStarting program\n')
        main()

#https://www.youtube.com/watch?v=jrrfu1BWpBg