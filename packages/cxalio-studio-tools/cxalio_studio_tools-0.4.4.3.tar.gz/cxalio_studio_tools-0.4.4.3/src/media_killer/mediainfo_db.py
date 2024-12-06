import csv
import heapq
import json
import threading
from collections import defaultdict
from functools import cache
from pathlib import Path
from typing import Union, Iterable

from ffmpeg import FFmpeg

from cx_core import DataPackage
from cx_core.filesystem import ensure_folder, CommandChecker
from .env import env


class MediaInfoDB:
    __duration_cache = defaultdict(float)
    __count_cache = defaultdict(int)
    __cache_lock = threading.Lock()
    __cache_filename = 'media_duration_cache.csv'

    @classmethod
    def insert_record(cls, key: str, value: float):
        with cls.__cache_lock:
            cls.__duration_cache[key] = value
            cls.__count_cache[key] = 1
        return value

    @classmethod
    def find_record(cls, key: str):
        if key in cls.__duration_cache:
            cls.__count_cache[key] = cls.__count_cache[key] + 1
            return cls.__duration_cache[key]
        return None

    @classmethod
    def load_caches(cls, cache_folder: Path = None):
        cache_folder = ensure_folder(cache_folder if cache_folder else Path.cwd())
        cache_file = cache_folder / cls.__cache_filename
        if not cache_file.exists():
            return
        with cls.__cache_lock:
            with open(cache_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 3:
                        continue
                    key = str(row[0])
                    count = int(row[1])
                    duration = float(row[2])
                    cls.__count_cache[key] = count
                    cls.__duration_cache[key] = duration
            env.debug(f'已从[yellow]{cache_file}[/yellow]中加载[red]{len(cls.__count_cache)}[/red]条缓存数据')

    @classmethod
    def save_caches(cls, cache_folder: Path = None):
        cache_folder = ensure_folder(cache_folder if cache_folder else Path.cwd())
        cache_folder.mkdir(parents=True,exist_ok=True)
        cache_file = cache_folder / cls.__cache_filename

        record_length = min(9999, len(cls.__count_cache))
        sorted_keys = heapq.nlargest(record_length, cls.__count_cache.items(), key=lambda x: x[1])
        keys = [item[0] for item in sorted_keys]
        with open(cache_file, 'w', encoding='utf-8',newline='') as file:
            writer = csv.writer(file)
            for key in keys:
                row = [key, cls.__count_cache[key], cls.__duration_cache[key]]
                writer.writerow(row)
        env.debug(f'已将[red]{len(keys)}[/red]条缓存保存到[yellow]{cache_file}[/yellow]')

    def __init__(self, executable=None):
        self._executable = str(executable) if executable else None

    @property
    @cache
    def ffprobe_executable(self) -> str:
        if not self._executable:
            return ''
        exe = str(self._executable).replace('ffmpeg', 'ffprobe')
        checker = CommandChecker(exe)
        return checker.executable()

    def __probe_duration(self, source: Path) -> float:
        source = Path(source)
        result = 1
        try:
            if self.ffprobe_executable:
                ff = FFmpeg(executable=str(self.ffprobe_executable))
                ff.input(source.resolve(), print_format='json', show_format=None)
                data = json.loads(ff.execute())
                mediainfo = DataPackage(**data)
                result = float(mediainfo.format.duration or 0)
        finally:
            return result

    def get_duration(self, source: Path) -> float:
        key = str(source.resolve())
        record = MediaInfoDB.find_record(key)
        if not record:
            record = MediaInfoDB.insert_record(key, self.__probe_duration(source))
        return record

    def get_durations(self, source: Union[Path | Iterable]) -> float:
        sources = []
        if isinstance(source, Iterable):
            sources = [Path(str(x)) for x in source]
        else:
            sources = [Path(str(source))]

        durations = map(self.get_duration, sources)
        return max(durations)
