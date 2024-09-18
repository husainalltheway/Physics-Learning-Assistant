import os

current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
common_path = os.path.join(parent_dir,'Neet_GPT')

BOOK_PATH = os.path.join(parent_dir,'books')
JSON_FOLDER_PATH = os.path.join(parent_dir,'json_output')