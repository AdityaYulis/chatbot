from rag.chatbot import ask

while True:
    question = input("\nAnda:")

    if question.lower() == "exit":
        break

    result = ask(question)

    print("\nChatbot:")
    print(result["answer"])

    print("\nSumber:")

    for source in result["sources"]:
        print(
            f"- {source['title']}"
        )