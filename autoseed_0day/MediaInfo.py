# mediainfo ny by diexiaomou@NYPT ftdlyc@NYPT
# 2017.12.29

from MediaInfoDLL3 import *
import sys


def get_mediainfo(path):
    mi = MediaInfo()
    mi.Open(path)

    name = mi.Get(Stream.General, 0, "FileName")
    time = mi.Get(Stream.General, 0, "Encoded_Date")
    during = mi.Get(Stream.General, 0, "Duration/String3")
    size = mi.Get(Stream.General, 0, "FileSize/String")
    container = mi.Get(Stream.General, 0, "Format")

    code1 = mi.Get(Stream.Video, 0, "Encoded_Library_Name")
    code2 = mi.Get(Stream.Video, 0, "Format_Profile")
    code3 = mi.Get(Stream.Video, 0, "BitRate/String")
    code = code1 + ' ' + code2 + ' ' + code3.replace(' ', '')

    fps = mi.Get(Stream.Video, 0, "FrameRate/String")
    hight = mi.Get(Stream.Video, 0, "Height")
    width = mi.Get(Stream.Video, 0, "Width")
    fbl = width + ' x ' + hight

    audio_count = int(mi.Get(Stream.General, 0, "AudioCount"))
    audio_list = []
    for i in range(0, audio_count):
        audio1 = mi.Get(Stream.Audio, 0, "Language/String")
        if audio1 == '':
            audio1 = 'Chinese'
        audio2 = mi.Get(Stream.Audio, 0, "Format")
        audio3 = mi.Get(Stream.Audio, 0, "Channel(s)/String")
        audio4 = mi.Get(Stream.Audio, 0, "BitRate/String")
        audio = audio1 + ' ' + audio2 + ' ' + audio3 + ' @ ' + audio4
        audio_list.append(audio)
    if len(audio_list) == 1:
        audio_text = 'AUDIO..........: ' + audio_list[0]
    else:
        audio_text = 'AUDIO' + str(1) + '.........: ' + audio_list[0]
        for i in range(2, len(audio_list) + 1):
            audio_text = '\n' + audio_text + 'AUDIO' + str(i) + '.........: ' + audio_list[i - 1]

    text_count = mi.Get(Stream.General, 0, "TextCount")
    if text_count.strip() != '':
        text_count = int(text_count)
        text_list = []
        for i in range(0, text_count):
            text1 = mi.Get(Stream.Text, 0, "Language/String")
            if text1 == '':
                text1 = 'Chinese'
            text2 = mi.Get(Stream.Text, 0, "Format")
            text = text1 + ' / ' + text2
            text_list.append(text)
        if len(text_list) == 1:
            text_text = 'SUBTITLES......: ' + text_list[0]
        else:
            text_text = 'SUBTITLES' + str(1) + '.....: ' + text_list[0]
            for i in range(2, len(text_list) + 1):
                text_text = text_text +'\n'+ 'SUBTITLES' + str(i) + '.....: ' + text_list[i - 1]
    else:
        text_text = ''

    has_chapter = mi.Get(Stream.General, 0, "MenuCount")
    if has_chapter.strip() != '':
        chapter = 'None'
    else:
        chapter = 'Included'

    mi.Close()

    content = '''[font=Courier New][code]RELEASE.NAME...: {name}
RELEASE.TIME...: {time}
DURATION.......: {during}
SIZE...........: {size}
CONTAINER......: {container}
VIDEO.CODEC....: {code}
FRAME.RATE.....: {fps}
RESOLUTION.....: {fbl}
{audio}{text}
CHAPTERS.......: {chapter}[/code][/font]'''.format(
        name=name,
        time=time,
        during=during,
        size=size,
        container=container,
        code=code,
        fps=fps,
        fbl=fbl,
        audio=audio_text,
        text=text_text,
        chapter=chapter
    )

    return content


if __name__ == '__main__':
    content = get_mediainfo(sys.argv[1])
    print(content)
    over = input()
