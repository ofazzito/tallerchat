from transformers import pipeline

clasificador = pipeline("text-classification", #tarea
                        model="nlptown/bert-base-multilingual-uncased-sentiment") #modelo
secuencia = "Estoy muy contento de aprender sobre esta increible biblioteca transformers"

resultado = clasificador(secuencia)
print(resultado)