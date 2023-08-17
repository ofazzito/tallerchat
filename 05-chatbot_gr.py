import openai
import os
import gradio as gr

# Configura tu clave de API de OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY')

def generar_respuesta(pregunta):
    respuesta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=pregunta,
        max_tokens=50
    )
    return respuesta.choices[0].text.strip()

def chatbot_interface(pregunta):
    respuesta = generar_respuesta(pregunta)
    return "Respuesta: " + respuesta

iface = gr.Interface(
    fn=chatbot_interface,
    inputs=gr.components.Textbox(label="Escribe tu pregunta aquí"),
    outputs=gr.components.Textbox(label="Respuesta generada"),
    title="Chatbot de OpenAI",
    description="Escribe una pregunta y obtén una respuesta generada por ChatGPT."
)


if __name__ == "__main__":
    iface.launch()