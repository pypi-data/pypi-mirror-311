# Author: kk.Fang(fkfkbill@gmail.com)

__all__ = [
    "get_bound_logger",
    "LoggerMixin",
]

import os
import glob
import traceback

import loguru._file_sink as file_sink
from loguru import logger

from .dt_utils import *

try:
    from django.conf import settings
    if not settings.LOG_NEED_STDOUT:
        # remove the default logging handler,
        # for avoiding print the logs to the stdout
        logger.remove(0)
except:
    pass


class FileSinkEx(file_sink.FileSink):
    """一个能够在rotation为True之后不会重命名旧文件（而以a模式重新打开写入）的FileSink"""

    def _terminate_file(self, *, is_rotating=False):
        old_path = self._file_path

        if self._file is not None:
            self._file.close()
            self._file = None
            self._file_path = None

        if is_rotating:
            new_path = self._prepare_new_path()

            # if new_path == old_path:
            #     creation_time = file_sink.get_ctime(old_path)
            #     root, ext = os.path.splitext(old_path)
            #     renamed_path = file_sink.generate_rename_path(root, ext, creation_time)
            #     os.rename(old_path, renamed_path)
            #     old_path = renamed_path
            # ^ 当新旧文件路径一致的时候，不要修改旧文件，而是直接写(默认以a方式打开)

        if is_rotating or self._rotation_function is None:
            if self._compression_function is not None and old_path is not None:
                self._compression_function(old_path)

            if self._retention_function is not None:
                logs = {
                    file
                    for pattern in self._glob_patterns
                    for file in glob.glob(pattern)
                    if os.path.isfile(file)
                }
                self._retention_function(list(logs))

        if is_rotating:
            file = open(new_path, **self._kwargs)
            file_sink.set_ctime(new_path, datetime.now().timestamp())

            self._file_path = new_path
            self._file = file


def get_bound_logger(module_name: str = None, **kwargs) -> logger:
    """
    产生一个带名称的日志控制器
    :param module_name: 日志的模块名，缺省尝试自动获取
    :param kwargs:
    :return:
    """
    if not module_name:
        module_name = traceback.extract_stack(3)[-2][1]
    # logger.add(
    #     FileSinkEx(
    #         Settings.LOG_FILE_DIR / "{time:YYYY-MM-DD}" / f"{module_name}.log",
    #         encoding='utf-8',
    #         rotation=timedelta(minutes=10.0)  # 10分钟检查一次日志是否需要切换
    #     ),
    #     filter=lambda x: x["extra"]["module_name"] == module_name,
    #     **kwargs
    # )
    return logger.bind(module_name=module_name)


class LoggerMixin(type):

    def __init__(cls, name, bases, attrs):

        super().__init__(name, bases, attrs)

        try:
            level = settings.LOG_LEVEL
        except:
            level = "info"

        # for logging
        cls.logger = get_bound_logger(name, level=level)
