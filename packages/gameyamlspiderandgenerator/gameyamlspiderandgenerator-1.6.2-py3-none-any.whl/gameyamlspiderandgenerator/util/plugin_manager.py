import importlib
from typing import Literal, Type, Union

from loguru import logger

from ..hook import BaseHook
from ..plugin import BasePlugin
from ..util.config import config


class Package:
    plugin: dict[str, BasePlugin] = {}
    hook: dict[str, BaseHook] = {}
    log: list[str] = []

    def __init__(self):
        self.load_plugins()
        self.load_hooks()

    def __getitem__(self, item):
        # Compatibility with the old version
        return self.__getattribute__(item)

    def __setitem__(self, key, value):
        # Compatibility with the old version
        self.__setattr__(key, value)

    def _load(
            self,
            _dir: Literal["plugin", "hook"],
            _type: Union[Type[BasePlugin], Type[BaseHook]],
    ):
        def find_subclasses(module, base_class):
            # 导入模块

            # 获取模块中所有的类
            classes = module.__dict__.values()

            # 过滤出继承了指定基类的子类
            subclasses = [cls for cls in classes if isinstance(cls, type) and issubclass(cls, base_class)]

            return subclasses
        if _dir == "plugin":
            base = __package__.split(".")[0] + "." + _dir
        else:
            base= 'yamlgenerator_{}_hook'
        if config[_dir] is None:
            if None not in self["log"]:
                logger.warning(f"All {_dir}s are disabled")
                self["log"].append(None)
            return

        for plugin in getattr(config, _dir, []):
            if plugin.startswith("_"):
                logger.warning(f"Skip loading protected {_dir} {plugin}")
                continue
            try:
                if _dir == "plugin":
                    package = f"{base}.{plugin}"
                else:
                    package = base.format(plugin)
                if plugin in self["log"]:
                    continue
                logger.info(f"Loading {_dir}: {plugin}")
                temp = importlib.import_module(package)
                self[_dir][plugin] = find_subclasses(temp,_type)[0]
                self["log"].append(temp.__name__.split(".")[-1])
            except ImportError as e:
                logger.trace(e)
                logger.error(f"Failed to import {_dir}: {plugin}")
            except IndexError:
                logger.error(f"Imported {_dir} but no {_type.__name__} found: {plugin}")

    def load_plugins(self):
        self._load("plugin", BasePlugin)

    def load_hooks(self):
        self._load("hook", BaseHook)


pkg = Package()
