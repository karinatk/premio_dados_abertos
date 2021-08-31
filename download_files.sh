#!/bin/bash

fileid="1yOT5veyYHLuZNYdu4dJt6b-FP0c-SRiv"
filename="./files/models/modelo_produto.pkl"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}

fileidcsv="1-DJTxRkDqkvKBVXM6XqChHKNcw8pQaTq"
filenamecsv="./files/csv/output_csv/bndes_financiamentos.csv"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileidcsv}" > /dev/null
curl --create-dirs -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileidcsv}" -o ${filenamecsv}

rm cookie