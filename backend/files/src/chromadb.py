import os
import chromadb
from chromadb.config import Settings

class Database:
    def __init__(self, df):
        self.database = df
        self.collection_name = 'user_vectors_collection'
        self.storage_path = 'backend/files/database/'

        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

        self.chroma_client = chromadb.Client(Settings(persist_directory=self.storage_path))
        self.collection = None

    def generate_ids(self):
        rows = self.database.shape[0]
        ids = [str(i) for i in range(1, rows + 1)]
        return ids

    def convert_to_list(self):
        data_arr = self.database.values.tolist()
        return data_arr

    def fetch_or_create_db(self):
        self.collection = self.chroma_client.get_or_create_collection(self.collection_name)
        self.collection.add(embeddings=self.convert_to_list(), ids=self.generate_ids())
