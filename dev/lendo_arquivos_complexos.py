import os
import pandas as pd
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
cliente_ia = OpenAI()

# ====================================================================
# TODO 1: LEITURA DO "PDF" (Lendo o texto sujo)
# ====================================================================
# Leia o arquivo 'fatura_suja_01.txt' e guarde todo o conteúdo
# em uma variável chamada 'texto_bruto'.

caminho_arquivo = 'exemplo/nota-fiscal-notebook-dell.pdf'

leitor = PdfReader(caminho_arquivo)
texto_bruto = ""
for pagina in leitor.pages:
    texto_bruto += pagina.extract_text()

# ====================================================================
# TODO 2: EXTRAÇÃO INTELIGENTE COM IA (Structured Output)
# ====================================================================
# Use a API da OpenAI para analisar o 'texto_bruto'.
# CRIE UM SYSTEM PROMPT EXTREMAMENTE RÍGIDO pedindo que a IA
# devolva a resposta NO FORMATO JSON com as chaves:
# "nome_empresa", "data_vencimento", "valor" (só os números).

prompt_sistema = """
Você é um extrator de dados de notas fiscais.
Analise o texto abaixo e retorne SOMENTE um JSON válido, sem explicações, sem markdown.
O JSON deve ter exatamente estas 3 chaves:
- "nome_empresa": nome da empresa emitente
- "data_vencimento": data de emissão no formato DD/MM/AAAA
- "valor": apenas os números do valor total da nota, sem R$ ou pontos (ex: 3254.07)
"""

resposta = cliente_ia.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": prompt_sistema},
        {"role": "user", "content": texto_bruto}
    ]
)

texto_resposta = resposta.choices[0].message.content
print("\n🤖 Resposta bruta da IA:")
print(texto_resposta)

# ====================================================================
# TODO 3: CONSOLIDANDO NO PANDAS
# ====================================================================
# 1. Pegue a resposta em JSON gerada pela IA (que é uma string).
# 2. Converta ela em um dicionário Python (use a biblioteca 'json').
# 3. Transforme esse dicionário em uma linha de um DataFrame do Pandas.

import json
json_extraido = json.loads(texto_resposta)
df_resultado = pd.DataFrame([json_extraido])
print("\n📊 Dado Extraído e Estruturado:")
print(df_resultado)
