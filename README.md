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

## Configuración y Despliegue Local con Docker

Para ejecutar el chatbot en un entorno local utilizando **Docker**, sigue los siguientes pasos:

### Clonar el Repositorio

```sh
 git clone https://github.com/Luc4sG/ChatbotPromptior
 cd ChatbotPromptior
```

### Configurar Variables de Entorno

Antes de construir y ejecutar el contenedor Docker, asegúrate de configurar las variables de entorno necesarias. Puedes hacerlo de las siguientes maneras:

1. Configurando las variables de entorno directamente en tu sistema.
2. Creando un archivo de secretos con el formato:
   ```sh
   echo <api_key> > oa_api_key.txt
   ```

### Construir y Ejecutar el Contenedor Docker

Ejecuta los siguientes comandos:

```sh
docker-compose build
docker-compose up
```

### Acceder al Chatbot

El chatbot estará disponible en:
```
http://localhost:8000
```

## Versión Desplegada en AWS

Puedes visitar la versión desplegada en AWS. El enlace se encuentra en la documentación del proyecto.

# Chatbot RAG - Promptior

## Description 

This project is a **chatbot based on RAG (Retrieval-Augmented Generation)** designed to answer questions about **Promptior** using pre-indexed documentation and web content. It implements a modular architecture that combines context retrieval with response generation using **GPT-3.5-turbo**.

The chatbot is developed with **LangChain**, uses **ChromaDB** as a vector database to store embeddings, and is exposed via a **REST API with LangServe and FastAPI**. The production deployment is done on **AWS**, while for local development it can be run in a **Docker** container.

## Technologies Used

- **Python 3.10+**
- **LangChain v0.2** 
- **Langserve - FastAPI** 
- **OpenAI model: GPT-3.5-turbo** 
- **ChromaDB** 
- **LangSmith**
- **Docker** 
- **AWS** 

## Local Configuration and Deployment with Docker

To run the chatbot in a local environment using **Docker**, follow these steps:

### Clone the Repository

```sh
 git clone https://github.com/Luc4sG/ChatbotPromptior
 cd ChatbotPromptior
```

### Configure Environment Variables

Before building and running the Docker container, make sure to configure the necessary environment variables. You can do this in the following ways:

1. Setting the environment variables directly on your system.
2. Creating a secrets file with the format:
   ```sh
   echo <api_key> > oa_api_key.txt
   ```

### Build and Run the Docker Container

Run the following commands:

```sh
docker-compose build
docker-compose up
```

### Access the Chatbot

The chatbot will be available at:
```
http://localhost:8000
```

## Deployed Version on AWS

You can visit the deployed version on AWS. The link is found in the project documentation.



