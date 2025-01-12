import pandas as pd
from datetime import datetime, timedelta
import os

class JobTracker:
    def __init__(self, file_path):
        self.file_path = file_path
        # Create file if it doesn't exist
        if not os.path.exists(file_path):
            columns = ['Entreprise', 'Lien vers l\'offre', 'Date Candidature', 
                      'Date de relance', 'Date de relance 2', 'Réponse', 
                      'Contact', 'Commentaire']
            self.df = pd.DataFrame(columns=columns)
            self.save()
        else:
            try:
                self.df = pd.read_excel(file_path, engine='openpyxl')
            except Exception as e:
                print(f"Error reading file: {e}")
                self.df = pd.DataFrame()

    def display_data(self):
        if self.df.empty:
            print("\nNo entries found.")
        else:
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
        if self.df.empty:
            print("\nNo entries to update.")
            return
        
        self.display_data()
        try:
            row_idx = int(input("\nEnter row number to update: "))
            column = input("Enter column name to update: ")
            new_value = input("Enter new value: ")
            self.df.at[row_idx, column] = new_value
            self.save()
        except Exception as e:
            print(f"Error updating entry: {e}")
            
    def delete_entry(self):
        if self.df.empty:
            print("\nNo entries to delete.")
            return
            
        self.display_data()
        try:
            row_idx = int(input("\nEnter row number to delete: "))
            self.df = self.df.drop(row_idx)
            self.save()
        except Exception as e:
            print(f"Error deleting entry: {e}")
            
    def clear_all(self):
        if self.df.empty:
            print("\nNo data to clear.")
            return
            
        confirm = input("Are you sure you want to clear all data? (yes/no): ")
        if confirm.lower() == 'yes':
            self.df = pd.DataFrame(columns=self.df.columns)
            self.save()
            print("All data cleared.")
        
    def save(self):
        try:
            self.df.to_excel(self.file_path, index=False, engine='openpyxl')
            print("Changes saved successfully!")
        except Exception as e:
            print(f"Error saving file: {e}")

def main():
    file_name = "Digi2 - [Prénom] [NOM] copy.xlsx"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    
    tracker = JobTracker(file_path)
    
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