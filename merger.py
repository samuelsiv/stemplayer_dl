from pydub import AudioSegment
import os,logging

files = {}

AudioSegment.converter = os.getcwd() + "\\ffmpeg.exe"

# thx kyiro

def merge(album, song):
    for file in os.scandir(f'{os.getcwd()}/Dump/{album}/{song}'):
        if not file.is_file():
            continue

        file_name = "{}.{}".format("_".join(file.name.split("_")[:-1]), file.name.split(".")[1])

        if not file_name in files:
            files[file_name] = []
            
        print(file.path)

        files[file_name].append(AudioSegment.from_file(file.path))

    for file in files:
        logging.debug(f"stem_merger: Merging file {file}")
        stems = files[file]
        x_song = stems[0]

        for stem in stems[1:]:
            x_song = x_song.overlay(stem)
            
        x_song.export(os.path.join(f'{os.getcwd()}/Dump/{album}/{song}', "song.flac"), format="flac")