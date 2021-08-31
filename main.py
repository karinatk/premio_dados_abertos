import os

import streamlit as st

import file_utils
from pages import home

st.set_page_config(layout="wide")

def main():

    current_dir = os.getcwd()
    files_dir = os.path.join(current_dir, "files")
    image_path = os.path.join(files_dir, "images", "bndes.png")
    csv_path = os.path.join(files_dir, "csv", "output_csv", "bndes_financiamentos.csv")
    product_model_path = os.path.join(files_dir, "models", "modelo_produto.pkl")
    encoder_file_path = os.path.join(files_dir, "models", "encoder.json")

    image = file_utils.read_image(image_path)
    st.image(image, width=200)

    cached_df = file_utils.read_df(csv_path)
    cached_model = file_utils.read_model(product_model_path)
    cached_encoder_dict = file_utils.read_json(encoder_file_path)

    home.get_page_information(
        cached_df,
        cached_model,
        cached_encoder_dict
    )

if __name__ == '__main__':
    main()
