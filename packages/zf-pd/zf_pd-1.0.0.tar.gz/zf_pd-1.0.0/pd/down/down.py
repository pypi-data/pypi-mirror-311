from click import group
from click import option
from loguru import logger
from pytubefix import YouTube
from pytubefix.cli import on_progress

from .libgen import download_book
from .youtube import get_script


@group(name='down', help="Download from the internet")
def down():
    pass


@down.command(help="Download a YouTube video")
@option('-l', '--link', type=str, required=True, prompt=True,
        help="Link to the YouTube video (e.g. https://www.youtube.com/watch?v=...)")
@option('-f', '--format', type=str, required=True, prompt=True,
        help="Format to download as (e.g. mp4, mp3, txt)")
def youtube(link: str, format: str):
    logger.debug("down video")

    if format == 'mp4':
        logger.info("Downloading highest resolution video in mp4")
        yt = YouTube(link, on_progress_callback=on_progress)
        ys = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        ys.download()
    elif format == 'mp3':
        logger.info("Downloading highest quality audio in mp3")
        yt = YouTube(link, on_progress_callback=on_progress)
        ys = yt.streams.get_audio_only()
        ys.download(mp3=True)
    elif format == 'webm':
        logger.info("Downloading highest quality audio in webm")
        yt = YouTube(link, on_progress_callback=on_progress)
        ys = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        ys.download()
    elif format == 'txt':
        logger.info("Downloading transcript of YouTube video")
        title, script = get_script(link)
        with open(f"{title}.txt", 'w') as f:
            f.write(script)
    else:
        logger.error(f"Unsupported format {format}")


@down.command(help="Download a book from Libgen")
@option('-n', '--name', type=str, required=True, prompt=True,
        help="Author name")
@option('-t', '--title', type=str, required=True, prompt=True,
        help="Book title")
def libgen(name: str, title: str):
    logger.debug("down book")
    download_book(name, title)
