from PIL import Image
import streamlit as st

from faq import Faq 
from paginas_faq import tipo_financiamento, como_funciona, garantia, juros, participacao, prazos, usuario_financiamento

image = Image.open("imagens/bndes.png")
st.image(image, width=200)

bndes_faq = Faq()
bndes_faq.add_page("O que pode ser financiado", tipo_financiamento.get_page_information)
bndes_faq.add_page("Quem pode obter", usuario_financiamento.get_page_information)
bndes_faq.add_page("Como funciona", como_funciona.get_page_information)
bndes_faq.add_page("Participação, limites e gastos realizados", participacao.get_page_information)
bndes_faq.add_page("Prazos", prazos.get_page_information)
bndes_faq.add_page("Garantias", garantia.get_page_information)
bndes_faq.add_page("Taxa de juros", juros.get_page_information)

bndes_faq.run()