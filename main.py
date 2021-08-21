from PIL import Image
import streamlit as st

from faq import Faq 
from paginas_faq import tipo_financiamento, como_funciona, usuario_financiamento

def main():
    image = Image.open("imagens/bndes.png")
    st.image(image, width=200)
    bndes_faq = Faq()
    bndes_faq.add_page("O que pode ser financiado", tipo_financiamento.get_page_information)
    bndes_faq.add_page("Quem pode obter", usuario_financiamento.get_page_information)
    bndes_faq.add_page("Como funciona", como_funciona.get_page_information)
    bndes_faq.run()

if __name__ == '__main__':
    main()