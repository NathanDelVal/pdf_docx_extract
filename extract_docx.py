from docx import Document
from unidecode import unidecode
import os
import re

### REGEX'S ###
re_month = r"(janeiro|fevereiro|mar[cç]o|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)"
re_find_table_summary = r"ano[\:\-\s]+.*sistema[\:\-\s]+.*municipio[\:\-\s]+.*data[:=\s]+.*"
re_extract_table_summary = r"\b(?:ano|sistema|municipio|data|uts)\b[\:\-\s]+[^:]+?(?=\s+\b(?:ano|sistema|municipio|data)\b|$)"
re_extract_date = r"(\d{2}\/\d{2}\/\d{4})"

counter = 0

docx_tables = []
docx_tables_data = []
temp_arr = []

# Load the .docx file
doc = Document("./amostragem/teste.docx")
# Print each paragraph
for para in doc.paragraphs:
    if re.findall(re_find_table_summary, unidecode(para.text), re.IGNORECASE):
        data = re.findall(re_extract_table_summary, unidecode(para.text), re.IGNORECASE)      
        for i in range(0, len(data), 4):
            counter += 1
            summary_structure = {"ano": "", "sistema": "", "municipio": "", "data": ""}
            summary_structure["ano"] = re.split(r"^\w+[\-\:\s]+", re.split(r"[\:\-](?=\b\w+\b)", data[i], re.IGNORECASE)[0], re.IGNORECASE)[1]
            summary_structure["sistema"] = re.split(r"^\w+[\-\:\s]+", re.split(r"[\:\-](?=\b\w+\b)", data[i+1], re.IGNORECASE)[0], re.IGNORECASE)[1]
            summary_structure["municipio"] = re.split(r"^\w+[\-\:\s]+", re.split(r"[\:\-](?=\b\w+\b)", data[i+2], re.IGNORECASE)[0], re.IGNORECASE)[1]
            summary_structure["data"] = re.findall(re_extract_date, data[i+3], re.IGNORECASE)
            data_structure = {"nome": f"cabecalho {counter}", "meses": [], "dados": [], "dados_de_cabecalho": summary_structure}
            docx_tables.append(data_structure)
# print(docx_tables[-1])
counter = 0

for t in doc.tables:
    table_rows = []
    for r in t.rows:
        row_data = [cell.text.strip() for cell in r.cells]
        table_rows.append(row_data)
    temp_arr.append(table_rows)
        
print(temp_arr)

for t in range(len(temp_arr)):
    for r in range(len(temp_arr[t])):
        if re.search(r"(3.frequ[eê]ncia)", str(temp_arr[t][r]), re.IGNORECASE):
            temp_arr[t] = temp_arr[t][r+1:]
            break
        
# print([len(t) for t in temp_arr])
# print(temp_arr[0])

for t in temp_arr:
    temp_arr = [r[0] for r in t if r[0]]
    temp_arr = {key: [] for key in temp_arr}
    counter += 1
    data_structure = {"nome": f"tabela {counter}", "dados": temp_arr}
    for r in range(len(t)):
        if t[r][0] in temp_arr:
            data_structure["dados"][t[r][0]] += [cell for cell in t[r][1:]]
        else:
            data_structure["dados"][t[r-1][0]] = [data_structure["dados"][t[r-1][0]],t[r][1:]]
    docx_tables_data.append(data_structure)
    
# print(docx_tables_data[-1])

        
        
