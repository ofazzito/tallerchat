import webbrowser as web #abrir url de las imagenes y buscador
import openai 
import gradio as gr #interface
import logging as log #para llevar registros 

import pyttsx3 #convertir texto a voz

import threading #para dividir la ejecucion de programas en hilos
import re, string
import os #


#configura token de openai
#openai.api_key = cf.key

openai.api_key = os.environ['OPENAI_API_KEY'] 

#configuracion de registros
log.basicConfig(level=log.INFO)


# Función para obtener autocompletado
def bot_completion(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt, 
        max_tokens=100, #cantiad maxima de tokens en la respuesta
        n=1, #cantidad de respuestas
        stop=None, # caracter para marcar el fin de la respuesta
        temperature=0.5 # grado de creatividad 0-2 cuanto mas chico menos random       
        )
    
    return response.choices[0].text

#Funcion para el chat
def chat_completion(prompt, context): 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
        ]
    )    
    texto = response.choices[0].message.content
    
    return texto


def hablar(texto): #funcion para repoducir en audio el texto            
    log.info("Dando respuesta con voz...") #configuracion de voz assitente
    engine = pyttsx3.init() # configuración de voz del asistente
    engine.say(texto) # Se genera la voz a partir de un texto
    engine.runAndWait()   # Se reproduce la voz

def buscar_en_google(consulta):
    url = f"https://www.google.com/search?q={consulta}"
    web.open_new_tab(url)
    return url    
    

def procesar_chat(mensaje):
    resp = chat_completion(mensaje, "Eres un chatbot")
    #resp = chat_completion(mensaje, "Eres un chatbot, mustrate con personalidad divertida, ironica e irritable") 
    #resp = chat_completion(mensaje, "Eres un chatbot, muestrate proactivo y participativo")  
    return resp

def procesar_traduccion(prompt): 
    split = prompt.split(maxsplit=2)  
    #(Traduce) 
    # al + idioma + texto a traducir
    idioma = split[1]
    texto = split[2]
    log.info("Idioma: " + idioma)
    log.info("Frase: " + texto)
    traduccion = chat_completion(texto, "Eres traductor, asi que traduce esto al " + idioma)      
    return traduccion   

def procesar_dibujo(prompt):
    response = openai.Image.create(
        prompt = prompt,
        n = 1, # cantidad de imagenes puede ir de 1 a 10
        size = "1024x1024" #tamaño
        )
    url = response["data"][0]["url"]
    web.open(url) # abre imagen en una pestaña
    return  url

def procesar_entrada(audio,voz):  
    #print(audio) 
    log.info("Procesando audio ...")
    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1",audio_file)
    
    words = transcript["text"].split(maxsplit=1)
    # instruccion + el resto del texto
    instruc = re.sub('[%s]' % re.escape(string.punctuation), '', words[0]) 
    prompt = words[1]
    log.info("Transcripción: " + transcript["text"])
    log.info("Instrucción: " + instruc)
    log.info("Prompt: " + prompt)
    
    # diccionario que mapea instrucciones a funciones
    acciones = {
        "Dime": [procesar_chat, True], # orden : [funcion a llamar, muestra texto si/no]
        "Traduce": [procesar_traduccion,True],
        "Dibuja": [procesar_dibujo, False],
        "Busca": [buscar_en_google, False]
    }
    
    if instruc.capitalize() in acciones:
        funcion = acciones[instruc.capitalize()][0]
        respuesta = funcion(prompt)
        if voz:
            if not acciones[instruc.capitalize()][1]:
                respuesta = "Abriendo URL"  
            # Creamos un hilo para ejecutar la función hablar()
            t = threading.Thread(target=hablar, args=(respuesta,))
            t.start()         
        return respuesta
    else:
        resp = bot_completion(transcript["text"])
        if voz:
            # Creamos un hilo para ejecutar la función hablar()
            t = threading.Thread(target=hablar, args=(resp,))
            t.start()     
        return resp 

             
ui = gr.Interface(fn=procesar_entrada, 
                  inputs=[gr.Audio(source="microphone",type="filepath"),
                          gr.Checkbox(label="activar voz")],
                  outputs="text")
ui.launch()

