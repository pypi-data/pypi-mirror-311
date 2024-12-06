import pkgutil
from argparse import ArgumentParser

from appdirs import AppDirs
from ffmpeg import FFmpegError
from rich.markdown import Markdown
from rich.panel import Panel
from rich_argparse import RichHelpFormatter

from cx_core.app import AbstractApp, LogLevel
from cx_core.filesystem.path_utils import *
from cx_core.misc import DataPackage
from cx_core.tui import JobCounter
from .env import env
from .exceptions import *
from .mediainfo_db import MediaInfoDB
from .mission_maker import MissionMaker, Mission
from .profile_loader import ProfileLoader
from .script_writer import ScriptWriter
from .source_detector import SourceDetector
from .transcoder import Transcoder


# from .utils import FFmpegChecker


class MediaKillerApp(AbstractApp):
    APP_VERSION = "0.4.4.3"
    APP_NAME = "mediakiller"

    def __init__(self):
        super(MediaKillerApp, self).__init__()

        _parser = ArgumentParser(
            prog=MediaKillerApp.APP_NAME,
            formatter_class=RichHelpFormatter,
            description="批量转码工具",
            epilog=f"Version {MediaKillerApp.APP_VERSION} Designed by xiii_1991",
        )

        _parser.add_argument(
            "sources",
            help="指定需要处理的文件，其中必须包含至少一个配置文件",
            default=None,
            metavar="需要处理的路径",
            nargs="*",
        )
        _parser.add_argument(
            "-g",
            "--generate",
            action="store_true",
            dest="generate_example",
            help="生成范例配置文件",
        )
        _parser.add_argument(
            "-s",
            "--make-script",
            dest="script_output",
            metavar="脚本文件路径",
            help="生成对应的脚本文件",
        )
        _parser.add_argument(
            "-o",
            "--output",
            dest="output_dir",
            metavar="输出位置",
            help="指定输出目录",
            default=".",
        )
        _parser.add_argument(
            "-c",
            "--continue",
            dest="continue_mode",
            action="store_true",
            help="继续未完成的任务",
        )
        _parser.add_argument(
            "--no-sort", dest="no_sort", action="store_true", help="禁用任务自动排序"
        )
        _parser.add_argument(
            "--pretend",
            "-p",
            dest="pretend_mode",
            action="store_true",
            help="空转模式，模拟执行",
        )
        _parser.add_argument(
            "-d", "--debug", action="store_true", dest="debug", help="显示调试信息"
        )
        _parser.add_argument(
            "--full-help", help="显示详细的说明", dest="full_help", action="store_true"
        )
        _parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=MediaKillerApp.APP_VERSION,
            help="显示软件版本信息",
        )

        self.parser = _parser
        self.profile = None
        self.args = None
        self.global_task = None
        self.appdirs = AppDirs(MediaKillerApp.APP_NAME)

    def __enter__(self):
        env.start()
        env.print(
            f"[yellow]{MediaKillerApp.APP_NAME}[/yellow] [blue]{MediaKillerApp.APP_VERSION}[/blue]"
        )

        _args = self.parser.parse_args()
        self.args = DataPackage(**vars(_args))
        env.log_level = LogLevel.DEBUG if self.args.debug else LogLevel.WARNING
        env.debug("解析命令行参数：", self.args)

        self.global_task = env.progress.add_task("全局进度", start=False, visible=False)

        MediaInfoDB.load_caches(self.appdirs.user_cache_dir)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        env.progress.stop_task(self.global_task)
        env.progress.update(self.global_task,description=f'保存元数据缓存…',total=None)
        MediaInfoDB.save_caches(self.appdirs.user_cache_dir)

        result = False
        if exc_type is None:
            pass
        elif issubclass(exc_type, CxException):
            env.error(exc_val)
            result = True
        env.progress.stop_task(self.global_task)
        env.progress.remove_task(self.global_task)
        env.stop()
        return result

    @staticmethod
    def copy_example_profile(to):
        to = normalize_path(to)
        to = force_suffix(to, ".toml")
        data = pkgutil.get_data("media_killer", "example_project.toml")
        try:
            with open(to, "xb") as file:
                file.write(data)
            env.print(f"配置文件{to.name}已初始化，[red]请在修改后运行[/red]")
        except FileExistsError:
            env.error(
                f"文件 [yellow]{to.name}[/yellow] 已存在，请手动删除或指定其它目标文件"
            )

    @staticmethod
    def show_full_help():
        data = pkgutil.get_data("media_killer", "help.md").decode("utf_8")
        panel = Panel(Markdown(data), width=80)
        env.console.print(panel)

    def _load_profiles(self) -> list[DataPackage]:
        env.progress.update(self.global_task, description="检测配置文件…")
        profiles = []
        pro_files = set()
        for s in self.args.sources:
            source = Path(s)
            if not source.is_file():
                continue
            if not source.suffix:
                source = source.with_suffix('.toml')
            if source.suffix == ".toml" and source.exists():
                pro_files.add(source)
        env.print(f"在输入中发现[green]{len(pro_files)}[/green]个配置文件")
        for a in pro_files:
            with ProfileLoader(a, self.args) as loader:
                loaded_profile = loader.load()
                if not loaded_profile.general.ffmpeg:
                    env.error(
                        f"配置文件[green]{p.general.name}[/green]中的[red]ffmpeg[/red]路径非法，将忽略此配置文件"
                    )
                    break
                profiles.append(loaded_profile)
        if len(profiles) == 0:
            raise NoProfileError("没有指定配置文件，无法执行任务")
        return profiles

    def _detect_sources(self) -> list[Path]:
        env.progress.update(self.global_task, description="探测源文件…")
        result = []
        sources = set(filter(lambda x: Path(x).suffix != ".toml", self.args.sources))
        source_count = len(sources)
        env.print(f"发现[cyan]{source_count}[/cyan]个来源路径")
        with SourceDetector(self.args) as detector:
            for s in sources:
                detector.detect(s)
            result = detector.arrange_tasks()
        result_count = len(result)
        if result_count != source_count:
            env.print(f"展开后探测到[cyan]{result_count}[/cyan]个源文件")
        return result

    def _make_missions(
            self, profiles: list[DataPackage], sources: list[Path]
    ) -> list[Mission]:
        missions = []
        env.progress.update(
            self.global_task,
            description="制定计划中…",
            completed=0,
            total=len(profiles) * len(sources),
        )
        for profile in profiles:
            with MissionMaker(profile) as maker:
                for source in sources:
                    missions.append(maker.make_mission(source))
                    env.progress.advance(self.global_task)
        total_count = len(missions)
        env.print(
            f"为[green]{len(profiles)}[/green]个配置文件生成了[yellow]{total_count}[/yellow]个任务"
        )

        if self.args.continue_mode:
            env.debug("检测到继续模式，开始检查已完成的任务")
            env.progress.update(
                self.global_task, description="检测已完成的任务…", total=None
            )
            filtered_missions = [
                m
                for m in missions
                if not all([x.exists() for x in m.iter_output_filenames()])
            ]
            env.print(
                f"已移除[red]{total_count - len(filtered_missions)}[/red]项已完成的任务"
            )
            missions = filtered_missions

        if not self.args.no_sort:
            env.progress.update(self.global_task, description="正在按路径对任务排序…")
            missions.sort(key=lambda x: str(x.source.resolve()))

        return missions

    @staticmethod
    def _count_duration(missions: list[Mission]) -> float:
        if not missions or len(missions) == 0:
            return 0
        durations = [float(x.duration) for x in missions]
        env.print(durations)
        return sum(durations)

    def _pretend_run_missions(self, missions: list[Mission]):
        mission_count = len(missions)
        env.progress.update(
            self.global_task, description="假装执行任务…", total=mission_count
        )
        job_counter = JobCounter(mission_count)
        for m in missions:
            if env.wanna_quit:
                raise UserCanceledError("用户取消了执行")
            job_counter.advance()
            filenames = [str(x.filename) for x in m.outputs]
            for name in filenames:
                env.print(
                    f"[yellow]{job_counter}[/yellow] 假装生成了 [cyan]{name}[/cyan]"
                )
            env.progress.advance(self.global_task)

    def _export_script(self, missions: list[Mission], script: Path):
        script = Path(script)
        env.progress.update(self.global_task, description="生成脚本文件…", total=None)
        with ScriptWriter(script) as writer:
            writer.write_all(missions)

    def _transcode(self, missions: list[Mission]):
        total_duration = sum([x.duration for x in missions])
        env.print(f"媒体总时长为：[yellow]{total_duration:.2f}[/yellow]秒")
        env.progress.update(self.global_task, total=total_duration, completed=0)
        job_counter = JobCounter(len(missions))
        for m in missions:
            mission_name = m.source.name
            if env.wanna_quit:
                env.print("取消未完成的任务…")
                raise UserCanceledError("用户取消了执行")
            has_error = False
            try:
                with Transcoder(m) as coder:
                    coder.run()
            except FFmpegError as e:
                env.error(f"FFMPEG运行出错 ：[red]{e.message}[/red]")
                has_error = True

            job_counter.advance()
            env.progress.update(self.global_task, advance=m.duration)
            if has_error:
                env.print(
                    f"[yellow]{job_counter}[/yellow] [red]{mission_name}[/red] 未正确执行"
                )
            else:
                env.print(
                    f"[yellow]{job_counter}[/yellow] [cyan]{mission_name}[/cyan] 执行完毕"
                )

    def run(self):
        if self.args.full_help:
            env.info("检测到full_help，打印帮助文件并输出")
            MediaKillerApp.show_full_help()
            return

        if not self.args.sources:
            env.info("指定的路径为空")
            raise NoSourcesError("未指定任何文件，你想做什么？")

        if self.args.generate_example:
            MediaKillerApp.copy_example_profile(self.args.sources[0])
            return

        env.progress.update(self.global_task, visible=True, total=None)
        env.progress.start_task(self.global_task)

        profiles = self._load_profiles()
        total_sources = self._detect_sources()
        missions = self._make_missions(profiles, total_sources)

        env.progress.start_task(self.global_task)
        env.progress.update(
            self.global_task,
            description="总体进度",
        )

        if self.args.pretend_mode:
            env.print("启用了干转模式，将会假装执行")
            self._pretend_run_missions(missions)
            return

        if self.args.script_output:
            env.debug(
                f"指定了脚本目标[cyan]{self.args.script_output}[/cyan]，将会生成脚本文件"
            )
            self._export_script(missions, self.args.script_output)

        else:
            self._transcode(missions)


def run():
    with MediaKillerApp() as media_killer:
        media_killer.run()
