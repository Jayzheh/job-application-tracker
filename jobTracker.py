import pandas as pd
from datetime import datetime, timedelta

class JobTracker:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_excel(file_path)
        
    def display_data(self):
        print("\nCurrent Applications:")
        print(self.df.to_string(index=True))
        
    def add_entry(self):
        print("\nAdding new entry:")
        new_entry = {
            'Entreprise': input("Company name: "),
            'Lien vers l\'offre': input("Job link (press Enter to skip): "),
            'Date Candidature': datetime.now(),
            'Date de relance': datetime.now() + timedelta(days=5),
            'Date de relance 2': datetime.now() + timedelta(days=10),
            'Réponse': 'en cours',
            'Contact': input("Contact (press Enter to skip): "),
            'Commentaire': input("Comments (press Enter to skip): ")
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_entry])], ignore_index=True)
        self.save()
        
    def update_entry(self):
        self.display_data()
        try:
            row_idx = int(input("\nEnter row number to update: "))
            column = input("Enter column name to update: ")
            new_value = input("Enter new value: ")
            self.df.at[row_idx, column] = new_value
            self.save()
        except:
            print("Invalid input. Please try again.")
            
    def delete_entry(self):
        self.display_data()
        try:
            row_idx = int(input("\nEnter row number to delete: "))
            self.df = self.df.drop(row_idx)
            self.save()
        except:
            print("Invalid input. Please try again.")
            
    def clear_all(self):
        confirm = input("Are you sure you want to clear all data? (yes/no): ")
        if confirm.lower() == 'yes':
            self.df = pd.DataFrame(columns=self.df.columns)
            self.save()
            print("All data cleared.")
        
    def save(self):
        self.df.to_excel(self.file_path, index=False)
        print("Changes saved successfully!")

def main():
    tracker = JobTracker("Digi2 - [Prénom] [NOM] copy.xlsx")
    
    while True:
        print("\n=== Job Application Tracker ===")
        print("1. Display all entries")
        print("2. Add new entry")
        print("3. Update entry")
        print("4. Delete entry")
        print("5. Clear all data")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            tracker.display_data()
        elif choice == '2':
            tracker.add_entry()
        elif choice == '3':
            tracker.update_entry()
        elif choice == '4':
            tracker.delete_entry()
        elif choice == '5':
            tracker.clear_all()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()