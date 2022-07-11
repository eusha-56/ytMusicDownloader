from pytube import YouTube
import os
import re
import keyboard

def folderInitializer():                                #initializes required folder.
    if os.path.exists('downloads') == False:
        os.mkdir('downloads')


def urlReceiver(single = True):                         #single means url is received for single file download           
    url = urlFilter(input('\nEnter Video URL:\n'))      #receives and filters url
    if single == False and url == '':                                       #
        return url
    
    if urlValidity(url) == False:                       #checks if url exists
        print("\nInvalid URL, try again")
        return urlReceiver()

    return url

def urlValidity(url):                                   #url validity checker
    try:
        YouTube(url)
        return True
    except:
        return False

def urlFilter(url):                                     #removes inverted coma from url
    url = list(url)
    if len(url) == 0 : return ''
    if url[0] == "'" and url[-1] == "'":
        url = url[1:-1]
    elif url[0] == '"' and url[-1] == '"':
        url = url[1:-1]
    return ''.join(url)


def titleModifier(ytTitle):                                #modifies youtube title to avoid string error
    return ' '.join(list(filter(lambda x: x != '' ,re.split(r'[\"\'\`\/\|\\\s]',ytTitle))))


def fileNameMaker(path, title, extsn, count = 1):          #if same file exists it renames the download file
    repeatCount = ''
    if count > 1:
        repeatCount = f'({count})'
    
    fileName = f'{title+repeatCount}.{extsn}'

    if os.path.exists(f'{path}\\{fileName}'):
        return fileNameMaker(path, title, extsn, count + 1)
    else:
        return fileName



def downloader(url):                                        #downloads the audio
    folderInitializer()
    
    yt = YouTube(url)                                       #loads the youtube object
    audio = yt.streams.get_audio_only()                     #gets best audio stream
    extnsn = audio.mime_type.split("/")[1]                  #gets audio extension
    
    title = titleModifier(yt.title)                         #modifies yt title
    fileName = fileNameMaker('downloads',title, extnsn)     #concats title and etension, modifies if same file exists
    
    print(f'Downloading {fileName}')
    audio.download(filename = f'downloads\\{fileName}')     #downloads in the download folder

    print(f'\nDownload complete')
    print(f"Audio saved as '{fileName}' in downloads\n")


def main():
    downloadPattern = input('Download multiple files?[y/n]\n')          #checks if user want to download multiple files or single file

    if downloadPattern == 'n' :                                         #doanloads single file
        url = urlReceiver()
        downloader(url)
        print('\nPress Enter to download files again\nPress esc to exit')
    elif downloadPattern == 'y' :                                       #downloads multiple files
        listURL = []                                                    #list of urls
        print('\nEnter a url. Then press Enter to add another\nEnter blank url to stop')
        while True:                                                     #continues to receive urls and push to listURL as long as user enters blank url
            url = urlReceiver()
            if url == '':
                break
            else:
                listURL.append(url)

        for url in listURL:                                             #for each url runs the downloader function
            downloader(url,False)
        print('\nPress Enter to download files again\nPress esc to exit')
        
        
    else:                                                               #if user presses wrong key in downloadPattern it runs the main function again
        print("Enter 'y' or 'n' only\n  y stands for yes\n  n stands for no")
        main()

main()

while True:                                                             #after completing main function it checks if user want to run the function again
    if keyboard.is_pressed('esc'):
        print('\nProgram finished')
        quit()                                                          
    if keyboard.is_pressed('enter'):
        input()                                                         #extra input function to neutralize the enter
        print('\nStarting program\n')
        main()

#https://www.youtube.com/watch?v=jrrfu1BWpBg