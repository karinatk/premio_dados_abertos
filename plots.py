import plotly.express as px

def get_pie_chart(dataframe, column, title):
    series_counts = dataframe[column].value_counts()
    values = series_counts.tolist()
    names = series_counts.index.tolist()
    fig = px.pie(
        values=values,
        names=names,
        color_discrete_sequence=px.colors.sequential.Teal,
        title=title
    )
    #fig.update_layout(width=500,height=300)
    return fig