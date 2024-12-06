#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, ItemsView, Iterable, Iterator, KeysView, Optional, Sequence, Type, TypeVar, Tuple, Union, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
from enum import Enum
import logging
from logging import Logger as PythonStandardLogger
from logging import StreamHandler, FileHandler, Formatter
from ..environment import Path
from .loglevel import LogLevel



#--------------------------------------------------------------------------------
# 로그 클래스.
#--------------------------------------------------------------------------------
class Logger():
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__logger: PythonStandardLogger
	__consoleHandler: StreamHandler
	__fileHandler: FileHandler
	__formatter: Formatter


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, logFilePath: str, level: LogLevel = LogLevel.DEBUG) -> None:

		path, name, extension = Path.GetPathNameExtensionFromFileFullPath(logFilePath)
		self.__logger: PythonStandardLogger = logging.getLogger(name)
		self.__logger.setLevel(level.value)
		self.__consoleHandler = StreamHandler()
		self.__fileHandler = FileHandler(logFilePath)
		self.__consoleHandler.setLevel(level.value)
		self.__fileHandler.setLevel(level.value)
		self.__formatter = Formatter("[%(asctime)s][%(name)s][%(levelname)s]%(message)s")
		self.__consoleHandler.setFormatter(self.__formatter)
		self.__fileHandler.setFormatter(self.__formatter)
		self.__logger.addHandler(self.__consoleHandler)
		self.__logger.addHandler(self.__fileHandler)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def __Log(self, level: LogLevel, message: object) -> None:
		if isinstance(message, str):
			if not message.startswith("["):
				message = f" {text}"
		else:
			text = str(message)
			if not text.startswith("["):
				message = f" {text}"

		self.__logger.log(level.value, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogDebug(self, message: object) -> None:
		self.__Log(LogLevel.DEBUG, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogInfo(self, message: object) -> None:
		self.__Log(LogLevel.INFO, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogWarning(self, message: object) -> None:
		self.__Log(LogLevel.WARNING, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogError(self, message: object) -> None:
		self.__Log(LogLevel.ERROR, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogException(self, message: object, *arguments) -> None:
		self.__logger.exception(message, *arguments, True, True, 8)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogCritical(self, message: object) -> None:
		self.__Log(LogLevel.CRITICAL, message)