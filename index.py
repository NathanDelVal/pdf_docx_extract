import tabula
import re
import pandas as pd

### REGEX'S PARA CAPTURA###
re_month = r"janeiro|fevereiro|mar[cç]o|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro"
re_parametros = r"[0-9]+[\r\s]+?semana(l|is)|mensa(l|is)|trimestra(l|is)|bimestra(l|is)"
################

data_structure = {"name": "", "months": [], "data": []}

temp_arr = []

tables_list = []

count = 0

dfs = tabula.read_pdf("./amostragem/teste2.pdf", pages='all', encoding="latin-1", lattice=True)
dfs = [t for t in dfs if re.search("20[0-9]{2}", t.to_string()) and re.search("an[aá]lise", t.to_string(), re.IGNORECASE)]
for df in dfs:
    count += 1
    data_structure["name"] = f"Tabela {count}"
    temp_dict = {}
    for i, r in df.iterrows():
        # print(r)
        if re.findall(re_month, r.to_string(), re.IGNORECASE):
            months = {v for v in r if pd.isna(v) is False}
            months = re.findall(re_month, str(months), re.IGNORECASE)
            if len(months) > 4:
                data_structure["months"].append(months)
        
        if re.findall(re_parametros, r.to_string(), re.IGNORECASE):
            data =  [v for v in r if pd.isna(v) is False]
            temp_arr.append(data)
    
        if re.findall(r"1.\s?par[aâ]metro", r.to_string(), re.IGNORECASE):
            data_structure["data"].append(temp_arr)
            temp_arr = []
    tables_list.append(data_structure)
    
print(tables_list[0])