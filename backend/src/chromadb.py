import pandas as pd
import chromadb
from typing import List, Tuple


class Database:
    """
    A class to manage the database of user vectors using ChromaDB.

    Attributes:
    ----------
    database : pandas.DataFrame
        A dataframe containing user vectors.
    collection_name : str
        The name of the collection to store user vectors.
    storage_path : str
        The path to store the ChromaDB files.
    chroma_client : chromadb.Client
        The client instance for interacting with ChromaDB.
    collection : chromadb.Collection or None
        The collection instance for storing user vectors.

    Methods:
    -------
    generate_ids() -> List[str]:
        Generate unique IDs for each row in the dataframe.
    convert_to_list() -> List[List[float]]:
        Convert the dataframe to a list of lists.
    fetch_or_create_db() -> None:
        Fetch the existing collection or create a new one and add data to it.
    query_vector(vector: List[float], n_results: int = 10) -> Tuple[List[str], List[float]]:
        Query the collection to find vectors similar to the given vector.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the Database class.

        Parameters:
        ----------
        df : pandas.DataFrame
            A dataframe containing user vectors.
        """
        self.database = df
        self.collection_name = 'user_vectors_collection'
        self.chroma_client = chromadb.Client()
        self.collection = None

    def generate_ids(self) -> List[str]:
        """
        Generate unique IDs for each row in the dataframe.

        Returns:
        -------
        List[str]
            A list of unique string IDs.
        """
        rows = self.database.shape[0]
        ids = [str(i) for i in range(1, rows + 1)]
        return ids

    def convert_to_list(self) -> List[List[float]]:
        """
        Convert the dataframe to a list of lists.

        Returns:
        -------
        List[List[float]]
            A list of lists where each sublist represents a row in the dataframe.
        """
        data_arr = self.database.values.tolist()
        return data_arr

    def fetch_or_create_db(self) -> None:
        """
        Fetch the existing vector database if it exists, else save the collection of the new database.
        """
        collections = self.chroma_client.list_collections()
        collection_names = [collection.name for collection in collections]

        if self.collection_name in collection_names:
            self.collection = self.chroma_client.get_collection(self.collection_name)
        else:
            self.collection = self.chroma_client.create_collection(self.collection_name)
            self.collection.add(embeddings=self.convert_to_list(), ids=self.generate_ids())

    def query_vector(self, vector: List[float], n_results: int = 10) -> Tuple[List[str], List[float]]:
        """
        Query the collection to find vectors similar to the given vector.

        Parameters:
        ----------
        vector : List[float]
            A vector to query for similar vectors in the collection.
        n_results : int, optional
            The number of similar vectors to retrieve (default is 10).

        Returns:
        -------
        Tuple[List[str], List[float]]
            A tuple containing a list of IDs of similar vectors and a list of distances to these vectors.
        """
        similarity_dict = self.collection.query(query_embeddings=vector, n_results=n_results)
        similar_vector_indexes, distances = similarity_dict['ids'][0], similarity_dict['distances'][0]
        return similar_vector_indexes, distances
