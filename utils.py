from functools import wraps
import json
from typing import Callable, Union
import pandas as pd
from pathlib import Path


def makedir(path:Union[str,Path], remove_filename:bool=False, recursive:bool=True, exist_ok:bool=True)->None:
	"""Creates directory from path if not exists.

	:param path: Path of the directory to be created.
	:type path: str
	:param remove_filename: If set to True, it attempts to remove the filename from
		the path, defaults to False
	:type remove_filename: bool, optional
	:param recursive: Creates directories recursively (i.e., create necessary 
		subdirectories if necessary), defaults to True
	:type recursive: bool, optional
	:param exist_ok: is set to False, arises an error if `path` directory exists,
		defaults to True
	:type exist_ok: bool, optional
	"""
	# Ensure it is a PurePath
	path = Path(path)
	
	if remove_filename: path = path.parent

	path.mkdir(parents=recursive, exist_ok=exist_ok)