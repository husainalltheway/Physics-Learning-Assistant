import os
import re
import unicodedata
import json
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import (SemanticSplitterNodeParser)

load_dotenv()

current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)

BOOK_PATH = os.path.join(parent_dir,'books')
JSON_OUTPUT_PATH = os.path.join(parent_dir,'json_output')

def create_json_file(data_array, file_name):
    file_name = file_name.replace(".pdf", ".json")
    file_path = os.path.join(JSON_OUTPUT_PATH, file_name)
    with open(file_path, 'w') as json_file:
        json.dump(data_array, json_file, indent=4)
        return True
     

def get_embeddings_of_data(text):
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-mpnet-base-v2")
    embeddings = embed_model.get_text_embedding(text)
    return embeddings
    
def clean_text(text):
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    replacements = {
        '\u2212': '-',
        '\u00b7': '*',
        '\u03b8': 'theta',
        '\u03c0': 'pi',
    }
    for unicode_char, ascii_char in replacements.items():
        text = text.replace(unicode_char, ascii_char)
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    text = '\n'.join(line.strip() for line in text.split('\n'))
    
    return text.strip()


def semantic_chunking_of_data(data):
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-mpnet-base-v2")
    splitter = SemanticSplitterNodeParser(
        buffer_size=1,
        breakpoint_percentile_threshold=95,
        embed_model=embed_model
    )
    nodes = splitter.get_nodes_from_documents(data)
    return nodes

def parse_file(path):
    documents = LlamaParse(result_type="markdown").load_data(path)
    return documents

def parse_each_file(file_array):
    if isinstance(file_array, list) and len(file_array) > 0:
        for each_file in file_array:
            file_data_array = []
            print(f"PARSING OF FILE {each_file['name']} STARTED")
            parsed_file = parse_file(each_file['path'])
            print(f"PARSING OF FILE {each_file['name']} ENDED")
            print(f"SEMANTIC CHUNKING OF FILE {each_file['name']} STARTED")
            chunks = semantic_chunking_of_data(parsed_file)
            print(f"SEMANTIC CHUNKING OF FILE {each_file['name']} ENDED")
            if isinstance(chunks, list) and len(chunks) > 0:
                chunk_counter = 0
                for chunk in chunks:
                    chunk_counter += 1
                    chunk_text = chunk.get_content()
                    print(f"CLEANING CHUNK NUMBER {chunk_counter}")
                    clean_chunk_text = clean_text(chunk_text)
                    print(f"EMBEDDING STARTED FOR CHUNK NUMBER {chunk_counter}")
                    embedded_chunk_text = get_embeddings_of_data(clean_chunk_text)
                    chunk_obj = {
                        "vectors": embedded_chunk_text,
                        "metadata": clean_chunk_text
                    }
                    file_data_array.append(chunk_obj)
                    print(f"OBJ OF CHUNK NUMBER {chunk_counter} ADDED")
        
            if isinstance(file_data_array, list) and len(file_data_array) > 0:
                create_file = create_json_file(file_data_array, each_file['name'])
                if create_file:
                    print(f"FILE CHREATED FOR {each_file['name']}")

def check_file_exists():
    print("CHECKING IF FILES EXIST")
    each_file_path_array = []
    listdir = os.listdir(BOOK_PATH)
    if isinstance(listdir, list) and len(listdir) > 0:
        for each_book in listdir:
            each_book_path = os.path.join(BOOK_PATH, each_book)
            obj = {
                "name": each_book,
                "path": each_book_path 
            }
            each_file_path_array.append(obj)
        print(f"{len(each_file_path_array)} FILES EXIST")
        return each_file_path_array
    else:
        print("FILES DO NOT EXIST")


# Example usage
if __name__ == "__main__":
    files_list = check_file_exists()
    parse_each_file(files_list)