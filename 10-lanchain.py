from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Para controlar la aleatoriedad y la creatividad del 
# texto generado de un LLM, uso temperatura = 0.0
chat = ChatOpenAI(temperature=0.0)
#print(chat)

template_string = """Traducir el texto \
que está delimitado por triples acentos \
en un estilo que es {estilo}. \
texto: ```{texto}```
"""
prompt_template = ChatPromptTemplate.from_template(template_string)

estilo_str = """Ingles, \
en un tono tranquilo y respetuoso
""" 

texto_str = """🚀 Descubre el mundo de la Inteligencia Artificial y \
amplía tus horizontes tecnológicos con nuestros cursos especializados. \
Desde los fundamentos hasta aplicaciones avanzadas, te guiaremos en \
cada paso del camino. ¡Únete a nosotros y sé parte de la revolución tecnológica!\
🤖📚 #InteligenciaArtificial #AprendizajeTecnológico #CursosTech
"""

mensaje = prompt_template.format_messages(
                    estilo= estilo_str,
                    texto= texto_str)

respuesta = chat(mensaje)
print(respuesta.content)