import os, re
from io import BytesIO
from pathlib import Path
import zipfile
from typing import Union, IO, Tuple
import pandas as pd
import pyarrow.parquet as pq


class FileReader:
    def __init__(self, content: Union[str, Path, zipfile.ZipFile]):
        self.content = content
        self.is_dir = False
        self.is_zipfile = False
        self._available_exts = ('.csv', '.xlsx', '.parquet', '.json')
        self._prefix_file_pattern_regex = re.compile(r'^([A-Z]+)_\d+')
        self._check_content_type()
        self._check_extensions()

    def set_prefix_file_pattern_regex(self, regex: str):
        self._prefix_file_pattern_regex = re.compile(regex)

    def _check_content_type(self):
        if isinstance(self.content, (str, Path)):
            self.content = Path(self.content)
            self.is_dir = self.content.is_dir()
            if self.content.is_file() and self.content.suffix.lower() == '.zip':
                self.is_zipfile = True
                self.content = zipfile.ZipFile(self.content)
        elif isinstance(self.content, zipfile.ZipFile):
            self.is_zipfile, self.is_dir = True, False

    def _check_extensions(self):
        exts = set()
        if self.is_dir:
            exts = set([os.path.splitext(x)[1] for x in os.listdir(self.content)
                        if os.path.splitext(x)[1] != ''])
        elif self.is_zipfile:
            exts = set([os.path.splitext(x)[1] for x in self.content.namelist()
                        if os.path.splitext(x)[1] != ''])
        if len(exts) <= 0:
            raise Exception(f"No data found inside {self.content}")
        elif len(exts) > 1:
            raise Exception(f"Multiple file types found in content '{self.content}': {exts}")
        elif len(exts) == 1:
            ext_is_available = list(exts)[0] in self._available_exts
            if not ext_is_available:
                raise Exception(f"'{list(exts)[0]}' not available. The available file types are {', '.join(self._available_exts)}")

    def _get_files_to_read(self):
        if self.is_zipfile:
            return self.content.namelist()
        elif self.is_dir:
            return os.listdir(self.content)

    def _zip_file_reader(self, data: dict, file: str, **kwargs):
        filename, ext = os.path.splitext(file)
        if ext.lower() == '.csv':
            with self.content.open(file) as f:
                data[filename] = pd.read_csv(f, **kwargs)
        elif ext.lower() == '.xlsx':
            with self.content.open(file) as f:
                data[filename] = pd.read_excel(f, **kwargs)
        elif ext.lower() == '.parquet':
            with self.content.open(file) as f:
                data[filename] = pq.read_table(f, **kwargs).to_pandas()
        elif ext.lower() == '.json':
            with self.content.open(file) as f:
                data[filename] = pd.read_json(f, **kwargs)
        return data

    def _path_file_reader(self, data: dict, file: str, **kwargs):
        filename, ext = os.path.splitext(file)
        path_to_read = os.path.join(self.content, file)
        if ext.lower() == '.csv':
            data[filename] = pd.read_csv(path_to_read, **kwargs)
        elif ext.lower() == '.xlsx':
            data[filename] = pd.read_excel(path_to_read, **kwargs)
        elif ext.lower() == '.parquet':
            data[filename] = pq.read_table(path_to_read, **kwargs).to_pandas()
        elif ext.lower() == '.json':
            data[filename] = pd.read_json(path_to_read, **kwargs)
        return data

    def __get_file_pattern(self, filenames: list):
        prefixes = set([re.match(self._prefix_file_pattern_regex, filename).group(1) for filename in filenames if
                        re.match(self._prefix_file_pattern_regex, filename)])
        return prefixes

    def read_files(self,
                   join_prefixes: bool = False,
                   regex: bool = True,
                   join_custom_prefixes: Tuple[str] = None,
                   **kwargs):
        data = {}
        files = self._get_files_to_read()
        if self.is_zipfile:
            for file in files:
                data.update(self._zip_file_reader(data, file, **kwargs))
        elif self.is_dir:
            for file in files:
                data.update(self._path_file_reader(data, file, **kwargs))
        if join_prefixes:
            if not regex and join_custom_prefixes:
                unique_file_prefixes = set(join_custom_prefixes)
            else:
                unique_file_prefixes = self.__get_file_pattern(list(data.keys()))
            for prefix in unique_file_prefixes:
                file_prefixes = [x for x in data.keys() if prefix in x]
                data[prefix] = pd.concat([data[x] for x in file_prefixes], ignore_index=True)
                [data.pop(x) for x in file_prefixes]
                del file_prefixes
            return data
        else:
            return data
