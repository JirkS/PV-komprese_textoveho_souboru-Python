import configparser
from src.compression.Loader import Loader
from src.patterns.Template import Template
from src.security.Logger import Logger
from src.compression.Compressor import Compressor


def print_hint(hint_list: list):
    """
    prints and explains how to use the program
    :param hint_list: list of lines from text file
    :return: welcome text with hints and explains how to use the program
    """
    tmp_hint = ""
    for line in hint_list:
        tmp_hint += line
    return tmp_hint


def main():
    try:
        c_p = configparser.ConfigParser()
        c_p.read('config/config.ini')

        path_to_info_log_file = c_p.get('STATIC', 'info_log_path')
        path_to_error_log_file = c_p.get('STATIC', 'error_log_path')
        logger = Logger(path_to_info_log_file, path_to_error_log_file)
        logger.log_info("Program started!")

        loader = Loader(logger)

        hint = c_p.get('STATIC', 'hint')
        print(print_hint(loader.load_hint(hint)))

        useless_words_json_file_path = c_p.get('STATIC', 'useless_words_json_file_path')
        abbreviations_json_file_path = c_p.get('STATIC', 'abbreviations_json_file_path')
        couplings_json_file_path = c_p.get('STATIC', 'couplings_json_file_path')
        t = Template(useless_words_json_file_path,
                     abbreviations_json_file_path,
                     couplings_json_file_path,
                     loader,
                     logger)

        path_to_text_file = c_p.get('USER-STATIC', 'text_file_path')
        compressor = Compressor(path_to_text_file, t, loader, logger)

        path_to_save_output_files = c_p.get('USER-STATIC', 'path_to_save_output_files')
        name_of_csv_abbreviations = c_p.get('STATIC', 'name_of_csv_abbreviations')
        name_of_csv_symbols = c_p.get('STATIC', 'name_of_csv_symbols')
        compressor.compress(path_to_save_output_files, name_of_csv_abbreviations, name_of_csv_symbols)

        name_of_compressed_text_file = c_p.get('USER-STATIC', 'name_of_final_text_file')
        print(compressor.write_final_text_file(path_to_save_output_files, name_of_compressed_text_file))

        wants_print_logs = c_p.get('USER-LOG', 'wants_print_logs')
        start_date_time = c_p.get('USER-LOG', 'start_date_time')
        end_date_time = c_p.get('USER-LOG', 'end_date_time')
        min_score = c_p.get('USER-LOG', 'min_score')
        max_score = c_p.get('USER-LOG', 'max_score')
        type_of_change = c_p.get('USER-LOG', 'type_of_change')
        print(logger.get_logs(wants_print_logs, start_date_time, end_date_time, min_score, max_score, type_of_change))

        logger.log_info("Program ended!")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
