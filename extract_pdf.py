import pandas as pd
import re
import tabula
import regexes
from unidecode import unidecode

counter = 0

filename = "teste5.pdf"
pdf_tables_data = []
pdf_tables = []
area = [78.40, 31.15, 146.29, 804.66]

table_headers = tabula.read_pdf(f"./amostragem/{filename}", pages='all', encoding="latin-1", stream=True, area=area)

# Loop through each detected table (DataFrame)
for i, df in enumerate(table_headers, start=1):
    # Skip if DataFrame is empty
    if df.empty or len(df) < 2:
        continue

    # Loop through rows using iloc, starting at index 1
    for i in range(1, len(df)):
        data = [str(cell) for cell in df.iloc[i] if pd.notna(cell) and re.match(regexes.re_extract_table_summary, str(cell), re.IGNORECASE)]
        if re.search(r"\bano[\:\s\-]+", str(data), re.IGNORECASE):
            pdf_tables += [data]
        elif re.search(r"\buts[\:\s\-]+", str(data), re.IGNORECASE):
            pdf_tables[-1] = [str(cell) for cell in df.iloc[i - 1]] + data

pdf_tables = {f"cabecalho {h + 1}":{"tabelas": [], "dados de cabecalho": pdf_tables[h]} for h in range(len(pdf_tables))}

dfs = tabula.read_pdf("./amostragem/teste2.pdf", pages='all', encoding="latin-1", lattice=True)
dfs = [t for t in dfs if re.search("20[0-9]{2}", t.to_string()) and re.search("an[aá]lise", t.to_string(), re.IGNORECASE)]

for df in dfs:
    counter += 1
    data_structure = {f"tabela {counter}":{"dados":[],"meses":[]}}
    temp_arr = []

    for i, r in df.iterrows():
        if re.findall(r"1\.\s*par[aâ]metro", r.to_string(), re.IGNORECASE):
            if temp_arr:  # ✅ Avoid appending empty arrays
                data_structure[f"tabela {counter}"]["dados"] += temp_arr
            temp_arr = []
        
        if re.findall(regexes.re_month, r.to_string(), re.IGNORECASE):
            months = re.findall(regexes.re_month, str({v for v in r}), re.IGNORECASE)
            if len(months) > 4:
                data_structure[f"tabela {counter}"]["meses"] = months
        
        if re.findall(regexes.re_parametros, r.to_string(), re.IGNORECASE):
            data = [v for v in r if pd.notna(v)]
            temp_arr.append(data)

    # ✅ Append remaining temp_arr after loop finishes
    if temp_arr:
        data_structure[f"tabela {counter}"]["dados"].extend(temp_arr)

    pdf_tables_data.append(data_structure)  # ✅ Each table gets its own independent dict
  
pdf_tables_data = {list(pdf_tables_data[i].keys())[0]:pdf_tables_data[i][list(pdf_tables_data[i].keys())[0]] for i in range(len(pdf_tables_data))}

# print(pdf_tables_data)

decrementer = 0

try:
    for x in range(len(pdf_tables_data)):
        if "Dezembro" not in pdf_tables_data[f"tabela {x + 1}"]["meses"]:
            pdf_tables[f"cabecalho {x - decrementer + 1}"]["tabelas"].append({f"tabela {x + 1}":pdf_tables_data[f"tabela {x + 1}"]})
            decrementer += 1
        else:
            pdf_tables[f"cabecalho {x - decrementer + 1}"]["tabelas"].append({f"tabela {x + 1}":pdf_tables_data[f"tabela {x + 1}"]}) 
except:
    pass

filename = f"{filename.split(".")[0]}_pdf_extraction.txt"

with open(filename, "w", encoding="utf-8") as f:
    f.write(str(pdf_tables))

print(f"✅ File '{filename}' has been written to the current directory.")