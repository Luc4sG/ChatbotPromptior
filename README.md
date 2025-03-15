# Chatbot RAG - Promptior

## Descripción 

Este proyecto es un **chatbot basado en RAG (Retrieval-Augmented Generation)** diseñado para responder preguntas sobre **Promptior** utilizando documentación y contenido web previamente indexado. Implementa una arquitectura modular que combina recuperación de contexto con generación de respuestas mediante **GPT-3.5-turbo**.

El chatbot está desarrollado con **LangChain**, utiliza **ChromaDB** como base de datos vectorial para almacenar embeddings, y está expuesto mediante una **API REST con LangServe y FastAPI**. El despliegue en producción se realiza en **AWS**, mientras que para desarrollo local se puede ejecutar en un contenedor **Docker**.

## Tecnologías Usadas

- **Python 3.10+**
- **LangChain v0.2** 
- **Langserve - FastAPI** 
- **OpenAI model: GPT-3.5-turbo** 
- **ChromaDB** 
- **LangSmith**
- **Docker** 
- **AWS** 

##  Configuración y Despliegue Local con Docker

Para ejecutar el chatbot en un entorno local utilizando **Docker**, sigue los siguientes pasos:

### Clonar el Repositorio

```sh
 git clone https://github.com/Luc4sG/ChatbotPromptior
 cd ChatbotPromptior
```

### Construir y Ejecutar el Contenedor Docker
Ejecuta los siguientes comandos:

```sh
docker-compose build
```

### Acceder al chatbot disponible en:
```
http://localhost:8000
```



