import os
import json
import streamlit as st
import pandas as pd
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

def read_json(path):
    with open(path, encoding='utf-8') as f:
        dict = json.loads(f.read())
    return dict

#@st.cache(hash_funcs={dict: lambda _: None})
def get_map(dataframe):
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'geojson', 'brazil-states.json')
    brazil_dict = read_json(path)
    state_dict = {}
    for feature in brazil_dict["features"]:
        state = feature["properties"]["name"]
        state_abbreviation = feature["properties"]["sigla"]
        state_dict[state_abbreviation] = state
    bndes_state_count = dataframe.groupby(['UF', 'ano_contratado']).CNPJ.count().reset_index()
    bndes_state_count.rename({"CNPJ": "Contagem CNPJ", "ano_contratado": "Ano"}, inplace=True, axis=1)
    dataframe["Estado"] = dataframe["UF"].apply(lambda uf: state_dict.get(uf, None))
    dataframe.dropna(inplace=True)
    bndes_state_count = dataframe.groupby(['Estado', 'ano_contratado']).CNPJ.count().reset_index()
    bndes_state_count.rename({"CNPJ": "Contagem CNPJ", "ano_contratado": "Ano"}, inplace=True, axis=1)
    bndes_state_count
    figure_dict = {}
    fig = px.choropleth(
        bndes_state_count,
        locations = "Estado",
        geojson = brazil_dict,
        color = "Contagem CNPJ",
        hover_name = "Estado",
        hover_data =["Contagem CNPJ"],
        title = "Contagem de CNPJ por estado com financiamento BNDES por ano",
        animation_frame = "Ano"
    )
    fig.update_geos(fitbounds = "locations", visible = False)
    figure_dict['map'] = fig
    return figure_dict