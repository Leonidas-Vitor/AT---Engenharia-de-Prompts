import pandas as pd
from services import GeminiMethods as gm

def get_resume(text_to_resume : pd.DataFrame):
    systemInstruction_A = '''
    Sua tarefa é resumir as proposições dos deputados apartir dos textos das ementas.

    A resposta deve ser no formato Json conforme o exemplo: 
    {"Resumo": <Resumo> }
    A resposta deve estar pronta para ser convertida em formato json sem erros ou processos adicionais.
    '''

    systemInstruction_B = '''
    Sua tarefa é juntar um conjunto de resumos e gerar um resumo final, destacando os pontos mais relevantes
    e significativos.

    A resposta deve ser no formato Json e a resposta deve estar pronta para ser convertida em formato json sem erros ou processos adicionais.
    '''

    chunks = []
    step = 100
    overlap = 25

    #Criar lista de palavras
    words = text_to_resume.split()
    print(f'Quantidade de palavras: {len(words)}')

    for i in range(0, len(words), step-overlap):
        chunk = words[i:i+step]
        chunks.append(chunk)

    return gm.GetGeminiChunkAbstract(chunks, systemInstruction_A, systemInstruction_B)