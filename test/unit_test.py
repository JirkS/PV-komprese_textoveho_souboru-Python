import unittest
import configparser
from unittest.mock import MagicMock
from src.compression.Loader import Loader
from src.patterns.Template import Template
from src.security.Logger import Logger
from src.compression.Compressor import Compressor


class TestCompressorMethods(unittest.TestCase):

    def setUp(self):
        self.c_p = configparser.ConfigParser()
        self.c_p.read('../config/config.ini')

        self.path_to_info_log_file = self.c_p.get('STATIC', 'info_log_path')
        self.path_to_error_log_file = self.c_p.get('STATIC', 'error_log_path')
        self.logger = Logger("../" + self.path_to_info_log_file, "../" + self.path_to_error_log_file)
        self.loader = Loader(self.logger)

        self.path_to_text_file = self.c_p.get('USER-STATIC', 'text_file_path')

        self.useless_words_json_file_path = self.c_p.get('STATIC', 'useless_words_json_file_path')
        self.abbreviations_json_file_path = self.c_p.get('STATIC', 'abbreviations_json_file_path')
        self.couplings_json_file_path = self.c_p.get('STATIC', 'couplings_json_file_path')
        self.template = Template("../" + self.useless_words_json_file_path,
                                 "../" + self.abbreviations_json_file_path,
                                 "../" + self.couplings_json_file_path,
                                 self.loader,
                                 self.logger)

    def test_count_num_of_words(self):
        compressor = Compressor('../' + self.path_to_text_file, self.template, self.loader, self.logger)
        compressor._dictionary_of_words = {'word1': 3, 'word2': 5, 'word3': 2}
        compressor.count_num_of_words()
        self.assertEqual(compressor._num_of_words, 10)

    def test_fill_dic_by_the_most_common_words(self):
        loader_mock = MagicMock()
        loader_mock.load_rows_of_text_file.return_value = ['This is a test. This is another test.', 'Yet another test.']
        compressor = Compressor('../' + self.path_to_text_file, self.template, loader_mock, self.logger)
        compressor.fill_dic_by_the_most_common_words()
        expected_dict = {'this': 2, 'is': 2, 'a': 1, 'test': 3, 'another': 2, 'yet': 1}
        self.assertDictEqual(compressor._dictionary_of_words, expected_dict)

    def test_fill_dic_of_two_word_phrases(self):
        loader_mock = MagicMock()
        loader_mock.load_rows_of_text_file.return_value = ['This is a test. This is another test.', 'Yet another test.']
        compressor = Compressor('../' + self.path_to_text_file, self.template, loader_mock, self.logger)
        result = compressor.fill_dic_of_two_word_phrases()
        expected_dict = {'this is': 2, 'is a': 1, 'a test': 1, 'test this': 1, 'is another': 1, 'another test': 2,
                         'yet another': 1}
        self.assertDictEqual(result, expected_dict)

    def test_fill_dic_of_abbreviation(self):
        compressor = Compressor('../' + self.path_to_text_file, self.template, self.loader, self.logger)
        compressor._dictionary_of_two_word_phrases = {'word1 word2': 3, 'word3 word4': 5, 'word5 word6': 2}
        compressor._dictionary_of_words = {'word1': 1, 'word2': 2, 'word3': 3, 'word4': 4, 'word5': 5, 'word6': 6}
        compressor.fill_dic_of_abbreviation()
        expected_dict = {'word1 word2': 'WW', 'word3 word4': 'WOWO'}
        self.assertDictEqual(compressor._dic_of_abbreviation, expected_dict)

    def test_delete_short_sentences(self):
        compressor = Compressor('../' + self.path_to_text_file, self.template, self.loader, self.logger)
        compressor._list_of_rows = ['Tak je to.', 'Ano, přesně.']
        compressor.delete_short_sentences()
        expected_list = ['', '']
        self.assertListEqual(compressor._list_of_rows, expected_list)

    def test_delete_useless_words(self):
        compressor = Compressor('../' + self.path_to_text_file, self.template, self.loader, self.logger)
        compressor._list_of_rows = ['This is a test.', 'jakoby noo']
        compressor.delete_useless_words()
        expected_list = ['This is a test.', ' ']
        self.assertListEqual(compressor._list_of_rows, expected_list)

    def test_replace_words_with_abbreviations(self):
        compressor = Compressor('../' + self.path_to_text_file, self.template, self.loader, self.logger)
        compressor._list_of_rows = ['Informace', 'například']
        compressor.replace_words_with_abbreviations()
        expected_list = ['Info.', 'např.']
        self.assertListEqual(compressor._list_of_rows, expected_list)

    def test_replace_words_of_coupling_synonyms(self):
        compressor = Compressor('../' + self.path_to_text_file, self.template, self.loader, self.logger)
        compressor._list_of_rows = ['This is a test.', 'Another example sentence.']
        compressor.replace_words_of_coupling_synonyms()
        expected_list = ['This is a test.', 'Another example sentence.']
        self.assertListEqual(compressor._list_of_rows, expected_list)

    def test_replace_words_with_abbreviations_from_dictionary(self):
        compressor = Compressor('../' + self.path_to_text_file, self.template, self.loader, self.logger)
        compressor._list_of_rows = ['This is a test.', 'Another example sentence.']
        compressor._dic_of_abbreviation = {'is a': 'IA', 'example sentence': 'ES'}
        compressor.replace_words_with_abbreviations_from_dictionary('../output', 'abbreviations')
        expected_list = ['This IA test.', 'Another ES.']
        self.assertListEqual(compressor._list_of_rows, expected_list)

    def test_fill_best_of_rest_of_the_most_common_words(self):
        compressor = Compressor('../' + self.path_to_text_file, self.template, self.loader, self.logger)
        compressor._dictionary_of_words = {'word1': 5, 'word2': 10, 'word3': 15}
        compressor._num_of_words = 30
        compressor.fill_best_of_rest_of_the_most_common_words()
        self.assertTrue(all(symbol.isascii() for symbol in compressor._best_of_rest_of_the_most_common_words.values()))

    def test_replace_words_for_symbols(self):
        compressor = Compressor('../' + self.path_to_text_file, self.template, self.loader, self.logger)
        compressor._list_of_rows = ['This is a test.', 'Another example sentence.']
        compressor._best_of_rest_of_the_most_common_words = {'test': '?T', 'example': '?E'}
        compressor.replace_words_for_symbols('../output', 'symbols')
        expected_list = ['This is a ?T.', 'Another ?E sentence.']
        self.assertListEqual(compressor._list_of_rows, expected_list)


if __name__ == '__unit_test__':
    unittest.main()
