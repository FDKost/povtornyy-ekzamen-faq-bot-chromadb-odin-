from bot import FAQBot

def main():
    bot = FAQBot()
    print("FAQ Bot is ready. Type your question (or 'exit' to quit).")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            response = bot.answer(user_input)
            print(f"Bot: {response}")
        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
