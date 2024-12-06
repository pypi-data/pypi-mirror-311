import asyncio
import logging
import time
import traceback
from collections.abc import Coroutine
from datetime import datetime
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING, cast

from raphson_music_client.track import DownloadedTrack
import vlc
from raphson_music_client import RaphsonMusicClient
from requests import RequestException

from .config import Config
from .downloader import Downloader

if TYPE_CHECKING:
    from tempfile import \
        _TemporaryFileWrapper  # pyright: ignore[reportPrivateUsage]


_LOGGER = logging.getLogger(__name__)


class AudioPlayer():
    temp_file: '_TemporaryFileWrapper[bytes] | None' = None
    downloader: 'Downloader'
    client: RaphsonMusicClient
    currently_playing: DownloadedTrack | None = None
    vlc_instance: vlc.Instance
    vlc_player: vlc.MediaPlayer
    vlc_events: vlc.EventManager
    start_timestamp: int = 0
    news: bool
    last_news: int

    def __init__(self,
                 client: RaphsonMusicClient,
                 downloader: 'Downloader',
                 config: Config):
        self.client = client
        self.downloader = downloader
        self.news = config.news
        self.last_news = int(time.time())  # do not queue news right after starting

        self.vlc_instance = vlc.Instance('--file-caching=0')
        self.vlc_player = self.vlc_instance.media_player_new()
        self.vlc_events = self.vlc_player.event_manager()

    async def setup(self):
        asyncio.create_task(self._now_playing_submitter())
        self.vlc_events.event_attach(vlc.EventType.MediaPlayerEndReached, self.on_media_end, asyncio.get_running_loop())

    async def on_media_end_async(self) -> None:
        tasks: list[Coroutine[None, None, None]] = []
        # save current info before it is replaced by the next track
        if self.currently_playing and self.currently_playing.track:
            path = self.currently_playing.track.path
            start_timestamp = self.start_timestamp
            tasks.append(self.client.submit_played(path, start_timestamp))
        tasks.append(self.next(retry=True))
        await asyncio.gather(*tasks)

    def on_media_end(self, event, loop: asyncio.AbstractEventLoop):
        _LOGGER.info('Media ended, play next')
        async def create_task():
            await loop.create_task(self.on_media_end_async())
        asyncio.run_coroutine_threadsafe(create_task(), loop)

    def stop(self):
        try:
            self.vlc_player.stop()
            self.vlc_player.set_media(None)
            self.currently_playing = None
        finally:
            if self.temp_file:
                self.temp_file.close()

    def pause(self):
        self.vlc_player.set_pause(True)
        asyncio.create_task(self._submit_now_playing())

    async def play(self):
        if self.has_media():
            self.vlc_player.play()
            asyncio.create_task(self._submit_now_playing())
        else:
            await self.next()

    async def next(self, retry: bool = False, force_news: bool = False) -> None:
        if force_news:
            await self.downloader.enqueue_news()
        elif self.news:
            minute = datetime.now().minute
            # a few minutes past the hour and last news played more than 30 minutes ago?
            if minute > 11 and minute < 20 and time.time() - self.last_news > 30*60:
                # Attempt to download news. If it fails, next retry news won't be
                # downloaded again because last_news is updated
                self.last_news = int(time.time())
                try:
                    await self.downloader.enqueue_news()
                except:
                    traceback.print_exc()

        download = self.downloader.get_track()

        if not download:
            _LOGGER.warning('No cached track available')
            if retry:
                _LOGGER.info('Retry enabled, going to try again')
                time.sleep(5)
                self.next(retry)
            return

        self.currently_playing = download
        self.start_timestamp = int(time.time())
        if download.track:
            _LOGGER.info('Playing track: %s', download.track.path)
        else:
            _LOGGER.info('Playing virtual track')
        temp_file = NamedTemporaryFile('wb', prefix='rmp-playback-server-')

        try:
            temp_file.truncate(0)
            temp_file.write(download.audio)

            media = self.vlc_instance.media_new(temp_file.name)
            self.vlc_player.set_media(media)
            self.vlc_player.play()
        finally:
            # Remove old temp file
            if self.temp_file:
                self.temp_file.close()
            # Store current temp file so it can be removed later
            self.temp_file = temp_file

        asyncio.create_task(self._submit_now_playing())

    def has_media(self) -> bool:
        return self.vlc_player.get_media() is not None

    def is_playing(self) -> bool:
        return cast(int, self.vlc_player.is_playing()) == 1

    def position(self) -> int:
        return cast(int, self.vlc_player.get_time()) // 1000

    def duration(self) -> int:
        return cast(int, self.vlc_player.get_length()) // 1000

    def seek(self, position: int):
        _LOGGER.info('Seek to:', position)
        self.vlc_player.set_time(position * 1000)

    def volume(self) -> int:
        return self.vlc_player.audio_get_volume()

    def set_volume(self, volume: int) -> None:
        self.vlc_player.audio_set_volume(volume)

    async def _submit_now_playing(self):
        if self.has_media() and self.currently_playing and self.currently_playing.track:
            await self.client.submit_now_playing(self.currently_playing.track.path,
                                        self.position(),
                                        not self.is_playing())

    async def _now_playing_submitter(self):
        while True:
            try:
                await self._submit_now_playing()
            except RequestException:
                _LOGGER.warning('Failed to submit now playing info')

            if self.is_playing():
                await asyncio.sleep(10)
            else:
                await asyncio.sleep(60)
