from search import search_prompt

def main():
    print("Sistema de ingestão e busca semântica de dados")
    print("=" * 50)
    print("Faça sua pergunta (ou digite 'sair' para encerrar):\n")

    try:
        while True:
            question = input("PERGUNTA: ").strip()

            if question.lower() == "sair":
                print("\nAté breve!")
                break

            if not question:
                continue

            response = search_prompt(question)

            if response is None:
                print("RESPOSTA: Erro ao processar a pergunta.\n")
            else:
                print(f"RESPOSTA: {response}\n")

            print("-" * 50 + "\n")

    except KeyboardInterrupt:
        print("\n\nChat encerrado!")            

if __name__ == "__main__":
    main()