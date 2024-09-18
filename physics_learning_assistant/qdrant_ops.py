import os
import json
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.models import VectorParams, Distance, PointStruct

current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
JSON_OUTPUT_PATH = os.path.join(parent_dir,'json_output')

QDRANT_URL = "------------->> provide your url <<-------------"
QDRANT_TOKEN = "------------->> provide your token <<-------------"

def qdrant_connection():
    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_TOKEN
    )
    return qdrant_client

import uuid

def insert_data_in_qd(data):
    counter = 0
    qd = qdrant_connection()
    collection_name = "physics_data"
    all_insertions_successful = True

    for each_obj in data:
        counter += 1
        point_id = str(uuid.uuid4())
        point = models.PointStruct(
            id=point_id,
            vector=each_obj['vectors'],
            payload={
                'metadata': each_obj['metadata']
            }
        )
        try:
            print(f"INSERTING {counter} OBJ with ID {point_id}")
            operation_result = qd.upsert(
                collection_name=collection_name,
                points=[point],
                wait=True
            )
            
            if operation_result.status != models.UpdateStatus.COMPLETED:
                print(f"Insertion failed for object: {each_obj.get('id', 'unknown')}. Status: {operation_result.status}")
                all_insertions_successful = False
        except Exception as e:
            print(f"An error occurred during insertion of object {each_obj.get('id', 'unknown')}: {str(e)}")
            all_insertions_successful = False

    if all_insertions_successful:
        print(f"Successfully inserted all {len(data)} objects.")
        return all_insertions_successful
    else:
        print("Some insertions failed. Check the logs for details.")


def create_collection():
    qd = qdrant_connection()
    collection_name = "physics_data"
    
    if qd.collection_exists(collection_name=collection_name):
        return True
    
    try:
        qd.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )
        return True
    except Exception as e:
        print(f"Error creating collection: {e}")
        return False


def read_each_file(file_array):
    if isinstance(file_array, list) and len(file_array) > 0:
        for each_file in file_array:
            print(f"OPERATIONS STARTED FOR FILE {each_file['name']}")
            with open(each_file['path']) as file:
                data = json.load(file)
                
                print("CREATING COLLECTION")
                collection_boolean = create_collection()
                if collection_boolean:
                    print("DATA INSERTION STARTED")
                    data_insert = insert_data_in_qd(data)
                    if data_insert:
                        print("DATA INSERTION COMPLETED")
                    else:
                        print("ERROR WHILE INSERTING DATA")
        return True

    
def check_file_exists():
    print("CHECKING IF FILES EXIST")
    each_file_path_array = []
    listdir = os.listdir(JSON_OUTPUT_PATH)
    if isinstance(listdir, list) and len(listdir) > 0:
        for each_book in listdir:
            each_book_path = os.path.join(JSON_OUTPUT_PATH, each_book)
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
    read_each_file(files_list)