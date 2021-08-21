import streamlit as st

class Faq: 

    def __init__(self) -> None:
        self.pages = []
    
    def add_page(self, title, func) -> None: 

        self.pages.append({
                "title": title, 
                "function": func
            })

    def run(self):
        # Drodown to select the page to run  
        page = st.sidebar.selectbox(
            'Selecione a página', 
            self.pages, 
            format_func=lambda page: page['title']
        )

        page['function']()