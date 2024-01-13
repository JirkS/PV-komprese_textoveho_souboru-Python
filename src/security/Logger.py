import logging
import os
from datetime import datetime


class Logger:
    def __init__(self, info_log_file_path: str, error_log_file_path: str):
        self._info_log_file_path = info_log_file_path
        self.check_path(info_log_file_path)

        self._error_log_file_path = error_log_file_path
        self.check_path(error_log_file_path)

        self._info_logger = logging.getLogger('info_logger')
        self._info_logger.setLevel(logging.INFO)
        info_handler = logging.FileHandler(self._info_log_file_path, encoding='utf-8')
        self._info_logger.addHandler(info_handler)

        self._error_logger = logging.getLogger('error_logger')
        self._error_logger.setLevel(logging.ERROR)
        error_handler = logging.FileHandler(self._error_log_file_path, encoding='utf-8')
        self._error_logger.addHandler(error_handler)

    def log_info(self, message: str):
        """
        write log message into info file log
        :param message: message to write
        :return:
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._info_logger.info(f'INFO:root:{timestamp}: {message}')

    def log_error(self, message: str):
        """
        write log message into error file log
        :param message: message to write
        :return:
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._error_logger.error(f'ERROR:root:{timestamp}: {message}')

    def check_path(self, path: str):
        """
        checking if path of log file is correct
        :param path: path to the lig file
        :return:
        """
        if not os.path.exists(path):
            self.log_error(f"FileNotFoundError: File not found: {path}")
            raise FileNotFoundError(f"File not found: {path}")
        if not self._info_log_file_path.lower().endswith('.log'):
            self.log_error(f"ValueError: Invalid file type. Expected a .log file, but got: {path}")
            raise ValueError(f"Invalid file type. Expected a .log file, but got: {path}")

    def get_logs(self, wants_logs: str, start_time, end_time, min_score, max_score, change_type: str) -> str:
        """
        filters informations contained in info log file
        :param wants_logs: yes or no if user actually wants to print some informations from info log file
        :param start_time: starting date time of range, in which informations should be filtered
        :param end_time: ending date time of range, in which informations should be filtered
        :param min_score: minimum of range, in which informations should be filtered
        :param max_score: maximum of range, in which informations should be filtered
        :param change_type: fiter by type of change compression
        :return: filtered information logs
        """
        if wants_logs == "Y":
            try:
                if start_time == "None":
                    start_time = None
                else:
                    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                if end_time == "None":
                    end_time = None
                else:
                    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass
            try:
                if min_score == "None":
                    min_score = None
                else:
                    min_score = int(min_score)
                if max_score == "None":
                    max_score = None
                else:
                    max_score = int(max_score)
            except ValueError:
                pass
            if change_type == "None":
                change_type = None
            if isinstance(min_score, int) and isinstance(max_score, int) and min_score > max_score:
                self.log_error(f"Error: \"min_score\" is bigger than \"max_score\" loaded from config/config.ini")
                raise Exception(f"Error: \"min_score\" is bigger than \"max_score\" loaded from config/config.ini")
            list_of_filtered_line_logs = []
            with open(self._info_log_file_path, 'r', encoding='utf-8') as file:
                list_of_line_logs = list(file)
                for line in reversed(list_of_line_logs):
                    if start_time == "last_run" and end_time == "last_run" and "Program started!" in line:
                        break
                    date_time = False
                    score = False
                    ch_type = False
                    clean_line = line.strip()
                    if start_time is not None and end_time is not None:
                        if start_time == "last_run" and end_time == "last_run":
                            date_time = True
                        else:
                            try:
                                date_time_of_line = datetime.strptime(clean_line[10: 29], "%Y-%m-%d %H:%M:%S")
                                if start_time <= date_time_of_line <= end_time:
                                    date_time = True
                            except Exception:
                                pass
                    if isinstance(min_score, int) and isinstance(max_score, int) and \
                            min_score >= 0 and max_score >= 0 and min_score < max_score:
                        try:
                            index = 13
                            char = clean_line[len(clean_line) - index]
                            while char.isdigit():
                                index += 1
                                char = clean_line[len(clean_line) - index]
                            score_line = clean_line[len(clean_line) - index+1: len(clean_line) - 12]
                            if min_score <= int(score_line) <= max_score:
                                score = True
                        except Exception:
                            pass
                    if change_type is not None:
                        type_line = clean_line[37: 55]
                        if change_type in type_line:
                            ch_type = True

                    if (date_time or (start_time is None and end_time is None)) and \
                            (score or (min_score is None and max_score is None)) and \
                            (ch_type or (change_type is None)):
                        list_of_filtered_line_logs.append(clean_line)
            tmp_str = "Filtred logs:\n"
            for line in reversed(list_of_filtered_line_logs):
                tmp_str += line + "\n"
            return tmp_str
        return ""
