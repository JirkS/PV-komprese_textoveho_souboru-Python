from src.compression import Loader
from src.security import Logger


class Template:
    def __init__(self, useless_words_path: str, abbreviations_path: str, couplings_path: str, loader: Loader, logger: Logger):
        self._logger = logger
        self._list_of_useless_words = loader.load_useless_words(useless_words_path)
        self._dic_of_abbreviations = loader.load_abbreviations(abbreviations_path)
        self._dic_of_couplings = loader.load_couplings(couplings_path)

    @property
    def list_of_useless_words(self) -> list:
        """
        getter for list of useless words
        :return: list of useless words
        """
        return self._list_of_useless_words

    @property
    def dic_of_abbreviations(self) -> dict:
        """
        getter for dictionary of abbreviations
        :return: dictionary of abbreviations
        """
        return self._dic_of_abbreviations

    @property
    def dic_of_couplings(self) -> dict:
        """
        getter for dictionary of couplings
        :return: dictionary of couplings
        """
        return self._dic_of_couplings
