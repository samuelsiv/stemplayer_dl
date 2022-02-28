from utils import get_track, get_albums, download_stems
import logging
from multiprocessing import Process

# Change this to logging.debug for debug logs
logging.basicConfig(level=logging.INFO)


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
                args=(data, album["title"], track["metadata"]["title"]),
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


def dump_one(album_name="donda_2"):
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
            args=(data, album["title"], track["metadata"]["title"]),
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
    logging.info("stemdumper v3")
    dump_one()
