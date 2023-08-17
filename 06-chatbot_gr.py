import openai
import os
import gradio as gr

# Configura tu clave de API de OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY')

def generar_respuesta(pregunta,historia):
    respuesta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=pregunta,
        max_tokens=50
        
    )
    print (pregunta,historia)
    return respuesta.choices[0].text.strip()


iface = gr.ChatInterface(
    generar_respuesta,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Hazme una pregunta", container=False, scale=7),  
    title="Chatbot de OpenAI",
    description="Escribe una pregunta y obtén una respuesta generada por ChatGPT."
    
)

if __name__ == "__main__":
    iface.launch()
