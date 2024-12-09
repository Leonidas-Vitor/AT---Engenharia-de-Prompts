import streamlit as st
import os
import yaml
import json
import pandas as pd

#-----------------------------------------UTILIDADES
@st.cache_data
def LoadConfigs():
    with open('configs/config.json', 'r') as arquivo:
        st.session_state['config'] = json.loads(arquivo.read())

    with open('configs/gemini_config.yaml', 'r') as arquivo:
            st.session_state['gemini_config'] = yaml.safe_load(arquivo)

#-----------------------------------------PÁGINAS & ABAS
def ShowIntro():
    container = st.container(border=True)

    path_to_logo = "images/Infnet_logo.png"#s.path.join(os.path.dirname(__file__), '..', 'images', 'Infnet_logo.png')
    html_p = """<p style='text-align: center; font-size:%spx;'><b>%s</b></p>"""
    github_link = '''https://github.com/Leonidas-Vitor/AT---Engenharia-de-Prompts'''
    email = '''leonidas.almeida@al.infnet.edu.br'''
    
    with container:
        columns = st.columns([0.3,0.7])
        with columns[0]:
            st.image(path_to_logo,width=200)
        with columns[1]:
            st.markdown('''<h1 style='text-align: center; '><b>INSTITUTO INFNET</b></h1>''',unsafe_allow_html = True)
            st.markdown(html_p % tuple([35,"ESCOLA SUPERIOR DE TECNOLOGIA"]),unsafe_allow_html=True)
        
        st.divider()
        st.markdown(html_p % tuple([35,"AT - Engenharia de Prompts"]),unsafe_allow_html=True)
        st.markdown(html_p % tuple([25,'Aluno: Leônidas Almeida']),unsafe_allow_html = True)
        st.markdown(html_p % tuple([25,f'E-mail: <a href= mailto:{email}>{email}</a>']),unsafe_allow_html = True)
        st.markdown(html_p % tuple([25,f'GitHub Aplicação: <a href={github_link}>Link para o repositório</a>']),unsafe_allow_html = True)

        st.divider()

        st.markdown('**Instruções:**')
        st.markdown('O trabalho está dividido em 3 partes: **Introdução**, **Miscelânea** e **Aplicação**.')
        st.markdown('Na **Introdução** você encontrará informações sobre o trabalho e o autor.')
        st.markdown('Na **Miscelânea** você encontrará informações sobre a arquitetura da aplicação, criação de textos com LLM, processamento dos dados de deputados, despesas e proposições.')
        st.markdown('Na **Aplicação** você encontrará as abas interativas com aplicação de LLM')

    return container

def ShowMisc():
    container = st.container(border=True)
    with container:
        st.subheader("Miscelânea", divider=True)
        
        with st.expander("Mostrar Miscelânea", expanded=True):
            tab1, tab2, tab3, tab4, tab5  = st.tabs([
                'Arquitetura da aplicação',
                'Criação de textos com LLM',
                'Processamento dos dados de deputados',
                'Processamento dos dados de despesas',
                'Processamento dos dados de proposições'])
            with tab1:
                st.write("Arquitetura da aplicação")
            with tab2:
                ShowCreateTextsWithLLM()
            with tab3:
                ShowProcessDeputies()
            with tab4:
                ShowProcessExpenses()
            with tab5:
                ShowPropositions()

    return container

def ShowArchitecture():
    pass

def ShowCreateTextsWithLLM():
    container = st.container(border=True)
    with container:
        st.subheader("Criação de textos com LLM", divider=True)
        st.write("**PROMPT:**")
        st.write('*Faça um texto curto, de até 2 parágrafos, explicando a Câmara dos Deputados do Brasil.*')
        cols = st.columns(3)
        with cols[0]:
            st.write("Modelo: GPT-4o")
            st.image("images/Misc/GPT.png", use_container_width=True)
        with cols[1]:
            st.write("Modelo: Claude-3.5-Haiku")
            st.image("images/Misc/Claude.png", use_container_width=True)
        with cols[2]:
            st.write("Modelo: Gemini-1.5-Pro")
            st.image("images/Misc/Gemini.png", use_container_width=True)

        st.write("**Diferenças.:**")
        st.write('''
                 O GPT trouxe a resposta com mais detalhes quantitativas, como o número mínimo e máximo de deputados por estado,
                 enquanto o Claude trouxe uma resposta mais direta e objetiva, ao custo de menos detalhes e o 
                 Gemini trouxe uma resposta mais extensa e com mais detalhes sobre as funções da Câmara dos Deputados.''')
        st.write("**Escolha final.:**")
        st.write('''
                 Todas as LLMs testadas trouxeram respostas satisfatórias, contudo,
                 o Claude-3.5-Haiku foi o modelo que trouxe a resposta mais objetiva e direta,
                 sem perder a qualidade e a quantidade de informações.
                 ''')
        
        st.divider()
        
        st.write("**PROMPT:**")
        st.write('''
                 *Faça um texto curto, de até 2 parágrafos, explicando a Câmara dos Deputados do Brasil. Gere um arquivo config.yaml 
                 com a resposta usando como chave 'overview_summary'*
                 ''')
        
        with open('configs/data/config.yaml ', 'r', encoding='utf-8') as arquivo:
            r = yaml.safe_load(arquivo)
        cols = st.columns(2)
        with cols[0]:
            st.write('**Resposta final:**')
            st.code('''
                    with open('configs/data/config.yaml ', 'r', encoding='utf-8') as arquivo:
                        r = yaml.safe_load(arquivo)
                    ''')
            st.write(r['overview_summary'])
        with cols[1]:
            st.image("images/Misc/Claude_Resposta.png")
            
    return container


def ShowProcessDeputies():
    container = st.container(border=True)
    with container:
        st.subheader("Processamento dos dados de deputados", divider=True)
        st.write('**PROMPT**')
        st.write('''
                 Crie um código python que leia um arquivo em data/deputados.parquet e crie um gráfico de 
                 pizza usando matplotlib mostrando o total e o percentual de deputados de cada partido, 
                 adicione uma linha de código para salvar o gráfico em docs/distribuicao_deputados.png. 
                 O deputados.parquet possui as seguintes colunas: id, uri, nome, siglaPartido, uriPartido, 
                 siglaUf, idLegislatura, urlFoto, email
                 ''')
        st.write('**CÓDIGO GERADO:**')
        st.code('''
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
                ''')
        st.image("docs/distribuicao_deputados.png")

        st.divider()

        st.write('**PROMPT**')
        st.write('''
                 Você é um analista político, faça uma análise sobre a distribuição dos partidos na câmara 
                 dos deputados e como ela influência a política nacional. Os dados sobre a distribuição 
                 estão disponíveis em anexo no arquivo deputados_por_partido.json.
                ''')
        
        st.write('**ELEMENTOS DE PROMPT**')
        st.write('''
                 1. Definição de persona: Analista político, define a forma como a LLM irá realizar a análise
                 2. Objetivo/Direcionamento: Especificar o tipo da análise, no caso, focada na distribuição partidária na Câmara.
                 3. Disponibilizar Dados: Arquivo deputados_por_partido.json, fornecendo informações sobre a distribuição partidária.
                 4. Objetivo/Direcionamento: Especificar que o foco/contexto da análise é na visão de como a distribuição afeta a política no país.
                 ''')
        st.divider()
        st.write('**ANÁLISE:**')
        st.write('''
Com base nos dados fornecidos no arquivo deputados_por_partido.json, realizarei uma análise detalhada da composição partidária na Câmara dos Deputados.

Distribuição Partidária:

Blocos Principais:
1. Partidos Majoritários (acima de 50 deputados):
- PL (93 deputados): Principal força política
- PT (68 deputados): Segundo maior partido
- UNIÃO (60 deputados): Terceiro maior bloco
- PP (52 deputados): Importante base parlamentar

2. Partidos Médios (20-50 deputados):
- PSD (45 deputados)
- REPUBLICANOS (44 deputados)
- MDB (44 deputados)

3. Partidos Menores (10-20 deputados):
- PDT (19 deputados)
- PODE (15 deputados)
- PSB (14 deputados)
- PSOL (13 deputados)
- PSDB (12 deputados)

Análise Política:

1. Fragmentação Partidária
- O cenário demonstra alta fragmentação partidária
- Nenhum partido possui maioria absoluta (necessário 257 deputados)
- Formação de blocos e alianças será fundamental para governabilidade

2. Campo Ideológico
- Direita (PL, PP, REPUBLICANOS): Cerca de 189 deputados
- Centro (MDB, UNIÃO): Aproximadamente 104 deputados
- Esquerda (PT, PSOL, PCdoB): Cerca de 88 deputados

3. Estratégias Políticas
- Necessidade de negociações e acordos entre partidos
- Centrão (MDB, PP, UNIÃO) terá papel crucial nas deliberações
- Poder de articulação será mais importante que tamanho bancada individual

Conclusão:
A composição atual exigirá habilidade política para construir maiorias e aprovar projetos, evidenciando a complexidade do sistema político brasileiro.
''')
        st.divider()
        st.write('**AVALIAÇÃO DA RESPOSTA**')
        st.write('''
                A análise realizada foi satisfatório, especilamente considerando que havia apenas dados sobre 
                a distribuição partidária. Carecendo de maiores detalhes e contextos contemporâneos, contudo,
                a LLM foi capaz de entregar uma visão macro sobre a composição partidária na Câmara dos 
                Deputados e como ela influência a política nacional.
                ''')

    return container

def ShowProcessExpenses():
    container = st.container(border=True)
    with container:
        st.subheader("Processamento dos dados de despesas", divider=True)
        st.write('**1º PROMPT**')
        st.write('''
                 Você é um programador python que está fazendo uma análise sobre despesas de deputados. 
                 O arquivo se encontra no caminho data/serie_despesas_diárias_deputados.parquet e contém 
                 as colunas dataDocumento, idDeputado, tipoDespesa e valorDocumento. Faça um gráfico em python 
                 com a distribuição dos gastos por tipo de despesa e imprima a tabela de dados utilizada para 
                 gerar o gráfico.
                 ''')
        st.write('**1º CÓDIGO GERADO:**')
        st.code('''
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
print(gastos_por_tipo)
''')
        

        
        st.write('**1º GRÁFICO GERADO:**')
        st.image("images/Misc/Generated Knowledge/gastos_por_tipo_de_despesa.png")

        st.divider()

        st.write('**2º PROMPT**')
        st.write('''
                 Agora faça um gráfico porcentagem das despesas totais por deputado e imprima a 
                 tabela de dados utilizada para gerar o gráfico. Exiba apenas o top 10 deputados 
                 que mais gastaram, os demais coloque em um grupo de outros.
                 ''')
        st.write('**2º CÓDIGO GERADO:**')
        st.code('''
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
print(porcentagens)''')
        
        st.write('**2º GRÁFICO GERADO:**')
        st.image("images/Misc/Generated Knowledge/gastos_por_deputado.png")

        st.divider()

        st.write('**3º PROMPT**')
        st.write('''Agora faça um gráfico com a distribuição do tipo de despesa para os deputados 
                 que mais gastaram, não esqueça de imprimir os dados utilizados para gerar o 
                 gráfico.''')
        
        st.write('**3º CÓDIGO GERADO:**')
        st.code('''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o arquivo Parquet
df = pd.read_parquet('data/serie_despesas_diárias_deputados.parquet')

# Identificar os 5 deputados que mais gastaram
top_5_deputados = df.groupby('idDeputado')['valorDocumento'].sum().nlargest(5).index

# Filtrar o dataframe para esses deputados
df_top_5 = df[df['idDeputado'].isin(top_5_deputados)]

# Agregar gastos por deputado e tipo de despesa
gastos_por_deputado_tipo = df_top_5.groupby(['idDeputado', 'tipoDespesa'])['valorDocumento'].sum().reset_index()

# Criar o gráfico de barras empilhadas
plt.figure(figsize=(15, 8))
grafico = sns.barplot(x='idDeputado', y='valorDocumento', hue='tipoDespesa', 
                      data=gastos_por_deputado_tipo)

plt.title('Distribuição de Tipos de Despesa para os 5 Deputados que Mais Gastaram', fontsize=15)
plt.xlabel('ID do Deputado', fontsize=12)
plt.ylabel('Valor Total de Despesas (R$)', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Tipo de Despesa', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Mostrar o gráfico
plt.show()

# Imprimir a tabela de dados
print("Tabela de Gastos por Deputado e Tipo de Despesa:")
tabela_gastos = gastos_por_deputado_tipo.pivot(index='idDeputado', 
                                               columns='tipoDespesa', 
                                               values='valorDocumento').fillna(0)
print(tabela_gastos)

# Calcular porcentagens por deputado
print("\nPorcentagem de Gastos por Tipo de Despesa:")
tabela_porcentagens = tabela_gastos.apply(lambda x: x / x.sum() * 100, axis=1).round(2)
print(tabela_porcentagens)''')
        
        st.write('**3º GRÁFICO GERADO:**')
        st.image("images/Misc/Generated Knowledge/gastos_por_deputado_tipo.png")

        st.divider()

        st.write('**INSIGHT PROMPT**')
        st.write('''
                 Você é um analista de político e está analisando os dados sobre gastos dos 
                 deputados, você tem acesso a distribuição dos gastos por tipo, aos gastos por 
                 deputado, e aos gastos dos deputados por tipo (apenas o top 10 mais gastadores), 
                 que estão em anexo no formato json.  Considerando que os maiores gastos estão 
                 relacionados a divulgação da atividade parlamentar e Manutenção de escritório de 
                 apoio a atividade parlamentar, como você análise essa distribuição de gastos e o 
                 que ela diz a respeito do sistema político brasileiro?
                 ''')
        
        st.write('**INSISHTS GERADOS:**')
        st.write('''
Após analisar detalhadamente os dados fornecidos, posso fazer algumas observações importantes sobre os gastos dos deputados:

1. Categorias de Maior Impacto Financeiro:
- Divulgação da Atividade Parlamentar: R$ 3.704.636,72
- Manutenção de Escritório de Apoio à Atividade Parlamentar: R$ 2.666.458,60

Estas duas categorias representam juntas aproximadamente 6,3 milhões de reais, o que é bastante significativo.

2. Análise Crítica:
A concentração de gastos em "divulgação" e "manutenção de escritório" sugere alguns pontos importantes sobre o sistema político brasileiro:

a) Transparência Questionável
- A alta quantia em "divulgação" pode indicar um uso estratégico de recursos públicos para autopromoção, em vez de efetivo trabalho legislativo.
- Pode representar uma tentativa de construção de imagem política com recurso público.

b) Estrutura Administrativa Complexa
- Os altos custos de manutenção de escritório sugerem uma estrutura administrativa pesada e potencialmente ineficiente.
- Indica que os deputados necessitam de significativa infraestrutura de apoio para exercer suas funções.

c) Possível Uso Político dos Recursos
- A categoria "divulgação" pode mascarar gastos de campanha ou marketing pessoal.
- Representa uma zona cinzenta entre o trabalho parlamentar legítimo e autopromoção.

3. Gastos Individuais
- Os deputados 220593 e 204560 aparecem entre os maiores gastadores.
- Variações significativas nos gastos entre deputados sugerem diferentes estratégias de uso de recursos públicos.

Conclusão:
Esses dados revelam um sistema que permite considerável discricionariedade no uso de recursos públicos, com potencial para má utilização e falta de transparência. A estrutura atual parece privilegiar a visibilidade política sobre a efetiva representação.

Esta análise destaca a necessidade de:
- Maior regulação dos gastos parlamentares
- Critérios mais rígidos de prestação de contas
- Transparência nos gastos de divulgação
- Revisão dos custos administrativos
''')

    return container


def ShowPropositions():
    with open('data/sumarizacao_proposicoes.json') as f:
        data = json.load(f)

    tema_40 = {'Chunks': []}
    tema_46 = {'Chunks': []}
    tema_62 = {'Chunks': []}

    for line in data:
        if line['40'] is not None:
            try:
                tema_40['Chunks'].append(eval(line['40'])['Resumo'])
            except:
                tema_40['Resumo'] = eval(line['40'])['Resumo Consolidado']

        if line['46'] is not None:
            try:
                tema_46['Chunks'].append(eval(line['46'])['Resumo'])
            except:
                tema_46['Resumo'] = eval(line['46'])['Resumo Consolidado']

        if line['62'] is not None:
            try:
                tema_62['Chunks'].append(eval(line['62'])['Resumo'])
            except:
                tema_62['Resumo'] = eval(line['62'])['Resumo Consolidado']

    df_proposicoes = pd.read_parquet('data/proposicoes_deputados.parquet')

    container = st.container(border=True)

    with container:
        st.subheader("Proposições", divider=True)
        tab1, tab2, tab3 = st.tabs(['Tema 40', 'Tema 46', 'Tema 62'])
        with tab1:
            st.write('**RESUMO CONSOLIDADO**')
            st.write(tema_40['Resumo'])
            st.divider()
            st.write('**AVALIAÇÃO**')
            st.write('O resumo está coerente com as proposições apresentadas.')
            st.divider()
            st.write("**RESUMO POR CHUNK**")
            for chunk in tema_40['Chunks']:
                st.write(chunk)
            st.divider()
            st.write("**PROPOSICOES**")
            st.dataframe(df_proposicoes[df_proposicoes['codTema'] == 40]['ementa'], use_container_width=True)
        with tab2:
            st.write('**RESUMO CONSOLIDADO**')
            st.write(tema_46['Resumo'])
            st.divider()
            st.write('**AVALIAÇÃO**')
            st.write('O resumo está coerente com as proposições apresentadas.')
            st.divider()
            st.write("**RESUMO POR CHUNK**")
            for chunk in tema_46['Chunks']:
                st.write(chunk)
            st.divider()
            st.write("**PROPOSICOES**")
            st.dataframe(df_proposicoes[df_proposicoes['codTema'] == 46]['ementa'], use_container_width=True)
        with tab3:
            st.write('**RESUMO CONSOLIDADO**')
            st.write(tema_62['Resumo'])
            st.divider()
            st.write('**AVALIAÇÃO**')
            st.write('O resumo está coerente com as proposições apresentadas.')
            st.divider()
            st.write("**RESUMO POR CHUNK**")
            for chunk in tema_62['Chunks']:
                st.write(chunk)
            st.divider()
            st.write("**PROPOSICOES**")
            st.dataframe(df_proposicoes[df_proposicoes['codTema'] == 62]['ementa'], use_container_width=True)

