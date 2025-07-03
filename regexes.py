### REGEX'S ###
re_month = r"(janeiro|fevereiro|mar[cç]o|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)"
re_find_table_summary = r"\bano[\:\-\s]+.*sistema(?:/solu[cç][aã]o alternativa)?[\:\-\s]+.*municipio[\:\-\s]+.*data[:=\s]+.*"
re_extract_table_summary = r"\b(?:ano|sistema(?:/solu[cç][aã]o alternativa)?|municipio|uts|data)\b[\:\-\s]+.*?(?=\s+\b(?:ano|sistema|municipio|data|$)\b|$)"
re_extract_date = r"(\d{2}\/\d{2}\/\d{4})"
re_parametros = r"(?:trimestral?(?:is)?|semanal?(?:is)?|mensal?(?:is)?|bimestral?(?:is)?|anual?(?:is)?|semestral?(?:is)?)"
