import openai
import os
import gradio as gr

# Configura tu clave de API de OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY')

#set contexto
messages = [{"role": "system","content": "Eres un chatbot, muestrate proactivo y participativo. Da respuestas sencillas y no muy largas"}]

def gpt35(pregunta,historia):
    messages.append({"role": "user", "content": pregunta})
    respuesta = openai.ChatCompletion.create(
        model ="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
    )
    texto = respuesta.choices[0].message.content
    messages.append({"role": "assistant", "content": texto})
    return texto

iface = gr.ChatInterface(
    gpt35,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Hazme una pregunta", container=False, scale=7),  
    title="Chatbot de OpenAI",
    description="Escribe una pregunta y obtén una respuesta generada por ChatGPT."
    
)

if __name__ == "__main__":
    iface.launch()
