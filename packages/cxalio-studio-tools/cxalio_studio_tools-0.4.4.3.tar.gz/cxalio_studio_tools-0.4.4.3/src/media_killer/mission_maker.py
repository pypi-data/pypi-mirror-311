import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from cx_core.filesystem import normalize_path
from cx_core.misc import DataPackage
from cx_core.misc.misc_utils import limit_number
from cx_core.text import TagReplacer
from cx_core.text.text_utils import unquote_text, split_at_unquoted_spaces
from .env import env
from .mediainfo_db import MediaInfoDB


class OptionPackage:
    def __init__(self, filename=None):
        self.data = defaultdict(list)
        self.filename = Path(filename) if filename else None

    @staticmethod
    def __format_key(k: str):
        key = str(k).strip()
        if key.startswith("-"):
            key = key[1:]
        return key

    @staticmethod
    def __format_value(v):
        value = str(v) if v else ""
        return unquote_text(value)

    def insert(self, key, value=None):
        k = OptionPackage.__format_key(key)
        v = OptionPackage.__format_value(value) if value else None
        if v:
            self.data[k].append(v)
        elif k not in self.data:
            self.data[k] = []
        return self

    def iter_options(self):
        for k, vs in self.data.items():
            if not vs:
                yield k, None
            else:
                for v in vs:
                    yield k, v

    def iter_arguments(self):
        for k, v in self.iter_options():
            yield "-" + k
            yield v

    def __rich_repr__(self):
        yield "filename", self.filename
        yield "options", self.data


@dataclass
class Mission:
    source: Path = None
    ffmpeg: str = None
    overwrite: bool = None
    target_folder: Path = None
    general: OptionPackage = None
    inputs: list[OptionPackage] = None
    outputs: list[OptionPackage] = None
    duration: float = None

    def __rich_repr__(self):
        yield "Mission"
        yield "Source", self.source
        yield "target_folder", self.target_folder
        yield "general", self.general.iter_arguments()
        yield "inputs", self.inputs
        yield "outputs", self.outputs

    def iter_output_filenames(self):
        for x in self.outputs:
            yield x.filename

    def iter_input_filenames(self):
        for x in self.inputs:
            yield x.filename

    @staticmethod
    def __test_duration(ff: str, source: str) -> float:
        pattern = re.compile(r"Duration: \d\d:\d\d:\d\d\.\d\d")
        tc_pattern = re.compile(r"(\d\d):(\d\d):(\d\d)[^\d](\d\d)")
        dur = 0
        try:
            result = subprocess.run([ff, "-i", source])
            time_str = pattern.search(result.stderr)
            _, h, m, s, f = tc_pattern.match(time_str)
            time = int(h) * 60 * 60 + int(m) * 60 + int(s) + (int(f) / 100)
            dur = float(time)
        except Exception as e:
            env.debug(e)
            env.warning(f"任务[cyan]{Path(source).name}[/cyan]无法获取时长")
        finally:
            return dur


class MissionCompiler:
    class OptionParser:
        def __init__(self, options):
            self._options = options

        @staticmethod
        def _iter_list(elements: list):
            prev_token = None
            for t in elements:
                token = str(t).strip()
                if token.startswith("-"):
                    if prev_token:
                        yield prev_token, None
                        prev_token = None
                    else:
                        prev_token = token[1:]
                else:
                    if prev_token:
                        yield prev_token, token
                        prev_token = None
                    else:
                        env.debug(f"忽略无法识别的参数： {token}")
            if prev_token:
                yield prev_token, None

        @staticmethod
        def _iter_dict(elements: dict):
            for k, v in elements.items():
                yield k, v

        def __iter__(self):
            if isinstance(self._options, list):
                return self._iter_list(self._options)
            if isinstance(self._options, dict | DataPackage):
                return self._iter_dict(self._options)
            return self._iter_list(split_at_unquoted_spaces(str(self._options)))

    def __init__(self, source: Path, profile: DataPackage) -> None:
        self.source = Path(source)
        self.profile = profile
        self.replacer = TagReplacer(keep_unknown_tags=False)
        self.replacer.install_data_source(
            "source", self.__datahandler_source
        ).install_data_source("target", self.__datahandler_target).install_data_source(
            "source_parent", self.__datahandler_sourceparent
        ).install_data_source(
            "target_parent", self.__datahandler_targetparent
        ).install_data_source(
            "profile", self.__datahandler_profile
        ).install_data_source(
            "custom", self.__datahandler_custom
        )

    @property
    @cache
    def target(self) -> Path:
        profile_target_folder = self.replacer(self.profile.target.folder)
        target_folder = normalize_path(profile_target_folder)

        t_suffix = self.profile.target.suffix
        if not t_suffix.startswith("."):
            t_suffix = "." + t_suffix

        p_folder = Path()
        p_level = self.profile.target.keep_parent_level
        if p_level > 0:
            parents = self.source.parent.parts
            selected_parts = parents[-1 * p_level:]
            p_folder = Path(*selected_parts)
            env.debug(f"取用 {p_level} 个上级目录：{p_folder}")

        result = target_folder / p_folder / self.source.name
        return result.with_suffix(t_suffix)

    @cache
    def __datahandler_source(self, param=None):
        match param:
            case "absolute":
                return str(self.source.absolute())
            case "dot_suffix":
                return str(self.source.suffix)
            case "suffix":
                return str(self.source.suffix)[1:]
            case "parent":
                return str(self.source.parent)
            case "parent_name":
                return str(self.source.parent.stem)
            case "name":
                return str(self.source.name)
            case "basename":
                return str(self.source.stem)
            case _:
                return str(self.source)

    @cache
    def __datahandler_target(self, param=None):
        match param:
            case "absolute":
                return str(self.target.absolute())
            case "dot_suffix":
                return str(self.target.suffix)
            case "suffix":
                return str(self.target.suffix)[1:]
            case "parent":
                return str(self.target.parent)
            case "parent_name":
                return str(self.target.parent.stem)
            case "name":
                return str(self.target.name)
            case "basename":
                return str(self.target.stem)
            case _:
                return str(self.target)

    @cache
    def __datahandler_sourceparent(self, param=None):
        level = int(param) if param else 1
        ps = self.source.parent.parts
        level = limit_number(level, 1, len(ps))
        selected_parts = ps[-1 * level:]
        return str(Path(*selected_parts))

    @cache
    def __datahandler_targetparent(self, param=None):
        level = int(param) if param else 1
        ps = self.target.parent.parts
        level = limit_number(level, 1, len(ps))
        selected_parts = ps[-1 * level:]
        return str(Path(*selected_parts))

    @cache
    def __datahandler_profile(self, param=None):
        match param:
            case "id":
                return str(self.profile.general.profile_id)
            case "name":
                return str(self.profile.general.name)
            case "desc":
                return str(self.profile.general.description)
            case "ffmpeg":
                return str(self.profile.general.ffmpeg)
            case _:
                return str(self.profile.path.basename)

    @cache
    def __datahandler_custom(self, param=None):
        if param:
            return self.profile.get(f"custom.{str(param)}", str(param))
        return str(param)

    def __parse_general_table(self, general_table: DataPackage):
        result = OptionPackage()
        option_pairs = MissionCompiler.OptionParser(general_table.options)
        for k, v in option_pairs:
            value = self.replacer(v)
            result.insert(k, value)

        if general_table.hardware_accelerate:
            result.insert("hwaccel", general_table.hardware_accelerate)

        overwrite_option = "-y" if general_table.overwrite else "-n"
        result.insert(overwrite_option)
        return result

    def __parse_io_table(self, io_table: DataPackage) -> OptionPackage:
        filename = self.replacer(io_table.filename)
        result = OptionPackage(filename=filename)
        opt_parser = MissionCompiler.OptionParser(io_table.options)
        for k, v in opt_parser:
            result.insert(k, self.replacer(v))
        return result

    def compile(self) -> Mission:
        result = Mission(
            source=self.source,
            ffmpeg=str(self.profile.general.ffmpeg),
            overwrite=self.profile.general.overwrite,
            target_folder=Path(self.profile.target.folder),
            general=self.__parse_general_table(self.profile.general),
        )
        result.inputs = [self.__parse_io_table(i) for i in self.profile.input]
        result.outputs = [self.__parse_io_table(o) for o in self.profile.output]
        # result.duration = self.durationManager.duration(result.iter_input_filenames())
        return result


class MissionMaker:
    def __init__(self, profile: DataPackage):
        self.profile = profile
        self.durationDB = MediaInfoDB(self.profile.general.ffmpeg)
        self.task = None

    def __enter__(self):
        self.task = env.progress.add_task(description=f'为配置[green]<{self.profile.general.name}>[/green]创建任务…',
                                          total=None)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        env.progress.remove_task(self.task)
        return False

    def make_mission(self, source: Path) -> Mission:
        env.progress.update(self.task, description=f'为[cyan]{source.name}[/cyan]编译任务内容…')
        compiler = MissionCompiler(source, self.profile)
        result = compiler.compile()
        env.progress.update(self.task, description=f'为[cyan]{result.source.name}[/cyan]计算时长…')
        result.duration = self.durationDB.get_durations(result.iter_input_filenames())
        return result
