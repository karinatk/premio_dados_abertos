import json
import pickle

import pandas as pd
import streamlit as st
from PIL import Image

@st.cache(persist=True)
def read_image(path):
    image = Image.open(path)
    return image

@st.cache(persist=True)
def read_df(path):
    bndes_df = pd.read_csv(path, sep=";", encoding="utf-8", dtype={"cnpj": object})
    return bndes_df

@st.cache(persist=True)
def read_json(path):
    with open(path, encoding="utf-8") as f:
        file_dict = json.loads(f.read())
    return file_dict

#@st.cache(persist=True)
def read_model(file_path):
    with open(file_path, "rb") as f:
        loaded_model = pickle.load(f)
    return loaded_model
