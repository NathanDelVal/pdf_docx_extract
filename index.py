import pandas as pd
import re
import tabula
import os
from docx import Document
from unidecode import unidecode


### REGEX'S PARA CAPTURA###
re_month = r"janeiro|fevereiro|mar[cç]o|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro"
re_parametros = r"(?:trimestral?(?:is)?|semanal?(?:is)?|mensal?(?:is)?|bimestral?(?:is)?|anual?(?:is)?|semestral?(?:is)?)"
re_find_table_summary = r"ano[\:\-\s]+.*sistema[\:\-\s]+.*municipio[\:\-\s]+.*data[:=\s]+.*"
re_extract_table_summary = r"\b(?:ano|sistema|municipio|data|uts)\b[\:\-\s]+[^:]+?(?=\s+\b(?:ano|sistema|municipio|data)\b|$)"
re_extract_date = r"(\d{2}\/\d{2}\/\d{4})"
###################

pdf_tables = []
docx_tables = []
count = 0

dfs = tabula.read_pdf("./amostragem/teste2.pdf", pages='all', encoding="latin-1", lattice=True)
dfs = [t for t in dfs if re.search("20[0-9]{2}", t.to_string()) and re.search("an[aá]lise", t.to_string(), re.IGNORECASE)]

# Load the .docx file
doc = Document("./amostragem/teste.docx")
# Print each paragraph
for para in doc.paragraphs:
    if re.findall(re_find_table_summary, unidecode(para.text), re.IGNORECASE):
        data = re.findall(re_extract_table_summary, unidecode(para.text), re.IGNORECASE)      
        for i in range(0, len(data), 4):
            summary_structure = {"ano": "", "sistema": "", "municipio": "", "data": ""}
            summary_structure["ano"] = re.split(r"^\w+[\-\:\s]+", re.split(r"[\:\-](?=\b\w+\b)", data[i], re.IGNORECASE)[0], re.IGNORECASE)[1]
            summary_structure["sistema"] = re.split(r"^\w+[\-\:\s]+", re.split(r"[\:\-](?=\b\w+\b)", data[i+1], re.IGNORECASE)[0], re.IGNORECASE)[1]
            summary_structure["municipio"] = re.split(r"^\w+[\-\:\s]+", re.split(r"[\:\-](?=\b\w+\b)", data[i+2], re.IGNORECASE)[0], re.IGNORECASE)[1]
            summary_structure["data"] = re.findall(re_extract_date, data[i+3], re.IGNORECASE)
            data_structure = {"name": f"Tabela {i}", "months": [], "data": [], "summary_structure": summary_structure}
            # print(data)
          
for df in dfs:
    count += 1
    data_structure = {"name": f"Tabela {count}", "months": [], "data": []} 
    temp_arr = []

    for i, r in df.iterrows():
        if re.findall(r"1\.\s*par[aâ]metro", r.to_string(), re.IGNORECASE):
            if temp_arr:  # ✅ Avoid appending empty arrays
                data_structure["data"] += temp_arr
            temp_arr = []
        
        if re.findall(re_month, r.to_string(), re.IGNORECASE):
            months = {v for v in r if pd.notna(v)}
            months = re.findall(re_month, str(months), re.IGNORECASE)
            if len(months) > 4:
                data_structure["months"] = months
        
        if re.findall(re_parametros, r.to_string(), re.IGNORECASE):
            data = [v for v in r if pd.notna(v)]
            temp_arr.append(data)

    # ✅ Append remaining temp_arr after loop finishes
    if temp_arr:
        data_structure["data"].extend(temp_arr)

    pdf_tables.append(data_structure)  # ✅ Each table gets its own independent dict
    
# print(pdf_tables[0])