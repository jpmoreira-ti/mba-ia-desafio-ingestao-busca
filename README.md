# Ingestão e Busca Semântica com LangChain e PostgreSQL

## 📋 Descrição do Projeto

Sistema de ingestão e busca semântica que permite:

1. **Ingestão:** Lê um arquivo PDF e armazena seu conteúdo vetorizado em PostgreSQL com extensão pgVector
2. **Busca Semântica:** Permite realizar perguntas via CLI e retornar respostas baseadas **somente** no conteúdo do PDF

### Regras

- ✅ Divisão de PDF em chunks (1000 caracteres com overlap de 150)
- ✅ Geração de embeddings com OpenAI ou Google Gemini
- ✅ Armazenamento vetorizado em PostgreSQL + pgVector
- ✅ Busca dos 10 documentos mais relevantes
- ✅ Interface CLI interativa
- ✅ Respostas precisas baseadas apenas no contexto do PDF

---

## 🔧 Pré-requisitos

### Sistema
- **Python 3.8+** instalado
- **Docker** e **Docker Compose** instalados

### APIs
- Pode usar:
  - **OpenAI API Key** (para usar `text-embedding-3-small` e `gpt-4-nano`)
  - **Google Gemini API Key** (para usar `embedding-001` e `gemini-2.5-flash-lite`)

---

## 📦 Estrutura do Projeto

```
├── docker-compose.yml          # Configuração do PostgreSQL + pgVector
├── requirements.txt            # Dependências Python
├── .env                        # Variáveis de ambiente (não committar)
├── .env.example                # Template de variáveis
├── document.pdf                # PDF para ingestão
├── README.md                   # Este arquivo
└── src/
    ├── ingest.py              # Script de ingestão do PDF
    ├── search.py              # Funções de busca semântica
    └── chat.py                # CLI interativa
```

---

## 🚀 Como Usar

### 1. Criar Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Preencha o `.env` com suas chaves:
- **OPENAI_API_KEY** ou **GOOGLE_API_KEY**: Sua chave da API (OpenAI ou Google)
- **DATABASE_URL**: URL de conexão ao PostgreSQL (padrão para Docker: `postgresql://postgres:postgres@localhost:5432/rag`)
- **PG_VECTOR_COLLECTION_NAME**: Nome da collection (exemplo: `pdf_documents`)
- **PDF_PATH**: Caminho do arquivo PDF (exemplo: `document.pdf`)

Veja `.env.example` para a estrutura completa.

### 4. Subir o Banco de Dados
```bash
docker compose up -d
```

Aguarde 10-15 segundos para o PostgreSQL estar pronto.

### 5. Ingerir o PDF
```bash
python src/ingest.py
```

Fluxo:
- Carregar o `document.pdf`
- Dividir em chunks
- Gerar embeddings
- Armazenar no banco de dados

### 6. Executar o Chat Interativo
```bash
python src/chat.py
```
Aplicação pronta para receber perguntas
---

## 💬 Exemplo de Uso

```
Faça sua pergunta (ou 'sair' para encerrar):

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

---

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

---

## 📝 Notas Importantes

- O sistema responde **APENAS** com base no conteúdo do PDF
- Se a informação não estiver no PDF, retorna: "Não tenho informações necessárias para responder sua pergunta."
- Nunca inventa ou usa conhecimento externo
- Para parar o chat, digite `sair`

---