import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI 
from langchain_postgres import PGVector
from langchain_core.prompts import PromptTemplate 

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
  try:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = PGVector(
      connection=DATABASE_URL,
      embeddings=embeddings,
      collection_name=COLLECTION_NAME
    )

    docs = vector_store.similarity_search(question, k=10)
    contexto = "\n\n".join([doc.page_content for doc in docs])

    prompt_template = PromptTemplate(
      input_variables=["contexto", "pergunta"],
      template=PROMPT_TEMPLATE
    )

    prompt_filled = prompt_template.format(
      contexto=contexto,
      pergunta=question
    )

    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    response_llm = llm.invoke(prompt_filled)
    return response_llm.content

  except Exception as e:
    print(f"Erro ao processar a pergunta: {str(e)}")
    return None