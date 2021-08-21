import streamlit as st

def get_page_information():
    st.title("O que pode ser financiado?")

    st.write(
    """
        ##
        O cliente pode solicitar o financiamento diretamente ao BNDES (apoio direto) ou por meio de instituições financeiras credenciadas (apoio indireto).
        A forma de apoio depende da finalidade e do valor do financiamento.
        No apoio indireto, as instituições financeiras parceiras do BNDES atuam como intermediárias na concessão do financiamento, assumindo o risco de crédito
        (risco de não pagamento pelo cliente) total ou parcialmente. Como o BNDES não possui agências, o apoio indireto permite que seus recursos cheguem a clientes em todos os municípios do Brasil através das instituições financeiras.
        Em geral, são realizadas na forma de apoio indireto todas as operações de financiamento à compra isolada de máquinas e equipamentos, bem como financiamentos inferiores a R$ 10 milhões destinados a projetos de implantação, modernização e expansão de empreendimentos.
        Para solicitar apoio direto ao BNDES, é necessário, em geral, que o financiamento tenha valor superior a R$ 40 milhões - R$ 20 milhões a depender da sistemática. Em alguns casos específicos, o BNDES permite o apoio direto a financiamentos de valor inferior a esse limite.
    """)