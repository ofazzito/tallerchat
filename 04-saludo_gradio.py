import gradio as gr

def saludo(nombre):
    return "Hola " + nombre + ", ¿Como estas??? "


demo = gr.Interface(
    fn=saludo, 
    inputs = "text",
    outputs = "text"
)

demo.launch()