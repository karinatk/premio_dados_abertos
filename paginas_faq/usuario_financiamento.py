import streamlit as st

import plots

def get_page_information(cached_df):
    st.title("Quem pode obter o financiamento?")

    st.write(
    """
        Podem obter financiamento com recursos do BNDES:
        - empresas privadas, de qualquer porte, sediadas no Brasil;
        - associações e fundações;
        - empresário individual que exerça atividade produtiva e esteja inscrito no Registro Público de Empresas Mercantis e no Cadastro Nacional de Pessoas Jurídicas (CNPJ);
        pessoas físicas (microempreendedor, produtor rural e caminhoneiro);
        - Administração Pública, direta e indireta; e empresas sediadas no exterior, com a condição de que o acionista com maior capital votante e que exerça influência dominante sobre as atividades nelas desempenhadas, conforme juízo a ser feito pelo BNDES, seja: 
            - pessoa jurídica controlada, direta ou indiretamente, por pessoa física ou grupo de pessoas físicas, domiciliadas e residentes no Brasil;
            - pessoa jurídica controlada por pessoa jurídica de direito público interno.
    """)

    st.title("Evolução do financiamento em relação ao porte das empresas")

    row1_1, row1_2 = st.columns((1, 1))

    with row1_1:
        aggregation_type = st.radio(
            "Tipo de agregação",
            ("Quantidade de projetos", "Valor financiado")
        )
        use_sum = True if aggregation_type == "Valor financiado" else False

    with row1_2:
        min_year, max_year = st.slider("Filtro por ano", 2002, 2021, (2002, 2021))

    boolean_series = (cached_df["ano_contratado"] >= min_year) & (cached_df["ano_contratado"] <= max_year)
    filtered_by_year_df = cached_df[boolean_series]

    #pie plot
    st.plotly_chart(
        plots.get_pie_chart(
            filtered_by_year_df,
            "Porte do cliente",
            title="Porcentagem de {} por porte do cliente nos anos de {} a {}".format(aggregation_type.lower(), min_year, max_year),
            use_sum=use_sum
            ),
        use_container_width=True
    )

    #bar plot
    st.plotly_chart(
        plots.get_histogram(
            dataframe=filtered_by_year_df,
            column="Porte do cliente",
            group_by_lst=["ano_contratado", "Porte do cliente"],
            rename_dict={"ano_contratado": "Ano"},
            use_sum=use_sum
        ),
        use_container_width=True
    )

    #colocar exemplo do df
    st.write(filtered_by_year_df)
    

    st.title("Porte das empresas financiadas X Produtos de financiamento")
    #bar plot

    st.plotly_chart(
        plots.get_pie_chart(
            filtered_by_year_df,
            "Produto",
            title="Porcentagem de {} por produto nos anos de {} a {}".format(aggregation_type.lower(), min_year, max_year),
            use_sum=use_sum
            ),
        use_container_width=True
    )
    
    filtered_by_year_df["produto"] = filtered_by_year_df["Produto"].str.replace("BNDES", "")
    st.plotly_chart(
        plots.get_histogram(
            dataframe=filtered_by_year_df,
            column="Porte do cliente",
            group_by_lst=["Porte do cliente", "produto"],
            rename_dict={"produto": "Produto"},
            use_sum=use_sum
        ),
        use_container_width=True
    )

    st.title("Porte da empresa financiadas X Região")
    #map plot
    #fig_dict = plots.get_map(filtered_by_year_df)
    #st.plotly_chart(fig_dict['map'])

    st.plotly_chart(
        plots.get_pie_chart(
            filtered_by_year_df.drop_duplicates(subset=["CNPJ"]),
            "UF",
            title="Porcentagem de {} por região nos anos de {} a {}".format(aggregation_type.lower(), min_year, max_year),
            use_sum=use_sum
            ),
        use_container_width=True
    )

    st.plotly_chart(
        plots.get_histogram(
            dataframe=filtered_by_year_df.drop_duplicates(subset=["CNPJ"]),
            column="Porte do cliente",
            group_by_lst=["Porte do cliente", "UF"],
            rename_dict={"UF": "Estado"},
            use_sum=use_sum
        ),
        use_container_width=True
    )
    #colocar exemplo do df