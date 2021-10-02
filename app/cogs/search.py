import pprint
from typing import Union, List

from discord_slash.client import SlashCommand
from discord_slash.context import SlashContext
from cogs import Song
import config
from youtube_dl import YoutubeDL
import json

pp = pprint.PrettyPrinter(indent=2)


class YoutubeSearch:
    YTDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True", "logger": config.ytdl_logger}

    def __init__(self) -> None:
        pass

    @classmethod
    def search_song(cls, song: str, multiple=False, max_entries=10) -> Union[List[Song], bool]:
        with YoutubeDL(cls.YTDL_OPTIONS) as ytdl:
            try:
                results = ytdl.extract_info(f"ytsearch:{song}", download=False)["entries"]
                info = results[0]
            except Exception:
                return False
        if multiple:
            song_results = []
            for song in results[: min(len(results), max_entries)]:
                song_results.append(
                    Song(
                        _source=info["formats"][0]["url"],
                        title=info["title"],
                        _thumbnail=info["thumbnails"][1]["url"],
                        web_url=info["webpage_url"],
                        duration=info["duration"],
                    )
                )
            return song_results

        return [
            Song(
                _source=info["formats"][0]["url"],
                title=info["title"],
                _thumbnail=info["thumbnails"][1]["url"],
                web_url=info["webpage_url"],
                duration=info["duration"],
            )
        ]

    @classmethod
    def search_playlist(cls, playlist_url: str, ctx: SlashContext) -> Union[Song, bool]:
        options = cls.YTDL_OPTIONS.copy()
        options["noplaylist"] = False
        options["extract_flat"] = True

        with YoutubeDL(options) as ytdl:
            try:
                results = ytdl.extract_info(
                    playlist_url,
                    download=False,
                )
                pp.pprint(
                    ytdl.extract_info(f"https://youtube.com/watch?v={results['entries'][0]['url']}", download=False)
                )
            except Exception as e:
                config.logger.debug(f"Error searching youtube for playslist: \n{e}")
                return False
        song_results = []
        for song in results["entries"]:
            song_results.append(
                Song(
                    _source="",
                    title=song["title"],
                    _thumbnail="",
                    web_url=f"https://youtube.com/v/{song['url']}",
                    duration=int(song["duration"]),
                )
            )

        return song_results
