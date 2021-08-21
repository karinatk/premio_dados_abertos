import streamlit as st

from faq import Faq
from PIL import Image
from paginas_faq import tipo_financiamento


bndes_faq = Faq()

image = Image.open('imagens/bndes.png')
st.image(image, width=200)

bndes_faq.add_page('O que pode ser financiado', tipo_financiamento.get_page_information)

bndes_faq.run()