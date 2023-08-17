from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA,  ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.prompts import PromptTemplate

import logging
import gradio as gr
import param

#funcion para cargar base de datos

def load_db(file, chain_type, k):
    
    # load documents
    loader = PyPDFLoader(file)
    documents = loader.load()
    # split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)
    # define embedding
    embeddings = OpenAIEmbeddings()
    # create vector database from data
    #db = DocArrayInMemorySearch.from_documents(docs, embeddings)
    #persist_directory = 'DB/chroma_cons/'
    db = Chroma.from_documents(documents=docs, embedding=embeddings)
    # define retriever
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    # create a chatbot chain. Memory is managed externally.
    
    # Construir el prompt
    template = """Use las siguientes piezas de contexto para responder la pregunta al final. \
    Si no sabe la respuesta, simplemente diga que no sabe, no intente inventar una respuesta. \
    Utilice cinco frases como máximo. Mantenga la respuesta lo más concisa posible. \
    Siempre diga "¡gracias por preguntar!" al final de la respuesta.
    {context}
    Pregunta: {question}
    por favor dar las respuesta en español
    Respuesta:"""
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)  
    chain_type_kwargs = {"prompt":QA_CHAIN_PROMPT}
    
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0), 
        chain_type="stuff", 
        retriever=retriever, 
        chain_type_kwargs=chain_type_kwargs
    )
    
    # qa = ConversationalRetrievalChain.from_llm(
    #     llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0), 
    #     chain_type=chain_type, 
    #     retriever=retriever, 
    #     return_source_documents=True,
    #     return_generated_question=True,
    # )
    return qa 


class chatbot(param.Parameterized):
    chat_history = param.List([])
    answer = param.String("")
    db_query  = param.String("")
    db_response = param.List([])
    
    def __init__(self,  **params):
        super(chatbot, self).__init__( **params)
        self.loaded_file = "docs/constitucion_nacion_argentina.pdf"
        self.qa = load_db(self.loaded_file,"stuff", 4)
    
    
    def convchain(self, query):
        result = self.qa.run(query)
        #print(result)
        # self.chat_history.extend([(query, result["answer"])])
        # self.db_query = result["generated_question"]
        # self.db_response = result["source_documents"]
        # self.answer = result['answer']
        return result
          
def consultas(procear, archivo, question): 
    respuesta = chat.convchain(question)
    print(respuesta)
    return respuesta
    
iface = gr.Interface(
    fn=consultas,
    inputs=[
        gr.components.Checkbox(label="Procesar Archivo"),
        gr.components.File(label="Seleccione un archivo PDF", type="file"),
        gr.components.Textbox(label="Realice una consulta:")
    ],
    outputs=gr.components.Textbox(),
    title="Interfaz de Consulta de Archivos PDF",
    description="Cargue un archivo PDF, procese y realice consultas para obtener respuestas basadas en el contenido del archivo."
    )   


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger('langchain.retrievers.multi_query').setLevel(logging.INFO)
    chat = chatbot()
    iface.launch()