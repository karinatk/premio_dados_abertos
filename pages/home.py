import datetime

import pandas as pd
import streamlit as st

import loan_calculator as lc

def get_page_information(cached_df, cached_model, cached_encoder_dict):
    st.title("Simulação de financiamento BNDES")

    st.write(
    """
        ##
        Para obter apoio financeiro do BNDES, os seguintes requisitos mínimos são necessários:

        - estar em dia com obrigações fiscais, tributárias e sociais;
        - apresentar cadastro satisfatório;
        - ter capacidade de pagamento;
        - dispor de garantias suficientes para cobertura do risco da operação;
        - não estar em regime de recuperação de crédito;
        - atender a legislação relativa à importação, no caso de financiamento para a importação de bens e serviços; e
        - cumprir a legislação ambiental
        ##

        **Preencha os dados a seguir e tentaremos fazer uma simulação do seu financiamento.**
    """)

    row2_1, row2_2, row2_3 = st.columns((1, 1, 1))

    with row2_1:
        company_nature = st.radio(
            "Tipo da empresa",
            cached_df["natureza_do_cliente"].unique()
        )

    with row2_2:
        size_of_company = st.radio(
            "Porte da empresa",
            cached_df["porte_do_cliente"].unique()
        )

        innovation = st.radio(
            "É inovação?",
            ("Sim", "Não")
        )

    with row2_3:
        company_sector = st.radio(
            "Setor CNAE",
            cached_df["setor_cnae"].unique()
        )

        company_subsector_values = cached_df[cached_df["setor_cnae"] == company_sector]["subsetor_cnae"].unique()
        company_subsector_values.sort()
        company_subsector = st.selectbox(
            "Subsetor CNAE",
            company_subsector_values
        )

    amount_of_money = st.slider(
        label="Valor a ser financiado",
        min_value=10000,
        max_value=100000000,
        step=100
    )

    today_year = int(datetime.datetime.now().year)

    feature_data = [
        company_nature,
        size_of_company,
        amount_of_money,
        company_sector,
        company_subsector,
        innovation.upper(),
        today_year
    ]
    training_columns = [
        "natureza_do_cliente",
        "porte_do_cliente",
        "valor_contratado_reais",
        "setor_cnae",
        "subsetor_cnae",
        "inovacao",
        "ano_contratado"
    ]

    st.write("**Dados selecionados:**")
    features_df = pd.DataFrame({column_name: feature for feature, column_name in zip(feature_data, training_columns)}, index=[0])
    st.table(features_df)

    st.write("**Resultado da simulação de financiamento:**")

    product_prediction, product_prediction_prob = lc.get_prediction(
        cached_model,
        feature_data,
        cached_encoder_dict,
        training_columns,
        "produto"
    )

    similar_product_df = lc.get_similar_financing(
        cached_df,
        "produto",
        product_prediction,
        company_nature,
        size_of_company,
        amount_of_money,
        innovation,
        company_sector,
        company_subsector
    )

    financial_cost = lc.get_financial_cost(similar_product_df)

    wighted_fee, wighted_grace, wighted_amortization = lc.get_weighted_information(
        cached_df,
        similar_product_df,
        financial_cost,
        amount_of_money,
        today_year
    )

    st.write(
    """
        Produto BNDES indicado: **{product}**

        Confiança do modelo: **{prediction_prob}%**

        Custo financeiro: **{financial_cost}**

        Taxa de juros de: **{fee}% a.a**

        Prazo de carência de: **{grace} meses**

        Prazo de amortização de: **{amortization} meses**
    """.format(
        product=product_prediction,
        prediction_prob=round(product_prediction_prob,4)*100,
        financial_cost=financial_cost,
        fee=round(wighted_fee, 2),
        grace=int(round(wighted_grace)),
        amortization=int(round(wighted_amortization))
        )
    )

    st.write(
    """
        ##
        A seguir você pode conferir os 5 financiamento feitos no passado mais parecidos com os dados fornecidos:
    """
    )

    result_columns = ["produto", "juros", "prazo_carencia_meses", "prazo_amortizacao_meses"]
    similar_df = similar_product_df[training_columns + result_columns]
    st.table(similar_df)
