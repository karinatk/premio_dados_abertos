import streamlit as st

import plots

def get_page_information(cached_df):
    st.title("O que pode ser financiado?")

    st.write(
    """
        O BNDES financia a quase totalidade dos setores da economia, dentre eles: infraestrutura; indústria, comércio e serviços;
        agropecuária; exportação; desenvolvimento regional e territorial; cultura e economia criativa; entre outros.

        A seguir você consegue visualizar interativamente a porcentagem de financiamentos por setor, podendo ser escolhido o tipo de classificação de setor, o tipo de agregação dos dados e filtros de intervalos de anos.
        ##
    """)

    row1_1, row1_2, row1_3 = st.columns((1, 1, 1))
    sector_classification_type = "BNDES"

    with row1_1:
        sector_classification_type = st.radio(
            "Tipo de classificação de setor",
            ("BNDES", "CNAE")
        )
        sector_column = "Setor {}".format(sector_classification_type)

    with row1_2:
        aggregation_type = st.radio(
            "Tipo de agregação",
            ("Quantidade de projetos", "Valor financiado")
        )
        use_sum = True if aggregation_type == "Valor financiado" else False

    with row1_3:
        min_year, max_year = st.slider("Filtro por ano", 2002, 2021, (2002, 2021))

    st.write("##")
    st.title("O que já financiamos?")#"Classificação de setor do {}".format(sector_classification_type))
    st.write(
    """
        As seguintes visualizações são interativas e geradas a partir dos filtros passados anteriormente.
        Nos gráficos a seguir você poderá conferir informações de {} nos anos de {} a {} por setor.
        Caso deseje remover algum setor da visualização, apenas clique no nome do setor.
        Também é possível expandir as visualizações ou salvar as imagens geradas.
    """.format(aggregation_type.lower(), min_year, max_year)
    )

    boolean_series = (cached_df["ano_contratado"] >= min_year) & (cached_df["ano_contratado"] <= max_year)
    filtered_by_year_df = cached_df[boolean_series]

    st.plotly_chart(
        plots.get_pie_chart(
            filtered_by_year_df,
            sector_column,
            title="Porcentagem de {} por setor nos anos de {} a {}".format(aggregation_type.lower(), min_year, max_year),
            use_sum=use_sum
            ),
        use_container_width=True
    )

    st.plotly_chart(
        plots.get_histogram(
            dataframe=filtered_by_year_df,
            column=sector_column,
            group_by_lst=["ano_contratado", sector_column],
            rename_dict={"ano_contratado": "Ano"},
            use_sum=use_sum
        ),
        use_container_width=True
    )

    st.write(filtered_by_year_df)

    sector_type = st.radio(
        "Escolha um setor",
        filtered_by_year_df[sector_column].unique().tolist()
    )

    st.write("##")
    st.title("Classificação {} - Subsetor {}".format(sector_classification_type, sector_type))

    if sector_classification_type == "CNAE":
        sector_classification_type += " agrupado"
    subsector_column = "Subsetor {}".format(sector_classification_type)

    filtered_by_sector_df = filtered_by_year_df[filtered_by_year_df[sector_column] == sector_type]

    st.plotly_chart(
        plots.get_pie_chart(
            filtered_by_sector_df,
            subsector_column,
            title="Porcentagem de {} por subsetores de {} nos anos de {} a {}".format(aggregation_type.lower(), sector_type.lower().strip(), min_year, max_year),
            use_sum=use_sum
            ),
        use_container_width=True
    )

    st.plotly_chart(
        plots.get_histogram(
            dataframe=filtered_by_sector_df,
            column=subsector_column,
            group_by_lst=["ano_contratado", subsector_column],
            rename_dict={"ano_contratado": "Ano"},
            use_sum=use_sum
        ),
        use_container_width=True
    )

    st.write(filtered_by_sector_df)