import plotly.express as px

class BndesDataframe:

    def __init__(self, dataframe, all_columns: list) -> None:
        self.set_dataframe(dataframe[all_columns])

    def get_dataframe():
        return self.dataframe
    
    def set_dataframe(self, dataframe):
        self.dataframe = dataframe

    def filter(self, column_to_filter: str, value_to_filter):
        filtered_dataframe = self.dataframe[self.dataframe[column_to_filter] == value_to_filter]
        set_dataframe(filtered_dataframe)

    def get_pie_chart(self, column):
        series_counts = self.dataframe[column].value_counts()
        values = series_counts.tolist()
        names = series_counts.index.tolist()
        fig = px.pie(
            values=values,
            names=names,
            color_discrete_sequence=px.colors.sequential.Teal
        )
        return fig