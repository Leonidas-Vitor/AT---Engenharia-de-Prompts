import requests
import plotly.express as px
import pandas as pd
from services import ChunkSummarize as cs, GeminiMethods as gm
import json
import time

base_url = 'https://dadosabertos.camara.leg.br/api/v2/'
dataInicio = '2024-08-01'
dataFim = '2024-08-30'

def get_deputados():
    url = base_url + 'deputados'
    response = requests.get(url,params={'ordem':'ASC','ordenarPor':'nome', 
                                        'dataInicio':dataInicio, 'dataFim':dataFim})
    
    df_deputados = pd.DataFrame(response.json()['dados'])
    df_deputados.to_parquet('data/deputados.parquet')

def get_pie_chart():
    code = '''
import pandas as pd
import matplotlib.pyplot as plt

# Lê o arquivo Parquet
df = pd.read_parquet('data/deputados.parquet')

# Conta o número de deputados por partido
contagem_partidos = df['siglaPartido'].value_counts()

# Cria o gráfico de pizza
plt.figure(figsize=(12, 8))
plt.pie(contagem_partidos.values, 
        labels=[f'{partido} ({count})' for partido, count in contagem_partidos.items()],
        autopct='%1.1f%%')
plt.title('Distribuição de Deputados por Partido')
plt.axis('equal')  # Garante que o gráfico seja um círculo perfeito

# Salva o gráfico
plt.savefig('docs/distribuicao_deputados.png', bbox_inches='tight')
plt.close()
        '''
    try:
        exec(code)
        return True
    except Exception as e:
        print(e)
        return False

def get_expenses():
    deputados = pd.read_parquet('data/deputados.parquet')
    deputados_ids = deputados['id']
    df_expenses = pd.DataFrame()
    for id in deputados_ids:
        url = base_url + f'deputados/{id}/despesas'
        response = requests.get(url, params={'ano': 2024,'mes': 8})
        df_expenses = pd.concat([df_expenses, pd.DataFrame(response.json()['dados'])])

    df_expenses['idDeputado'] = deputados['id']

    #Converter dataDocumento para date
    df_expenses['dataDocumento'] = pd.to_datetime(df_expenses['dataDocumento']).dt.date

    df_expenses = df_expenses[['dataDocumento','idDeputado', 'tipoDespesa', 'valorDocumento']]

    #Agrupar despesas por dia, deputado e tipo de despesa
    df_expenses = df_expenses.groupby(['dataDocumento','idDeputado','tipoDespesa']).sum('valorDocumento').reset_index()
    df_expenses.to_parquet('data/serie_despesas_diárias_deputados.parquet')

def get_expenses_by_type():
    code = '''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o arquivo Parquet
df = pd.read_parquet('data/serie_despesas_diárias_deputados.parquet')

# Agregar os gastos por tipo de despesa
gastos_por_tipo = df.groupby('tipoDespesa')['valorDocumento'].sum().sort_values(ascending=False)

# Configurar o estilo do gráfico
plt.figure(figsize=(12, 6))
sns.set(style="whitegrid")

# Criar o gráfico de barras
plt.bar(gastos_por_tipo.index, gastos_por_tipo.values)
plt.title('Distribuição de Gastos por Tipo de Despesa', fontsize=15)
plt.xlabel('Tipo de Despesa', fontsize=12)
plt.ylabel('Valor Total (R$)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Mostrar o gráfico
plt.show()

# Imprimir a tabela de dados
print("Tabela de Gastos por Tipo de Despesa:")
print(gastos_por_tipo)'''

    try:
        exec(code)
        return True
    except Exception as e:
        print(e)
        return False

def get_expenses_by_dep():
    code = '''
import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo Parquet
df = pd.read_parquet('data/serie_despesas_diárias_deputados.parquet')

# Calcular o total de gastos por deputado
gastos_por_deputado = df.groupby('idDeputado')['valorDocumento'].sum().sort_values(ascending=False)

# Selecionar top 10 deputados e agrupar o restante
top_10_deputados = gastos_por_deputado.head(10)
outros_deputados = pd.Series({'Outros': gastos_por_deputado[10:].sum()})
gastos_final = pd.concat([top_10_deputados, outros_deputados])

# Calcular porcentagens
total_gastos = gastos_final.sum()
porcentagens = (gastos_final / total_gastos * 100).round(2)

# Criar gráfico de pizza
plt.figure(figsize=(12, 8))
plt.pie(porcentagens, labels=[f'{dep}: {perc}%' for dep, perc in porcentagens.items()], 
        autopct='%1.1f%%', startangle=90)
plt.title('Distribuição de Gastos por Deputado (Top 10)', fontsize=15)
plt.axis('equal')
plt.tight_layout()

# Mostrar o gráfico
plt.show()

# Imprimir a tabela de dados
print("Tabela de Gastos por Deputado:")
print(porcentagens)'''

    try:
        exec(code)
        return True
    except Exception as e:
        print(e)
        return False

def get_proposicoes():
    url = base_url + 'proposicoes'
    df_proposicoes = pd.DataFrame()
    for codTema in [40, 46, 62]:
        response = requests.get(url, params={'dataInicio':dataInicio, 'dataFim':dataFim, 
                                            'codTema': codTema, 
                                            'ordem':'ASC', 'ordenarPor':'id'})
        
        df_tema = pd.DataFrame(response.json()['dados'])
        df_tema['codTema'] = codTema
        df_proposicoes = pd.concat([df_proposicoes, df_tema])

        #Selecionar as 10 maiores ementas por codTema
    df_proposicoes = df_proposicoes.groupby('codTema').apply(lambda x: x.nlargest(10, 'id')).reset_index(drop=True)

    df_proposicoes.to_parquet('data/proposicoes_deputados.parquet')
    return True

def get_resumo_proposicoes():
    df_proposicoes = pd.read_parquet('data/proposicoes_deputados.parquet')

    resumos = {}
    for codTema in df_proposicoes['codTema'].unique():
        df_tema = df_proposicoes[df_proposicoes['codTema'] == codTema]
        proposicoes_tema = ' '.join(df_tema['ementa'])
        resumo = json.loads(cs.get_resume(proposicoes_tema))
        resumos[codTema] = resumo
        print(f'CodTema: {codTema} - Resumo: {resumo}')
        print('Aguardando 20 segundos para não exceder a cota de chamadas da API...')
        time.sleep(20)

    df_resumos = pd.DataFrame(resumos)
    df_resumos.to_json('data/sumarizacao_proposicoes.json', orient='records')
