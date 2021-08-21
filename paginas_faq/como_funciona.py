import streamlit as st

import plots

def get_page_information(cached_df):
    st.title("Como funciona o financiamento?")

    st.write(
    """
        O apoio financeiro do BNDES pode ser realizado por meio de:

        - financiamentos com recursos reembolsáveis;
        - financiamentos com recursos não reembolsáveis;
        - subscrição de valores mobiliários;
        - fundos de investimento de fomento a empresas nascentes, iniciantes ou em estágio de crescimento.
        ##
        Em alguns casos, o apoio financeiro pode ser feito de forma conjugada, combinando, por exemplo, financiamento com subscrição de valores mobiliários, a critério do BNDES.
        As operações de financiamento podem ser realizadas de forma direta, indireta ou mista (saiba mais):
        - **Operação direta**: realizada diretamente com o BNDES ou através de mandatário (via de regra, são financiamentos a projetos de investimento de valor superior a R$ 10 milhões);
        - **Operação indireta automática**: realizada por meio de instituições financeiras credenciadas. Estas realizam a análise e aprovação do crédito, que é, em seguida, homologado pelo BNDES;
        - **Operação indireta não automática**: similar à operação indireta automática, porém o BNDES também analisa e aprova ao crédito, após a análise da instituição financeira (via de regra, são financiamentos de valor superior a R$ 10 milhões);
        - **Operação mista**: combina as forma direta e indireta de apoio.
    """)

    st.title("Evolução das formas de financiamento")

    row1_1, row1_2 = st.columns((1, 1))

    with row1_1:
        aggregation_type = st.radio(
            "Tipo de agregação",
            ("Quantidade de projetos", "Valor financiado")
        )
        use_sum = True if aggregation_type == "Valor financiado" else False

    with row1_2:
        min_year, max_year = st.slider("Filtro por ano", 2002, 2021, (2002, 2021))

    st.write(
    """
        O apoio direto (veja Formas de Apoio) com o BNDES pode ser solicitado para projetos de investimento a partir de R$ 10 milhões. Conheça as linhas do BNDES Finem e acesse o Navegador de Financiamento para saber mais detalhes sobre cada uma delas.
    """)
    
    boolean_series = (cached_df["ano_contratado"] >= min_year) & (cached_df["ano_contratado"] <= max_year)
    filtered_by_year_df = cached_df[boolean_series]

    #pie plot
    st.plotly_chart(
        plots.get_pie_chart(
            filtered_by_year_df,
            "Forma de apoio",
            title="Porcentagem de {} por forma de apoio nos anos de {} a {}".format(aggregation_type.lower(), min_year, max_year),
            use_sum=use_sum
            ),
        use_container_width=True
    )

    #bar plot
    st.plotly_chart(
        plots.get_histogram(
            dataframe=filtered_by_year_df,
            column="Forma de apoio",
            group_by_lst=["ano_contratado", "Forma de apoio"],
            rename_dict={"ano_contratado": "Ano"},
            use_sum=use_sum
        ),
        use_container_width=True
    )
    
    #colocar exemplo do df
    st.write(filtered_by_year_df)

    st.title("Tem algum financiamento feito no passado parecido com o que eu preciso?")
    #busca financiamento parecido
    #colocar exemplo do df

    st.write(
    """
        ##
        Os requisitos mínimos para obter apoio financeiro do BNDES são:

        - estar em dia com obrigações fiscais, tributárias e sociais;
        - apresentar cadastro satisfatório;
        - ter capacidade de pagamento;
        - dispor de garantias suficientes para cobertura do risco da operação;
        - não estar em regime de recuperação de crédito;
        - atender a legislação relativa à importação, no caso de financiamento para a importação de bens e serviços; e
        - cumprir a legislação ambiental
    """)