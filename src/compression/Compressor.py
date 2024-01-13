import re
import csv
import os
import random
import string
from src.compression import Loader
from src.patterns import Template
from src.security import Logger


class Compressor:
    def __init__(self, path: str, template: Template, loader: Loader, logger: Logger):
        self._template = template
        self._logger = logger
        self._list_of_rows = loader.load_rows_of_text_file(path)
        self._dictionary_of_words = dict()
        self.fill_dic_by_the_most_common_words()
        self._num_of_words = 0
        self.count_num_of_words()
        self._dictionary_of_two_word_phrases = self.fill_dic_of_two_word_phrases()
        self._dic_of_abbreviation = dict()
        self.fill_dic_of_abbreviation()
        self._best_of_rest_of_the_most_common_words = dict()

    def compress(self, path_to_save_output_files: str, name_of_csv_abbreviations: str, name_of_csv_symbols: str):
        """
        calls every method to compress
        :param path_to_save_output_files: path/directory, where output files will be saved
        :param name_of_csv_abbreviations: name of csv abbreviations file
        :param name_of_csv_symbols: name of csv symbols file
        :return:
        """
        self.delete_short_sentences()
        self.delete_useless_words()
        self.replace_words_with_abbreviations()
        self.replace_words_of_coupling_synonyms()
        self.replace_words_with_abbreviations_from_dictionary(path_to_save_output_files, name_of_csv_abbreviations)
        self.fill_best_of_rest_of_the_most_common_words()
        self.replace_words_for_symbols(path_to_save_output_files, name_of_csv_symbols)

    def count_num_of_words(self):
        """
        counts number of all words in text file
        :return:
        """
        self._num_of_words = 0
        for key, value in self._dictionary_of_words.items():
            self._num_of_words += value

    def fill_dic_by_the_most_common_words(self):
        """
        fills dictionary by the most common words with their frequency
        :return:
        """
        self._dictionary_of_words = dict()
        for row in self._list_of_rows:
            tmp_words = row.split()
            for word in tmp_words:
                while word[len(word)-1] == "." or word[len(word)-1] == "," or word[len(word)-1] == '"':
                    word = word[0:len(word)-1]
                while word[0] == "." or word[0] == "," or word[0] == '"':
                    word = word[1:len(word)]
                word = word.lower()
                if word in self._dictionary_of_words:
                    self._dictionary_of_words[word] += 1
                else:
                    self._dictionary_of_words[word] = 1
        self._dictionary_of_words = dict(sorted(self._dictionary_of_words.items(),
                                                key=lambda item: item[1], reverse=True))

    def fill_dic_of_two_word_phrases(self) -> dict:
        """
        fills dictionary by two word phrases
        :return:
        """
        tmp_dic = dict()
        for row in self._list_of_rows:
            tmp_words = row.split()
            word_before = None
            for word in tmp_words:
                while word[len(word)-1] == "." or word[len(word)-1] == "," or word[len(word)-1] == '"':
                    word = word[0:len(word)-1]
                while word[0] == "." or word[0] == "," or word[0] == '"':
                    word = word[1:len(word)]
                word = word.lower()
                if word_before is None:
                    word_before = word
                else:
                    phrase = word_before + " " + word
                    word_before = word
                    if phrase in tmp_dic:
                        tmp_dic[phrase] += 1
                    else:
                        tmp_dic[phrase] = 1
        tmp_dic = dict(sorted(tmp_dic.items(), key=lambda item: item[1], reverse=True))
        return tmp_dic

    def fill_dic_of_abbreviation(self):
        """
        fills dictionary by words and abbreviations using the most effectively way based on frequency analysis of words
        :return:
        """
        self._dic_of_abbreviation = dict()
        set_of_words_to_delete = set()
        for key, value in self._dictionary_of_two_word_phrases.items():
            count_points = 0
            if value > 2:
                tmp_words = key.split()
                for word in tmp_words:
                    if len(word) < 3:
                        count_points = -1
                        break
                    count_points += self._dictionary_of_words[word]
                if count_points != -1 and count_points <= value * len(tmp_words) + len(tmp_words):
                    tmp_abbreviation = ""
                    index = 0
                    for word in tmp_words:
                        tmp_abbreviation += word[index].upper()
                    index += 1
                    while tmp_abbreviation in self._dic_of_abbreviation.values():
                        middle_index = len(tmp_abbreviation) // 2
                        part1 = tmp_abbreviation[:middle_index]
                        part2 = tmp_abbreviation[middle_index:]
                        part1 += tmp_words[0][index].upper()
                        part2 += tmp_words[1][index].upper()
                        tmp_abbreviation = part1 + part2
                        index += 1
                    self._dic_of_abbreviation[key] = tmp_abbreviation
                    for word in tmp_words:
                        set_of_words_to_delete.add(word)
            else:
                break
        for word in set_of_words_to_delete:
            del self._dictionary_of_words[word]

    def delete_short_sentences(self):
        """
        deletes short useless sentences
        :return:
        """
        for i in range(len(self._list_of_rows)):
            sentences = re.split(r'[.?!]', self._list_of_rows[i])
            sentences = list(sentences)
            for s in range(len(sentences)):
                words = sentences[s].split()
                if len(words) < 4 and len(sentences[s]) < 16:
                    self._list_of_rows[i] = self._list_of_rows[i].replace(sentences[s] + ".", "")
                    self._list_of_rows[i] = self._list_of_rows[i].replace(sentences[s] + "!", "")
                    self._list_of_rows[i] = self._list_of_rows[i].replace(sentences[s] + "?", "")

    def delete_useless_words(self):
        """
        deletes useless words
        :return:
        """
        for i in range(len(self._list_of_rows)):
            tmp_words = self._list_of_rows[i].split()
            for j in range(len(tmp_words)):
                tmp_word = tmp_words[j]
                tmp_word = tmp_word.lower()
                last_char = tmp_word[len(tmp_word) - 1]
                if not last_char.isalpha():
                    tmp_word = tmp_word[0:len(tmp_word)-1]
                for del_word in self._template.list_of_useless_words:
                    if del_word == tmp_word:
                        self._logger.log_info(f"Change: deleted \"{tmp_words[j]}\", "
                                              f"Score: deleted {len(tmp_words[j])} characters!")
                        tmp_words[j] = ""
                        break
            tmp_row = " ".join(tmp_words)
            self._list_of_rows[i] = tmp_row

    def replace_words_with_abbreviations(self):
        """
        replaces words with abbreviations
        :return:
        """
        for i in range(len(self._list_of_rows)):
            tmp_words = self._list_of_rows[i].split()
            for j in range(len(tmp_words)):
                tmp_word = tmp_words[j]
                is_upper = tmp_word[0].isupper()
                if is_upper:
                    tmp_word = tmp_word.lower()
                last_char = tmp_word[len(tmp_word)-1]
                if not last_char.isalpha():
                    tmp_word = tmp_word[0:len(tmp_word)-1]
                for key, value in self._template.dic_of_abbreviations.items():
                    if key == tmp_word or key == tmp_word[0:len(tmp_word)-1]:
                        tmp_word = value
                        if is_upper:
                            tmp_word = tmp_word.capitalize()
                        if not last_char.isalpha():
                            tmp_word = tmp_word + last_char
                        if len(tmp_words[j]) - len(tmp_word) > 0:
                            self._logger.log_info(f"Change: shorted \"{tmp_words[j]}\" to \"{tmp_word}\", "
                                                  f"Score: deleted {len(tmp_words[j]) - len(tmp_word)} characters!")
                            tmp_words[j] = tmp_word
                        break
            tmp_row = " ".join(tmp_words)
            self._list_of_rows[i] = tmp_row

    def replace_words_of_coupling_synonyms(self):
        """
        replaces words with couplings synonyms
        :return:
        """
        for i in range(len(self._list_of_rows)):
            tmp_words = self._list_of_rows[i].split()
            for j in range(len(tmp_words)):
                tmp_word = tmp_words[j]
                is_upper = tmp_word[0].isupper()
                if is_upper:
                    tmp_word = tmp_word.lower()
                last_char = tmp_word[len(tmp_word)-1]
                if not last_char.isalpha():
                    tmp_word = tmp_word[0:len(tmp_word)-1]
                for key, value in self._template.dic_of_couplings.items():
                    for word in value:
                        if word == tmp_word:
                            tmp_word = key
                            if is_upper:
                                tmp_word = tmp_word.capitalize()
                            if not last_char.isalpha():
                                tmp_word = tmp_word + last_char
                            if len(tmp_words[j]) - len(tmp_word) > 0:
                                self._logger.log_info(f"Change: shorted \"{tmp_words[j]}\" to \"{tmp_word}\", "
                                                      f"Score: deleted {len(tmp_words[j]) - len(tmp_word)} characters!")
                                tmp_words[j] = tmp_word
                            break
            tmp_row = " ".join(tmp_words)
            self._list_of_rows[i] = tmp_row

    def replace_words_with_abbreviations_from_dictionary(self, file_path: str, file_name: str):
        """
        replaces words with abbreviations from abbreviations words and dictionary
        :param file_path: path/directory, where csv file of words and abbreviations will be saved
        :param file_name: name of csv file
        :return:
        """
        for i in range(len(self._list_of_rows)):
            for key, value in self._dic_of_abbreviation.items():
                tmp_row = self._list_of_rows[i]
                self._list_of_rows[i] = self._list_of_rows[i].replace(key, value)
                self._list_of_rows[i] = self._list_of_rows[i].replace(key.capitalize(), value)
                if tmp_row != self._list_of_rows[i]:
                    self._logger.log_info(f"Change: replaced \"{key}\" to \"{value}\" "
                                          f"{tmp_row.count(key) + tmp_row.count(key.capitalize())} "
                                          f"times in {i + 1}. row, Score: deleted "
                                          f"{len(tmp_row) - len(self._list_of_rows[i])} characters!")
        self.write_csv_file(file_path, file_name, self._dic_of_abbreviation)

    def fill_best_of_rest_of_the_most_common_words(self):
        """
        fills list by the best of rest of the most common words in the text file
        :return:
        """
        for key, value in self._dictionary_of_words.items():
            if self._num_of_words / value < 150 and len(key) > 3:
                symbol = random.choice(string.ascii_letters + string.digits + string.punctuation)
                while symbol in self._best_of_rest_of_the_most_common_words.values():
                    if len(self._best_of_rest_of_the_most_common_words) % 90 == 0:
                        symbol += random.choice(string.ascii_letters + string.digits + string.punctuation)
                    symbol = random.choice(string.ascii_letters + string.digits + string.punctuation)
                self._best_of_rest_of_the_most_common_words[key] = "?" + symbol

    def replace_words_for_symbols(self, file_path: str, file_name: str):
        """
        replaces specific words for symbols
        :param file_path: path/directory, where csv file of words and symbols will be saved
        :param file_name: name of csv file
        :return:
        """
        for i in range(len(self._list_of_rows)):
            for key, value in self._best_of_rest_of_the_most_common_words.items():
                tmp_row = self._list_of_rows[i]
                self._list_of_rows[i] = self._list_of_rows[i].replace(key, value)
                self._list_of_rows[i] = self._list_of_rows[i].replace(key.capitalize(), value)
                if tmp_row != self._list_of_rows[i]:
                    self._logger.log_info(
                        f"Change: symbolized \"{key}\" to \"{value}\" "
                        f"{tmp_row.count(key) + tmp_row.count(key.capitalize())} times in {i + 1}. row, "
                        f"Score: deleted {len(tmp_row) - len(self._list_of_rows[i])} characters!")
        self.write_csv_file(file_path, file_name, self._best_of_rest_of_the_most_common_words)

    @classmethod
    def write_csv_file(cls, file_path: str, file_name: str, dictionary: dict):
        """
        writes csv file from dictionary
        :param file_path: path/directory, where csv file will be saved
        :param file_name: name of csv file
        :param dictionary: dictionary of abbreviations/symbols
        :return:
        """
        full_path = f"{file_path}/{file_name}.csv"
        with open(full_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            for key, value in dictionary.items():
                csv_writer.writerow([key, value])

    def check_directory_path(self, path: str):
        """
        checking if path of directory is correct
        :param path: path of dictionary
        :return:
        """
        if not os.path.isdir(path) or "." in path:
            self._logger.log_error(f"Error: The path '{path}' is not a directory or does not exist.")
            raise NotADirectoryError(f"Error: The path '{path}' is not a directory or does not exist.")
        if not os.path.exists(path):
            self._logger.log_error(f"Error: FileNotFoundError: File not found: {path}")
            raise FileNotFoundError(f"Error: File not found: {path}")

    def write_final_text_file(self, file_path: str, file_name: str):
        """
        write rows from list into final compressed text file
        :param file_path: path/dictionary, where final compressed text file will be saved
        :param file_name: name of final compressed text file
        :return:
        """
        self.check_directory_path(file_path)
        full_path = f"{file_path}{file_name}.txt"
        with open(full_path, 'w', encoding='utf-8') as file:
            for row in self._list_of_rows:
                file.write(row + '\n')
        size_of_file = os.path.getsize(full_path)
        self._logger.log_info(f"Compressed file successfully written to {full_path} "
                              f"with size of file: {size_of_file} bytes!")
        return f"Compressed text file was successfully written to {full_path} with size {size_of_file} bytes!"
