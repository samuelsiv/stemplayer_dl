from utils import get_track, get_albums, download_stems
from multiprocessing import Process
import logging
import argparse
import warnings

warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--album", help="Album to download",
                    required=False)
parser.add_argument("-m", "--merge", help="Should merge songs",
                    required=False)
parser.add_argument("-d", "--debug", help="Should debug logs",
                    required=False)
args = parser.parse_args()


def dump_all():
    albums = get_albums()

    for album in albums:
        album = albums[album]

        logging.info("Parsing album {}".format(album["title"]))
        for track in album["tracks"]:
            logging.info(
                "  Downloading track {} from {}.".format(
                    album["title"], track["metadata"]["title"]
                )
            )
            data = get_track(track["id"], track["version"])

            p = Process(
                target=download_stems,
                args=(
                    data,
                    album["title"],
                    track["metadata"]["title"],
                    track["metadata"]
                ),
            )
            p.start()

            processes.append(p)

    logging.info(
        "Enqueued all tracks for download! \
        Please wait until the program stops."
    )
    for p in processes:
        p.join()


processes = []


def dump_one(album_name):
    albums = get_albums()

    album = albums[album_name]

    logging.info("Parsing album {}".format(album["title"]))
    for track in album["tracks"]:
        logging.info(
            "  Downloading track {} from {}.".format(
                album["title"], track["metadata"]["title"]
            )
        )
        data = get_track(track["id"], track["version"])

        p = Process(
            target=download_stems,
            args=(
                data,
                album["title"],
                track["metadata"]["title"],
                track["metadata"]
            ),
        )
        p.start()

        processes.append(p)

    logging.info(
        "Enqueued all tracks for download! \
        Please wait until the program stops."
    )
    for p in processes:
        p.join()


if __name__ == "__main__":
    if (args.debug):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info("stemdumper v3")

    if (args.album):
        dump_one(args.album)
    else:
        dump_all()
