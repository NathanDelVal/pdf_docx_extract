import pandas as pd
import re
import tabula
import regexes
from unidecode import unidecode

counter = 0

pdf_tables = []
pdf_tables_data = []
area = [78.40, 31.15, 146.29, 804.66]

table_headers = tabula.read_pdf("./amostragem/teste2.pdf", pages='all', encoding="latin-1", stream=True, area=area)

headers = []

# Loop through each detected table (DataFrame)
for i, df in enumerate(table_headers, start=1):
    # Skip if DataFrame is empty
    if df.empty or len(df) < 2:
        continue

    # Loop through rows using iloc, starting at index 1
    for i in range(1, len(df)):
        data = [str(cell) for cell in df.iloc[i] if pd.notna(cell) and re.match(regexes.re_extract_table_summary, str(cell), re.IGNORECASE)]
        print(data)

dfs = tabula.read_pdf("./amostragem/teste2.pdf", pages='all', encoding="latin-1", lattice=True)
dfs = [t for t in dfs if re.search("20[0-9]{2}", t.to_string()) and re.search("an[aá]lise", t.to_string(), re.IGNORECASE)]

for df in dfs:
    counter += 1
    data_structure = {"nome": f"Tabela {counter}", "meses": [], "dados": []} 
    temp_arr = []

    for i, r in df.iterrows():
        if re.findall(r"1\.\s*par[aâ]metro", r.to_string(), re.IGNORECASE):
            if temp_arr:  # ✅ Avoid appending empty arrays
                data_structure["daods"] += temp_arr
            temp_arr = []
        
        if re.findall(regexes.re_month, r.to_string(), re.IGNORECASE):
            months = re.findall(regexes.re_month, str({v for v in r}), re.IGNORECASE)
            if len(months) > 4:
                data_structure["meses"] = months
        
        if re.findall(regexes.re_parametros, r.to_string(), re.IGNORECASE):
            data = [v for v in r if pd.notna(v)]
            temp_arr.append(data)

    # ✅ Append remaining temp_arr after loop finishes
    if temp_arr:
        data_structure["dados"].extend(temp_arr)

    pdf_tables_data.append(data_structure)  # ✅ Each table gets its own independent dict
    
# print(pdf_tables_data[2])