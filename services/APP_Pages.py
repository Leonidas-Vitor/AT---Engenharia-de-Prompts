import streamlit as st
import os
import yaml
import json
import pandas as pd
import matplotlib.pyplot as plt
from services import GeminiMethods as gm
from dotenv import load_dotenv
import os
import io


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
        #with columns[0]:
            #st.image(path_to_logo,width=200)
        #with columns[1]:
        st.markdown('''<h1 style='text-align: center; '><b>INSTITUTO INFNET</b></h1>''',unsafe_allow_html = True)
        st.markdown(html_p % tuple([35,"ESCOLA SUPERIOR DE TECNOLOGIA"]),unsafe_allow_html=True)
    
        st.divider()
        st.markdown(html_p % tuple([35,"AT - Engenharia de Prompts"]),unsafe_allow_html=True)
        st.markdown(html_p % tuple([25,'Aluno: Leônidas Almeida']),unsafe_allow_html = True)
        st.markdown(html_p % tuple([25,f'E-mail: <a href= mailto:{email}>{email}</a>']),unsafe_allow_html = True)
        st.markdown(html_p % tuple([25,f'GitHub Aplicação: <a href={github_link}>Link para o repositório</a>']),unsafe_allow_html = True)

    return container

#----------------------------MISC
def ShowMisc():
    container = st.container(border=True)
    with container:
        st.subheader("Miscelânea", divider=True)
        
        #with st.expander("Mostrar Miscelânea", expanded=True):
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9  = st.tabs([
            'Questão 1',
            'Questão 2',
            'Questão 3',
            'Questão 4',
            'Questão 5',
            'Questão 6',
            'Questão 7',
            'Questão 8',
            'Questão 9'])
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
        with tab6:
            ShowPromptsOverview()
        with tab7:
            ShowPromptsExpensesAndPropositions()
        with tab8:
            ShowAnswer()
        with tab9:
            ShowIAImage()

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
        #path = os.path.join(os.path.dirname(__file__),'..' ,'configs', 'data', 'config.yaml')
        with open('configs/data/config.yaml', 'r', encoding='utf-8') as arquivo:
            r = yaml.safe_load(arquivo)
        cols = st.columns(2)
        with cols[0]:
            st.write('**Resposta final:**')
            st.code('''
                    with open('configs/data/config.yaml', 'r', encoding='utf-8') as arquivo:
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
        
        st.divider()
        with st.expander('Galeria', expanded=True):
            cols = st.columns(4)
            with cols[0]:
                st.image('images/Claude_Prints/Claude_1_1.png')
                st.image('images/Claude_Prints/Claude_1_2.png')
            with cols[1]:
                st.image("images/Claude_Prints/Claude_3_1.png")
            with cols[2]:
                st.image("images/Claude_Prints/Claude_3_2.png")
            with cols[3]:
                st.image("images/Claude_Prints/Claude_3_3.png")

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
        
        st.divider()

        with st.expander('Galeria', expanded=True):
            cols = st.columns(3)            
            with cols[0]:
                st.image("images/Claude_Prints/Claude_4_1.png")
                st.image("images/Claude_Prints/Claude_4_2.png")
                st.image("images/Claude_Prints/Claude_4_3.png")
            with cols[1]:
                st.image("images/Claude_Prints/Claude_4_4.png")
                st.image("images/Claude_Prints/Claude_4_5.png")
                st.image("images/Claude_Prints/Claude_4_6.png")
            with cols[2]:
                st.image("images/Claude_Prints/Claude_5_1.png")
                st.image("images/Claude_Prints/Claude_5_2.png")
                st.image("images/Claude_Prints/Claude_5_3.png")
        
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


def ShowPromptsOverview():
    container = st.container(border=True)
    with container:
        st.subheader("Chain-of-Thought", divider=True)
        st.write('**1º PROMPT**')
        st.write('''
                 Você é um desenvolvedor python. Crie uma função que crie três tabs em 
                 streamlit, Overview, Despesas e Proposições. Se limite a apenas gerar 
                 o código comentado, não explique o código. 
                 ''')
        
        st.write('**OBJETIVO**')
        st.write('''
                 Criar a base para a aplicação de streamlit, com as abas Overview, Despesas e Proposições.
                 ''')
        
        st.divider()

        st.write('**2º PROMPT**')
        st.write('''
                 Agora na aba de Overview, adicione uma descrição sobre uma aplicação que 
                 analisa os dados públicos dos deputados, como suas despesas, proposições e 
                 filiação partidária. Inclua também um texto que se encontra em 
                 data/sumarizacao_proposicoes.json, onde temos três textos específicos que 
                 queremos exibir, um para cada um das chaves 40, 46 e 62. Dentro de cada uma 
                 dessas chaves temos dois tipos de texto, "Resumo" e "Resumo Consolidado", 
                 busque e exiba apenas o "Resumo Consolidado", destacando a qual chave 
                 (40, 46 e 62) ele pertence. Lembro que esse json é uma lista, como 
                 [{'40': {'Resumo':text}}, {'40':{'Resumo Consolidado':texto}}...] e 
                 é necessário checar se algum sub dicionário é do tipo None para evitar 
                 erros na aplicação, além de aplicar eval() nos sub dicionários para caso 
                 eles estejam sendo reconhecidos como string em vez de dict.
                 
                 Não esqueça de replicar os códigos anteriores e incluir as novas funções 
                 solicitadas. 
                 ''')
        
        st.write('**OBJETIVO**')
        st.write('''
                 Adicionar o recurso de exibir os resumos consolidados das proposições, foi necessário passar detalhes da estrutura do Json para que a LLM conseguisse 
                 identificar os resumos corretamente.
                 ''')
        
        st.divider()

        st.write('**3º PROMPT**')
        st.write('''
                 Agora inclua na Aba Overview uma imagem localizada em 
                 docs/distribuicao_deputados.png e o texto do json localizado em 
                 data/insights_distribuicao_deputados.json, que tem como chave para o 
                 texto "Analise_Claude". Coloque um título separando cada um dos elementos 
                 da aba Overview, as proposições, imagem da distribuição e texto dos insights.
                 Não esqueça de replicar o código anterior e apenas adicionar os novos recursos.
                 ''')
        
        st.write('**OBJETIVO**')
        st.write('''
                 Concluir a aba Overview incluindo a imagem e o texto dos insights sobre a distribuição dos deputados. Além de incluir um título para cada elemento da aba.
                 ''')
        
        st.divider()

        with st.expander('Galeria', expanded=True):
            cols = st.columns(4)
            with cols[0]:
                st.image("images/Gemini_Prints/Gemini_1.png")
                st.image("images/Gemini_Prints/Gemini_2_1.png")
            with cols[1]:
                st.image("images/Gemini_Prints/Gemini_2_2.png")
                st.image("images/Gemini_Prints/Gemini_2_3_a.png")
            with cols[2]:
                st.image("images/Gemini_Prints/Gemini_3_1.png")
                st.image("images/Gemini_Prints/Gemini_3_2.png")
            with cols[3]:
                st.image("images/Gemini_Prints/Gemini_3_3.png")
        
    return container

def ShowPromptsExpensesAndPropositions():
    container = st.container(border=True)
    with container:
        st.subheader("Batch-prompting", divider=True)
        st.write('**PROMPT**')
        st.write('''
                 Perfeito agora, vamos programar as abas de Despesas e Proposições.
                 - Na aba de despesas adicione o texto do json localizado em 
                 data/insights_despesas_deputados.json, onde a chave do texto é "Insights".
                 - Também na de despesas, carregue o arquivo data/serie_despesas_diárias_deputados.parquet 
                 e plot uma série temporal dessa gráfico para o deputado selecionado. Para selecionar o 
                 deputado crie um st.selectbox. No arquivo data/serie_despesas_diárias_deputados.parquet 
                 existem as colunas dataDocumento, idDeputado, tipoDespesa e valorDocumento
                 - Agora na aba de Proposições, carregue a tabela em data/proposicoes_deputados.parquet 
                 e a exiba
                 - Também na aba de Proposições carregue e mostre o resumo em data/sumarizacao_proposicoes.json, 
                 lembrando que você já carregou esse arquivo e precisamos exibir da mesma forma que na 
                 aba de Overview.
                 
                 Não se esqueça dos títulos separando cada elemento.
                 
                 Não se esqueça de replicar todo o código anterior e apenas adicionar os novos recursos, especialmente a aba de Overview. 
                 ''')
        
        st.write('**COMPARAÇÃO**')
        st.write('''
                 A técnica de Batch-prompting é mais recomendada para tarefas mais simples, onde
                 ocorre uma repetição de ações, como traduzir textos, gerar gráficos, ou realizar
                 análises simples. Enquanto que a técnica de Chain-of-Thought é melhor para tarefas
                 mais complexas, onde é necessário um raciocínio mais elaborado, como a criação desse
                 dashboard, onde é necessário criar uma aplicação interativa com diversas abas e 
                 elementos com diferentes requisitos e funcionamentos, além das diferentes fontes de 
                 dados com diferentes estruturas.
                 ''')

        st.divider()

        with st.expander('Galeria', expanded=True):
            cols = st.columns(3)
            with cols[0]:
                st.image("images/Gemini_Prints/Gemini_4_1.png")
                st.image("images/Gemini_Prints/Gemini_4_2.png")
            with cols[1]:
                st.image("images/Gemini_Prints/Gemini_4_3.png")
                st.image("images/Gemini_Prints/Gemini_4_4.png")
            with cols[2]:
                st.image("images/Gemini_Prints/Gemini_4_5.png")


def ShowAnswer():
    container = st.container(border=True)
    with container:
        st.subheader("Self-Ask", divider=True)
        st.write('**A:**')
        st.write('''
                 A técnica de Self-Ask pode ser utilizada para que o modelo avalie se a base de dados
                 vetorial FAISS forneceu os dados necessários para responder adequadamente a pergunta,
                 "fazendo" com que a LLM avalie a qualidade dos dados fornecidos e só responda se a
                 base de dados forneceu os dados necessários para responder a pergunta, evitando assim
                 alucinaçõesç.
                 ''')
        
        st.divider()

        st.write('''**B**:''')
        st.write('''
                 Devido ao limite de 200 frases por texto, a LLM não conseguiu responder as perguntas
                 1 e 2, pois não havia a totalidade das informações.

                 Já para as perguntas 3, 4 e 5 a LLM conseguiu responder com certa assertividade.
                 
                 Na pergunta 3 a LLM respondeu como maior gasto a \"Manutenção de Escritório de Apoio\",
                 que não está totalmente incorreto, pois é o segundo maior gasto, o que indica que os textos fornecidos
                 não foram suficientes.

                 Na pergunta 4 a LLM a resposta contém informações corretas, mas não é a resposta ideal, pois
                 há repetições de informações e a resposta não é clara.

                 Na pergunta 5 a LLM respondeu corretamente.
                 ''')
        
        st.divider()

        with st.expander('Galeria', expanded=True):
            cols = st.columns(3)
            with cols[0]:
                st.image("images/Dashboard_Prints/D_1.png")
                st.image("images/Dashboard_Prints/D_2.png")
            with cols[1]:
                st.image("images/Dashboard_Prints/D_3.png")
                st.image("images/Dashboard_Prints/D_4.png")
            with cols[2]:
                st.image("images/Dashboard_Prints/D_5.png")


def ShowIAImage():
    container = st.container(border=True)
    with container:
        st.subheader("Geração de Imagens com Prompts", divider=True)
        st.write('**CÓDIGO**')
        st.code('''
from diffusers import StableDiffusionPipeline
import torch

def generate_image(prompt, output_path="generated_image.png"):
    pipeline = StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        torch_dtype=torch.float16,
        revision="fp16" 
    )
                
    pipeline = pipeline.to("cuda"))
    image = pipeline(prompt).images[0]

    image.save(output_path)
    print(f"Imagem salva em: {output_path}")
                ''')
        cols = st.columns(2)
        with cols[0]:
            st.write('**1º PROMPT**: A rich caramel mutt with monocle')
            st.image("images/IA_Images/caramelo_rico.png")
        with cols[1]:
            st.write('**2º PROMPT**: Dog breed Cocker spaniel astronaut')
            st.image("images/IA_Images/cocker_atronauta.png")

        st.divider()

        st.write('**A:**')
        st.write('''
                 - Stable Diffusion: Baseado em redes neuras difusionais, que adiciona gradualmente ruído
                 a uma imagem e gerar imagens a partir do ruído. Tem como vantagem ser Open Source e 
                 poder ser utilizado localmente com hardware acessível. Suas principais limitações são
                 a dependencia da qualidade do prompt e os artefatos/falta de coerência nas imagens geradas.

                 - DALL-E: Baseado em transformers e combina modelos de linguagem (como o GPT), utilizando CLIP (Constrative Language-Image Pre-training) 
                 para conectar texto e imagem, melhorando a compreenmsão do modelo, sendo uma das suas principais vantagens.
                 Outras vantagens estão na facilidade de uso e a consistência na composição. Suas principais limitações são a dependência da Nuvem,
                 os filtros de conteúdo e a falta de personalização, consequências de ser um modelo proprietário.

                 - MidJourney provavelmente uma combinação de modelos de difusão e aprendizado profundo, com foco em geração de imagens estilizadas 
                 e artísticas. Suas principais vantagens são a geração de imagens únicas e estilizadas, com um toque artístico e a comunidade ativa.
                 Suas principais limitações são a dependência da Nuvem, o licenciamento restrito e a falta de personalização, consequências de ser um 
                 modelo proprietário.
                 ''')
        
        st.divider()

        st.write('**B:**')
        cols = st.columns(2)
        with cols[0]:
            st.write('''**1º PROMPT**: A rich caramel mutt with monocle, Baroque-style painting, textured brushstrokes, 
                     dramatic chiaroscuro lighting, earthy tones''')
            st.image("images/IA_Images/caramelo_rico_v2.png")

            st.write('''**2º PROMPT**:A rich caramel mutt with monocle, Baroque-style painting, textured brushstrokes, dramatic chiaroscuro lighting, earthy tones, 
perfect symmetry, centered perspective, mystical style''')
            st.image("images/IA_Images/caramelo_rico_v3.png")
            
            st.write('''**3º PROMPT**: A rich caramel mutt with monocle, Baroque-style painting, textured brushstrokes, dramatic chiaroscuro lighting, 
earthy tones, blurred background, cinematic style, soft lighting''')
            st.image("images/IA_Images/caramelo_rico_v4.png")

        with cols[1]:
            st.write('''**1º PROMPT**: Dog breed Cocker spaniel astronaut, high-quality digital 
                     illustration, sharp lines, vibrant colors, cyberpunk style.''')
            st.image("images/IA_Images/cocker_atronauta_v2.png")

            st.write('''**2º PROMPT**: Dog breed Cocker spaniel astronaut, high-quality digital illustration, sharp lines, vibrant colors, cyberpunk style, 
  no old-fashioned elements, no vegetation, no pastel colors, no inconsistent lighting.''')
            st.image("images/IA_Images/cocker_atronauta_v3.png")

            st.write('''**3º PROMPT**: Dog breed Cocker spaniel astronaut, high-quality digital illustration, sharp lines, vibrant colors, cyberpunk style, 
  no face distortions, no deformed hands, no irrelevant background objects, no overly saturated colors.''')
            st.image("images/IA_Images/cocker_atronauta_v4.png")

        st.divider()
        st.write('**AVALIAÇÃO**')
        st.write('''
                 A inclusão de estilo visual e composição melhoraram substancialmente as imagens, principalmente
                 o estilo visual, que geraram o melhor resultado (primeiros prompts), a inclusão de composição e 
                 prompts negativos (quatro últimos prompts) geraram resultados, como adicionar um juba no vira-lata caramelo
                 na tentativa de trazer um ar mais místico para imagem, por exemplo, contudo, ainda é possível ver distorções
                 e falhas aparentes nas imagens geradas. 
                    ''')


#---------------------------APLICAÇÃO

import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

def carregar_dados_sumarizacao(arquivo):
    """Carrega os dados do arquivo JSON e retorna uma lista de dicionários.

    Args:
        arquivo (str): Nome do arquivo JSON.

    Returns:
        list: Lista de dicionários com os dados da sumarização.
    """

    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    return dados

def exibir_sumarizacao_proposicoes(dados):
    """Exibe o resumo consolidado das proposições para as chaves 40, 46 e 62.

    Args:
        dados (list): Lista de dicionários com os dados da sumarização.
    """

    for dado in dados:
        for chave, valor in dado.items():
            if chave in ['40', '46', '62']:
                if valor is not None and 'Resumo Consolidado' in valor:
                    valor = eval(str(valor))  # Converte para dicionário se necessário
                    st.write(f"**Chave {chave}:**\n{valor['Resumo Consolidado']}")

def carregar_insights_distribuicao(arquivo):
    """Carrega os insights sobre a distribuição de deputados.

    Args:
        arquivo (str): Nome do arquivo JSON.

    Returns:
        str: Texto dos insights.
    """

    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    return dados['Analise_Claude']

def carregar_insights_despesas(arquivo):
    """Carrega os insights sobre as despesas dos deputados.

    Args:
        arquivo (str): Nome do arquivo JSON.

    Returns:
        str: Texto dos insights.
    """

    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    return dados['Insights']

def criar_tabs():
    """
    Cria três tabs no Streamlit: Overview, Despesas e Proposições.

    Returns:
        None
    """

    tab1, tab2, tab3 = st.tabs(["Overview", "Despesas", "Proposições"])

    with tab1:
        st.title("Visão Geral")

        # Proposições
        st.header("Análise das Proposições")
        dados_sumarizacao = carregar_dados_sumarizacao('data/sumarizacao_proposicoes.json')
        exibir_sumarizacao_proposicoes(dados_sumarizacao)

        # Imagem da Distribuição
        st.header("Distribuição dos Deputados")
        image = plt.imread("docs/distribuicao_deputados.png")
        st.image(image, caption="Distribuição dos Deputados por Partido")

        # Insights sobre a Distribuição
        st.header("Insights sobre a Distribuição")
        insights = carregar_insights_distribuicao('data/insights_distribuicao_deputados.json')
        st.write(insights)

    with tab2:
        st.title("Despesas")

        # Insights sobre as Despesas
        insights_despesas = carregar_insights_despesas('data/insights_despesas_deputados.json')
        st.write(insights_despesas)

        # Gráfico de Série Temporal das Despesas
        df_despesas = pd.read_parquet('data/serie_despesas_diárias_deputados.parquet')
        deputados = df_despesas['idDeputado'].unique()
        deputado_selecionado = st.selectbox('Selecione um Deputado:', deputados)

        df_deputado = df_despesas[df_despesas['idDeputado'] == deputado_selecionado]
        plt.figure(figsize=(20, 5))
        plt.plot(df_deputado['dataDocumento'], df_deputado['valorDocumento'])
        plt.xlabel('Data')
        plt.ylabel('Valor da Despesa')
        plt.title(f'Série Temporal das Despesas do Deputado {deputado_selecionado}')
        st.pyplot(plt)

    with tab3:
        st.title("Proposições")

        # Tabela de Proposições
        df_proposicoes = pd.read_parquet('data/proposicoes_deputados.parquet')
        st.dataframe(df_proposicoes, use_container_width=True)

        # Resumo das Proposições
        st.header("Resumo das Proposições")
        dados_sumarizacao = carregar_dados_sumarizacao('data/sumarizacao_proposicoes.json')
        exibir_sumarizacao_proposicoes(dados_sumarizacao)

        if os.getenv("GEMINI_KEY")  != '':
            #Pedir um arquivo .env com as credenciais do Gemini
            st.write('**CREDENCIAIS GEMINI**')
            env = st.file_uploader('Insira o arquivo .env com as credenciais do Gemini, chave GEMINI_KEY', type='env')
            if env:
                st.write('Arquivo .env carregado com sucesso!')
                with open("temp.env", "wb") as f:
                    f.write(env.getbuffer())
                
                # Carregar as variáveis de ambiente do arquivo temporário
                load_dotenv("temp.env")
                
                # Remover o arquivo temporário após carregar as variáveis
                os.remove("temp.env")

                ShowChatWithGemini(os.getenv("GEMINI_KEY"))
        else:
            ShowChatWithGemini(os.getenv("GEMINI_KEY"))
        


max_msg_key = 'max'
hist_key = 'hist'

def WriteHistory(messages):

    if max_msg_key not in st.session_state:
        st.session_state[max_msg_key] = 0
    if hist_key not in st.session_state:
        st.session_state[hist_key] = []
    try:
        for history in st.session_state[hist_key]:
            role = 'Usuário' if 'Usuário' in history else 'Assistente'
            icon = 'user' if 'Usuário' in history else 'assistant'
            messages.chat_message(icon).write(history[role])
    except:
        st.error('Erro ao escrever histórico')
        pass



def ShowChatWithGemini(api_key):
    cols = st.columns([0.8,0.2])
    geminiConfigs = gm.GetGeminiConfig('CHAT_CONFIG')
    embedding_model = gm.load_embedding_model()
    faiss = gm.load_faiss()
    texts = gm.load_texts()
    k = 200
    with cols[0]:
        messages = st.container(height=700)
        WriteHistory(messages)
        if st.session_state[max_msg_key] < 5:
            if prompt := st.chat_input("Converse com o especialista python"):
                st.session_state[hist_key].append({'Usuário':prompt})
                messages.chat_message("user").write(prompt)

                prompt_embedding = gm.vetorize_text(prompt, embedding_model)
                distances, indices = faiss.search(prompt_embedding, k)

                db_text = '\n'.join([f"- {texts[indices[0][i]]}" for i in range(k)])

                response = gm.GetGeminiResponse({
                    'model':geminiConfigs['model'], 
                    'generation_config': geminiConfigs['generation_config'],
                    'safety_settings' : geminiConfigs['safety_settings'],
                    'system_instruction':geminiConfigs['system_instruction'].format(db_texts=db_text)},
                    json.dumps(st.session_state[hist_key], ensure_ascii=False, indent=4),
                    api_key)
                
                messages.chat_message("assistant").write(f"Echo: {response.text}")

                st.session_state[hist_key].append({'Assistente':response.text})
                st.session_state[max_msg_key] += 1
        else:
            st.write('Limite atingido, reinicia o chat para continuar')


    with cols[1]:
        st.write('Esse chat tem o limite de 5 interações, ao atingir o limite, reinicie o chat para continuar')
        st.write(f'Interações: {st.session_state[max_msg_key]}/5')
        if st.button('Reiniciar', key='reiniciar_10'):
            st.session_state[max_msg_key] = 0
            st.session_state[hist_key].clear()
            st.rerun()
        if st.session_state[max_msg_key] == 5:
            st.warning('Limite atingido, reinicia o chat para continuar')
