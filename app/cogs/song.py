from dataclasses import dataclass
from typing import Union, Optional

from discord.embeds import Embed
import cogs


@dataclass
class Song:
    title: str
    _source: str
    _thumbnail: str
    web_url: str
    duration: int
    _embed: Optional[Embed] = None

    def load_missing_data(self):
        track_info = cogs.YoutubeSearch.search_song(self.web_url)[0]
        self._source = track_info.source
        self._thumbnail = track_info._thumbnail
        self.duration = track_info.duration
        self.title = track_info.title

    @property
    def thumbnail(self) -> str:
        if not self._thumbnail:
            self.load_missing_data()
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, v: str):
        self._thumbnail = v

    @property
    def source(self) -> str:
        if not self._source:
            self.load_missing_data()
        return self._source

    @source.setter
    def source(self, v: str):
        self._source = v

    @property
    def embed(self) -> Embed:
        if not self._embed:
            embed = Embed(title=self.title, url=self.web_url)
            embed.set_thumbnail(url=self.thumbnail)
            embed.add_field(name="Length", value=self.duration_time)
            self._embed = embed
        return self._embed

    @property
    def duration_time(self) -> str:
        return self.calc_duration_time(self.duration)

    @staticmethod
    def calc_duration_time(duration_int: int) -> str:
        duration = {}
        duration["hours"], rem = divmod(duration_int, 3600)
        duration["minutes"], duration["seconds"] = divmod(rem, 60)
        if duration["hours"] > 0:
            return f"{duration['hours']:02}:{duration['minutes']:02}:{duration['seconds']:02}"
        return f"{duration['minutes']:02}:{duration['seconds']:02}"
