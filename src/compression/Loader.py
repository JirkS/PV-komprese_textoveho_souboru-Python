import json
import os
from src.security import Logger


class Loader:
    def __init__(self, logger: Logger):
        self._logger = logger

    def check_text_file_path(self, file_path: str):
        """
        checking if path of text file is correct
        :param file_path: path to text file
        :return:
        """
        if not file_path.lower().endswith('.txt'):
            self._logger.log_error(f"ValueError: Invalid file type. Expected a .txt file, but got: {file_path}")
            raise ValueError(f"Invalid file type. Expected a .txt file, but got: {file_path}")
        if not os.path.exists(file_path):
            self._logger.log_error(f"FileNotFoundError: File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

    def check_json_file_path(self, file_path: str):
        """
        checking if path of json file is correct
        :param file_path: path to json file
        :return:
        """
        if not file_path.lower().endswith('.json'):
            self._logger.log_error(f"ValueError: Invalid file type. Expected a .json file, but got: {file_path}")
            raise ValueError(f"Invalid file type. Expected a .json file, but got: {file_path}")
        if not os.path.exists(file_path):
            self._logger.log_error(f"FileNotFoundError: File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

    def load_hint(self, file_path: str) -> list:
        """
        loads text/rows/hints from text file
        :param file_path: path to hint text file
        :return: list of rows/hints
        """
        self.check_text_file_path(file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self._logger.log_info(f"File hint successfully loaded!")
                tmp_list_of_rows = []
                for i, line in enumerate(file, 1):
                    tmp_list_of_rows.append(str(line))
            self._logger.log_info("Data of hint loaded into list!")
            return tmp_list_of_rows
        except PermissionError:
            self._logger.log_error(f"PermissionError: Unable to read the file '{file_path}'.")
            raise PermissionError(f"Unable to read the file '{file_path}'.")

    def load_rows_of_text_file(self, file_path: str) -> list:
        """
        loads text/rows from text file, which will be compressed
        :param file_path: path to text file, which will be compressed
        :return: list of rows from text file
        """
        self.check_text_file_path(file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                size_of_file = os.path.getsize(file_path)
                self._logger.log_info(f"File text successfully loaded with original size: {size_of_file} bytes!")
                tmp_list_of_rows = []
                for i, line in enumerate(file, 1):
                    tmp_list_of_rows.append(str(line))
            self._logger.log_info("Data of text file loaded into list!")
            return tmp_list_of_rows
        except PermissionError:
            self._logger.log_error(f"PermissionError: Unable to read the file '{file_path}'.")
            raise PermissionError(f"Unable to read the file '{file_path}'.")

    def load_useless_words(self, useless_words_path: str) -> list:
        """
        loads useless words from json file
        :param useless_words_path: path to json file of useless words
        :return: list of useless words
        """
        self.check_json_file_path(useless_words_path)
        try:
            with open(useless_words_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                tmp_list_of_useless_words = []
                for i in range(10):
                    words_str = data.get(str(i), "")
                    if words_str != "":
                        tmp_list_of_useless_words.extend(words_str.split(", "))
        except PermissionError:
            self._logger.log_error(f"PermissionError: Unable to read the file '{useless_words_path}'.")
            raise PermissionError(f"Unable to read the file '{useless_words_path}'.")
        return tmp_list_of_useless_words

    def load_abbreviations(self, abbreviations_path: str) -> dict:
        """
        loads abbreviations from json file
        :param abbreviations_path: path to json file of abbreviations
        :return: dictionary of words and abbreviations
        """
        self.check_json_file_path(abbreviations_path)
        try:
            with open(abbreviations_path, 'r', encoding='utf-8') as file:
                tmp_dic_of_abbreviations = json.load(file)
        except PermissionError:
            self._logger.log_error(f"PermissionError: Unable to read the file '{abbreviations_path}'.")
            raise PermissionError(f"Unable to read the file '{abbreviations_path}'.")
        return tmp_dic_of_abbreviations

    def load_couplings(self, couplings_path: str) -> dict:
        """
        loads couplings words
        :param couplings_path: path of json file of couplings words
        :return: dictionary of words and abbreviations
        """
        self.check_json_file_path(couplings_path)
        try:
            with open(couplings_path, 'r', encoding='utf-8') as file:
                tmp_dic_of_couplings = json.load(file)
                for key, value in tmp_dic_of_couplings.items():
                    tmp_dic_of_couplings[key] = tuple(tmp_dic_of_couplings[key].split(", "))
        except PermissionError:
            self._logger.log_error(f"PermissionError: Unable to read the file '{couplings_path}'.")
            raise PermissionError(f"Unable to read the file '{couplings_path}'.")
        return tmp_dic_of_couplings
