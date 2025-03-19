import xmlrpc.client

def display_notes(notes):
    if not notes:
        print("No notes found")
        return
    
    for i, note in enumerate(notes, 1):
        print(f"\nNote {i}:")
        print(f"Name:    {note['name']}")
        print(f"Content: {note['text']}")
        print(f"Time:    {note['timestamp']}")
    print("-"*50)

def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
    
    while True:
        print("\n1. Add Note\n2. Get Notes\n3. Exit")
        choice = input("Choose action: ").strip()
        
        if choice == "1":
            topic = input("Enter topic: ").strip()
            note_name = input("Enter note name: ").strip()
            text = input("Enter content: ").strip()
            
            result = proxy.add_note(topic, note_name, text)
            if result is True:
                print("note added successfully")
            else:
                print(f"note added failed: {result}")
        
        elif choice == "2":
            topic = input("Enter topic to search: ").strip()
            notes = proxy.get_notes(topic)
            display_notes(notes)
        
        elif choice == "3":
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()