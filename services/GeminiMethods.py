import google.generativeai as genai
import streamlit as st
import json

#@st.cache_data
def GetGeminiModel(config : dict):
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
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

#@st.cache_data
def GetGeminiResponse(config : dict, prompt : str):
    model = GetGeminiModel(config)
    response = model.generate_content(prompt)
    return response

#@st.cache_data
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