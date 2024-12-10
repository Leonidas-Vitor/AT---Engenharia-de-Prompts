import google.generativeai as genai
import streamlit as st
import json
import yaml
import faiss
from sentence_transformers import SentenceTransformer

@st.cache_data
def GetGeminiModel(config : dict, api_key):
    genai.configure(api_key=api_key)
    if 'system_instruction' not in config:
        config['system_instruction'] = None
    if 'safety_settings' not in config:
        config['safety_settings'] = None
    if 'generation_config' not in config:
        config['generation_config'] = None
    model = genai.GenerativeModel(config['model']
                              ,system_instruction = config['system_instruction']
                              ,safety_settings = config['safety_settings']
                              ,generation_config = config['generation_config'])
    return model

@st.cache_data
def GetGeminiResponse(config : dict, prompt : str, api_key):
    model = GetGeminiModel(config, api_key)
    response = model.generate_content(prompt)
    return response

@st.cache_data
def GetGeminiChunkAbstract(chunks, chunkPrompt, abstractPrompt):
    responses = []
    for c in chunks:
        response = GetGeminiResponse({'model':'gemini-1.5-flash', 
                       'system_instruction': chunkPrompt,
                       'generation_config':{'candidate_count':1,'max_output_tokens': 500,'temperature':0.5}},c)
        responses.append(response.text)

    abstract = GetGeminiResponse({'model':'gemini-1.5-flash',
                          'system_instruction': abstractPrompt,
                          'generation_config':{'candidate_count':1,'max_output_tokens': 500,'temperature':0.5}},json.dumps(responses, ensure_ascii=False, indent=4))
    
    abstract = abstract.text.replace("```","").replace("json","")
    result = {}
    for i, r in enumerate(responses):
        result[f'Chunk_{i+1}'] = r.replace("```","").replace("json","")
    result['Resumo'] = abstract
    return json.dumps(result)

@st.cache_data
def GetGeminiConfig(config_type):
    with open("configs/gemini_config.yaml",'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config[config_type]

@st.cache_data
def load_embedding_model():
    with st.spinner('Baixando modelo de vetorização...'):
        model_name = "neuralmind/bert-base-portuguese-cased"
        #llm_model_dir = '../DB/bertimbau/'
        embedding_model = SentenceTransformer(
            model_name, 
            #cache_folder=llm_model_dir, 
            device='cpu'
        ) 
        return embedding_model

@st.cache_data
def vetorize_text(text, _model):
    return _model.encode([text]).astype("float32")

@st.cache_data
def load_texts():
    texts = []
    with open('DB/texts.txt', 'r', encoding='utf-8') as f:
        for line in f:
            texts.append(line.strip())
    return texts

@st.cache_data
def load_faiss():
    index = faiss.read_index("DB/faiss_index.bin")
    return index
