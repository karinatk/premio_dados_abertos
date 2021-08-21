import streamlit as st
import pandas as pd

def group_contracts(data):
    agg_dict = {column: ('first' if column != 'valor_contratado' else 'sum') for column in data.columns}
    grouped_contracts_df = data.groupby(['CNPJ', 'Número do contrato'], as_index=False).agg(agg_dict)
    return grouped_contracts_df

def pre_process_continuous(data):
    processed_data = data.copy()
    processed_data['mes_contratado'] = processed_data['Data da contratação'].str.split('/').str[1].astype(int)
    processed_data['ano_contratado'] = processed_data['Data da contratação'].str.split('/').str[2].astype(int)
    processed_data['valor_contratado'] = processed_data['Valor contratado  R$'].str.replace('.', '').astype(float)
    processed_data['prazo_carencia'] = processed_data['Prazo - carência (meses)']
    processed_data['prazo_amortizacao'] = processed_data['Prazo - amortização (meses)']
    processed_data['juros'] = processed_data['Juros'].str.replace(',', '.')
    processed_data['porte_do_cliente'] = processed_data['Porte do cliente'].apply(get_size_of_company_label)
    return processed_data

def get_size_of_company_label(size_of_company):
    if size_of_company == 'MICRO':
        label = 0
    elif size_of_company == 'PEQUENA':
        label = 1
    elif size_of_company == 'MÉDIA':
        label = 2
    elif size_of_company == 'GRANDE':
        label = 3
    else:
        label = 4
    return label

@st.cache(persist=True)
def load_data():
    operacoes = pd.read_csv('csv/Operações contratadas na forma direta e indireta não automática (2002 a 30.06.2021).csv', sep=';', encoding='latin-1')
    processed_data = pre_process_continuous(operacoes)
    grouped_contracts_df = group_contracts(processed_data)
    return grouped_contracts_df

class Faq: 

    def __init__(self) -> None:
        self.pages = []
        self.grouped_contracts_df = load_data()
    
    def add_page(self, title, func) -> None: 
        self.pages.append({
                "title": title, 
                "function": func
            })

    def run(self):
        page = st.sidebar.selectbox(
            "Selecione a página", 
            self.pages, 
            format_func=lambda page: page["title"]
        )
        page["function"](self.grouped_contracts_df)