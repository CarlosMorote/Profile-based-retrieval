from functools import wraps
import json
from typing import Callable
import pandas as pd
from pathlib import Path

CONFIG = dict(
	# Useful columns for fine-tuning.
	cols=["id", "summary", "text"]
)

def remove_filename_from_path(out_filename:str, path_standard_format:bool=False)->str:
    """Attempts to remove filename from the provided path.

    :param out_filename: Filepath.
    :type out_filename: str
    :param path_standard_format: Indicates whether the path follows the standard
     format (backslash separator) or the slash separator, defaults to False.
    :type path_standard_format: bool, optional
    :return: The directory excluding the filename.
    :rtype: str
    """
    if path_standard_format or '\\' in out_filename:
        out_filename = out_filename.replace('\\', '/')
    return (out_filename if '/' not in out_filename else
        out_filename.replace(out_filename.split('/')[-1], ''))

def makedir(path:str, remove_filename:bool=False, recursive:bool=True, exist_ok:bool=True, **kwargs)->None:
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
    if '/' in path or '\\' in path:
        path = path if not remove_filename else remove_filename_from_path(path, **kwargs)
        Path(path).mkdir(parents=recursive, exist_ok=exist_ok)


def write_json(i,article, abstract, base_dir="summaries/tokenized/"):
	""" Saves a json file."""

	with open(f'{base_dir}{i}.json', 'w') as f:
		json.dump(
			dict(
				id=i,
				article=article,
				abstract=abstract
			), 
			f, ensure_ascii=False)

def get_tokenized_text(text:str, tokenizer, convert_ids_to_tokens=False):
	"""Get the list of tokens in `text`

	:param text: Text to tokenize
	:type text: str
	:param tokenizer: Instance of `BertTokenizer` class. If `None`, it loads the
		predefined tokenizer of 'bert-base-uncased'.
	:type tokenizer: BertTokenizer, optional
	:return: list of tokens.
	:rtype: list
	"""
	ids = tokenizer.encode(text)

	# Return list of tokens in `text`.
	return ids if not convert_ids_to_tokens else tokenizer.convert_ids_to_tokens(ids)


#Not used
def load_json_data(func:Callable) -> Callable:
	"""Load json data from disk

	:param func: callable function
	:type func: Callable
	"""
	@wraps(func)
	def inner(filepath, *args, **kwargs):
		data = pd.read_json(filepath, lines=True)[CONFIG["cols"]]
		return func(data, filepath, *args, **kwargs)
	return inner
