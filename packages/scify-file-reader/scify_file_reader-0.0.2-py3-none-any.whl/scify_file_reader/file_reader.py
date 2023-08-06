import os
import re
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Union, IO, Tuple
import pandas as pd
import pyarrow.parquet as pq


class FileReader:
    """
    A class to handle and process multiple files with identical structures within a directory or a zip archive.

    Args:
        content (Union[str, Path, zipfile.ZipFile]): The content to read. It can be a string representing
            a file path, a Path object, or a zipfile.ZipFile object.

    Attributes:
        content (Union[str, Path, zipfile.ZipFile]): The content to read.
        is_dir (bool): Indicates if the content is a directory.
        is_zipfile (bool): Indicates if the content is a zip archive.
        _available_exts (Tuple[str]): Available file extensions to consider when reading files.
        _prefix_file_pattern_regex (re.Pattern): Regular expression pattern for file prefixes.
    """

    def __init__(self, content: Union[str, Path, zipfile.ZipFile]):
        self.content = content
        self.is_dir = False
        self.is_zipfile = False
        self._available_exts = ('.csv', '.xlsx', '.parquet', '.json')
        self._prefix_file_pattern_regex = re.compile(r'^([A-Z]+)_\d+')
        self._check_content_type()
        self._check_extensions()

    def set_prefix_file_pattern_regex(self, regex: str):
        """
        Set a custom regular expression pattern for file prefixes.

        Args:
            regex (str): The custom regular expression pattern.
        """
        self._prefix_file_pattern_regex = re.compile(regex)

    def _check_content_type(self):
        """
        Check the type of the content (directory or zip archive) and update the corresponding attributes.
        """
        if isinstance(self.content, (str, Path)):
            self.content = Path(self.content)
            self.is_dir = self.content.is_dir()
            if self.content.is_file() and self.content.suffix.lower() == '.zip':
                self.is_zipfile = True
                self.content = zipfile.ZipFile(self.content)
        elif isinstance(self.content, zipfile.ZipFile):
            self.is_zipfile, self.is_dir = True, False

    def _check_extensions(self):
        """
        Check the available file extensions in the content and validate if they are supported.
        """
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
        """
        Get the files to read based on the content type.

        Returns:
            List[str]: List of file names to read.
        """
        if self.is_zipfile:
            return self.content.namelist()
        elif self.is_dir:
            return os.listdir(self.content)

    def _zip_file_reader(self, data: dict, file: str, **kwargs):
        """
        Read a file from a zip archive and add it to the data dictionary.

        Args:
            data (dict): Dictionary to store the file data.
            file (str): File name to read.
            **kwargs: Additional arguments to pass to the pandas read methods.

        Returns:
            dict: Updated data dictionary.
        """
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
        """
        Read a file from a directory and add it to the data dictionary.

        Args:
            data (dict): Dictionary to store the file data.
            file (str): File name to read.
            **kwargs: Additional arguments to pass to the pandas read methods.

        Returns:
            dict: Updated data dictionary.
        """
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
        """
        Get the unique file patterns based on the file names.

        Args:
            filenames (list): List of file names.

        Returns:
            set: Set of unique file patterns.
        """
        prefixes = set([re.match(self._prefix_file_pattern_regex, filename).group(1) for filename in filenames if
                        re.match(self._prefix_file_pattern_regex, filename)])
        return prefixes

    def read_files(self,
                   join_prefixes: bool = False,
                   regex: bool = True,
                   join_custom_prefixes: Tuple[str] = None,
                   **kwargs):
        """
        Read and process the files.

        Args:
            join_prefixes (bool, optional): Whether to join files with the same prefix into a single DataFrame.
                Defaults to False.
            regex (bool, optional): Whether to use regular expressions to identify file prefixes. Defaults to True.
            join_custom_prefixes (Tuple[str], optional): Custom prefixes to join together. Defaults to None.
            **kwargs: Additional arguments to pass to the pandas read methods.

        Returns:
            dict: A dictionary where the keys are the filenames (or prefixes if join_prefixes is True) and
                the values are pandas DataFrames containing the file data.
        """
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
