import pandas as pd
import os

def load_products():
    df = pd.read_excel(os.path.join('dataset', 'Updated_PRODUCTS.xlsx'))

    # Handle missing values
    df['Image URL'] = df['Image URL'].fillna('https://via.placeholder.com/150')

    # Create a new column 'ImageURL' for the cart.html
    df['ImageURL'] = df['Image URL']

    return df
