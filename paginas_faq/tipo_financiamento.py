import streamlit as st

import plots

def get_page_information(cached_df):
    st.title("O que pode ser financiado?")

    st.write(
    """
        O BNDES financia a quase totalidade dos setores da economia, dentre eles: infraestrutura; indústria, comércio e serviços;
        agropecuária; exportação; desenvolvimento regional e territorial; cultura e economia criativa; entre outros.

        A seguir você consegue visualizar interativamente a porcentagem de financiamentos por setor, podendo ser filtrado por ano ou removido algum setor.
        ##

    """)

    row1_1, row1_2 = st.columns((1,1))

    with row1_1:
        sector_type = st.radio(
            "Escolha o tipo de setor",
            ("BNDES", "CNAE")
        )

    with row1_2:
        min_year, max_year = st.slider("Filtro por ano", 2002, 2021, (2002, 2021))

    boolean_series = (cached_df['ano_contratado'] >= min_year) & (cached_df['ano_contratado'] <= max_year)
    filtered_df = cached_df[boolean_series]

    st.plotly_chart(
        plots.get_pie_chart(
            filtered_df,
            "Setor {}".format(sector_type),
            title='Visualização interativa de setor financiado nos anos de {} a {}'.format(min_year, max_year)),
        use_container_width=True)

    if sector_type == "CNAE":
        sector_type = sector_type + " agrupado"

    st.plotly_chart(
        plots.get_pie_chart(
            filtered_df,
            "Subsetor {}".format(sector_type),
            title='Visualização interativa de subsetor financiado nos anos de {} a {}'.format(min_year, max_year)),
        use_container_width=True)