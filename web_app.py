from translator import translate

def main():
    print("🌾 Local Language Translator for Farmers 🌾")
    
    while True:
        print("\nMenu:")
        print("1. Translate Local → English")
        print("2. Translate English → Local")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            text = input("Enter text in local language (Yoruba): ")
            print("👉 English:", translate(text, "English"))

        elif choice == "2":
            text = input("Enter text in English: ")
            print("👉 Yoruba:", translate(text, "Yoruba"))

        elif choice == "3":
            print("Goodbye 👋")
            break
        else:
            print("❌ Invalid choice, try again.")

if __name__ == "__main__":
    main()
