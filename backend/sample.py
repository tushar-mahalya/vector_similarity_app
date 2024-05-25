from src.chromadb import Database
from src.preprocessing import preprocess_data
import pandas as pd
import ast

def main():
    # For db connectivity
    df = pd.read_csv('files/Data_Vectors.csv')
    prep_df = preprocess_data(df)
    db = Database(prep_df)
    db.fetch_or_create_db()

    # for querying the db
    with open('files/selected_vector.txt', 'r') as f:
        content = f.read().strip()
    selected_vectors = ast.literal_eval(content)

    similar_vectors = db.query_vector(selected_vectors, n_results=20)

    print(similar_vectors)


if __name__ == '__main__':
    main()