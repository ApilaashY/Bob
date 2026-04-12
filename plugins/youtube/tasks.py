from pytubefix import YouTube
import certifi
import os


def download(url: str):
    os.environ['SSL_CERT_FILE'] = certifi.where()
    
    # Initialize YouTube object with a progress callback
    print("URL: ", url)
    yt = YouTube(url)

    # Get highest resolution stream and download
    ys = yt.streams.get_highest_resolution()
    ys.download()