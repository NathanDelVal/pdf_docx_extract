import pandas as pd
import re
import tabula

### REGEX'S PARA CAPTURA###
re_month = r"janeiro|fevereiro|mar[cç]o|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro"
re_parametros = r"\d+\s+?(semana(l|is)|mensa(l|is)|trimestra(l|is)|bimestra(l|is)|anua(l|is))"
################

tables_list = []
count = 0

dfs = tabula.read_pdf("./amostragem/teste2.pdf", pages='all', encoding="latin-1", lattice=True)
dfs = [t for t in dfs if re.search("20[0-9]{2}", t.to_string()) and re.search("an[aá]lise", t.to_string(), re.IGNORECASE)]

for df in dfs:
    count += 1
    data_structure = {"name": f"Tabela {count}", "months": [], "data": []}  # ✅ New dict for each table
    temp_arr = []

    for i, r in df.iterrows():  
        if re.findall(r"1.\s?par[aâ]metro", r.to_string(), re.IGNORECASE):
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

    tables_list.append(data_structure)  # ✅ Each table gets its own independent dict
    
print(tables_list[0])