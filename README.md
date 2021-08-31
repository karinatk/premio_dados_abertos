# Prêmio Dados Abertos para o Desenvolvimento BNDES

Repositório com aplicação em Python feita com Streamlit para simular o financiamento do BNDES.

## Como rodar a aplicação principal?

Para rodar a aplicação principal você precisará ter o Python instalado na sua máquina com uma versão superior ou igual 3.8.5.
Também é recomendado que seja usado o Anaconda.

- acesse o diretório do projeto em premio_dados_abertos
- (recomendado) crie um ambiente virtual para rodar o projeto:
```bash
conda create -n financiamento_bndes python=3.8.5 anaconda
conda activate financiamento_bndes
```
- instale as dependências que estão no arquivo requirements.txt com o comando:

```bash
pip install -r requirements.txt
```

- baixe os arquivos necessários:
```bash
./download_files.sh
```

- rode a aplicação com o comando:
```bash
streamlit run main.py
```
Pronto, uma nova janela será aberta com a aplicação de simulação de financiamento do BNDES!

*Se a janela não abrir automaticamente, cole em seu navegador: **http://localhost:8501**

## Preciso rodar os notebooks também?

Não, você não precisa executar os notebooks, pois os arquivos necessários (bndes_financiamentos.csv, encoder.json, modelo_produto.pkl) já estão no projeto. Porém, se quiser executá-los, basta apenas:
- acesse o diretório do projeto em premio_dados_abertos/files
- instale as dependências que estão no arquivo jupyter_notebook_requirements.txt com o comando:
```bash
pip install -r jupyter_notebook_requirements.txt
```
- rode o notebook com o comando:
```bash
jupyter notebook
```
- escolha o notebook e clique na aba **Cell** no comando **Run all**

## Arquitetura

![Modelo BNDES](files/images/gerar_modelo_bndes.png?raw=true "Title")

![Simulação de financiamento](files/images/simulacao_financiamento_bndes.png?raw=true "Title")

## Licença
[Open Data Commons Open Database License (ODbL) v1.0](https://opendatacommons.org/licenses/odbl/1-0/)