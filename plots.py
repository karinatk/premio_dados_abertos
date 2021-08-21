import pandas as pd
#import geopandas as gpd
import plotly.express as px

def get_pie_chart(dataframe, column, title, use_sum=False):
    agg_func = get_agg_function(use_sum)
    name = get_name(use_sum)
    grouped = dataframe.groupby([column]).apply(agg_func, column=column, name=name).reset_index()

    fig = px.pie(
        values=grouped[name].tolist(),
        names=grouped[column].tolist(),
        color_discrete_sequence=px.colors.sequential.Teal,
        title=title
    )
    return fig

def count_agg(df, column, name):
    names = {name:  df[column].count()}
    return pd.Series(names, index=[name])

def sum_agg(df, column, name):
    names = {name:  df["valor_contratado"].sum()}
    return pd.Series(names, index=[name])

def rename_title(title):
    len_title = len(title.text)
    len_limit = 6
    new_title = title.text.split("=")[-1]
    if len_title >= len_limit:
        first_word = new_title.split(" ")[0]
        if len(first_word) >= len_limit:
            new_title = first_word[:6]+"."
        else:
            new_title = first_word
    return title.update(text=new_title)

def get_agg_function(use_sum):
    agg_func = sum_agg if use_sum == True else count_agg
    return agg_func

def get_name(use_sum):
    name = "Valor financiado" if use_sum == True else "Contagem"
    return name

def get_histogram(dataframe, column, group_by_lst, rename_dict, use_sum=False):
    agg_func = get_agg_function(use_sum)
    y_name = get_name(use_sum)
    grouped = dataframe.groupby(group_by_lst).apply(agg_func, column=column, name=y_name).reset_index()
    grouped.rename(columns=rename_dict, inplace=True)
    fig = px.bar(grouped, x=list(rename_dict.values())[0], y=y_name, facet_col=column)
    fig.for_each_annotation(rename_title)
    return fig

def get_map(dataframe):
    path = "C:/Users/karina.kato_ifood/Documents/BNDES/bcim_2016_21_11_2018.gpkg"
    state_data = gpd.read_file(path, layer="lim_unidade_federacao_a")
    bndes_state_count = dataframe.groupby(['UF']).CNPJ.count().reset_index()
    bndes_state_count.rename({"UF": "sigla"}, axis=1, inplace=True)
    brasil_map = state_data.merge(bndes_state_count, on="sigla", how="left")
    fig = brasil_map.plot(column="CNPJ", cmap="Blues")
    return fig