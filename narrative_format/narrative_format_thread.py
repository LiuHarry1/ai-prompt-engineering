import threading
import time
import os
from config import *
import util.file_util as file_util
import narrative_format.narrative_format_case as narrative_format_case

narrative_raw_folder = Config.NARRATIVE_RAW
narrative_formatted_folder = Config.NARRATIVE_FORMATTED


def get_new_files():
    new_files = set(os.listdir(narrative_raw_folder)) - set(os.listdir(narrative_formatted_folder))
    return new_files
    # all_new_files = []
    # if new_files:
    #     for file in new_files:
    #         file_a_path = os.path.join(narrative_raw_folder, file)
    #         file_b_path = os.path.join(narrative_formatted_folder, file + ".running")
    #
    #         if os.path.isfile(file_a_path) and not os.path.isfile(file_b_path):
    #             # Do whatever you want here when a new file is found
    #             all_new_files.append(file)
    #             print(f"New file found in folder A: {file}")
    # return all_new_files


def format_narrative(file):
    file_util.write_txt_to_file("", os.path.join(narrative_formatted_folder, file + ".running"))
    print("Starting to format narrative file,", file)
    # time.sleep(10)
    formatted_text = narrative_format_case.format_into_paragraphs(file)
    print(formatted_text)
    print("Finished to format narrative file,", file)
    file_util.remove_file(os.path.join(narrative_formatted_folder, file + ".running"))


def narrative_format_task():
    while True:
        all_new_files = get_new_files()
        if all_new_files:
            for new_file in all_new_files:
                format_narrative(new_file)

        time.sleep(10)  # Check every 1 minute


# Start the thread to continuously check for new files
narrative_format_thread = threading.Thread(target=narrative_format_task)
narrative_format_thread.daemon = True
# narrative_format_task.start()
