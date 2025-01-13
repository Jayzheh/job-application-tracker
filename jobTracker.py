import pandas as pd
from datetime import datetime, timedelta
import os
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

class JobTracker:
    def __init__(self):
        # Get user first and last name
        self.prenom = input("Enter your first name (Prénom): ")
        self.nom = input("Enter your last name (NOM): ")
        self.file_name = f"Digi2 - {self.prenom} {self.nom}.xlsx"
        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.file_name)
        
        if not os.path.exists(self.file_path):
            columns = ['Entreprise', 'Lien vers l\'offre', 'Date Candidature', 
                    'Date de relance', 'Date de relance 2', 'Réponse', 
                    'Contact', 'Commentaire']
            self.df = pd.DataFrame(columns=columns)
            self.save_file()
        else:
            try:
                self.df = pd.read_excel(self.file_path, engine='openpyxl')
            except Exception as e:
                print(f"Error reading file: {e}")
                self.df = pd.DataFrame()

    def save_file(self):
        try:
            # Create backup just in case
            if os.path.exists(self.file_path):
                backup_name = f"Digi2 - {self.prenom} {self.nom}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                backup_path = os.path.join(os.path.dirname(self.file_path), backup_name)
                os.rename(self.file_path, backup_path)
            
            # Save new file file
            self.df.to_excel(self.file_path, index=False, engine='openpyxl')
            print(f"Changes saved successfully to {self.file_name}!")
        except Exception as e:
            print(f"Error saving file: {e}")

    def display_data(self):
        if self.df.empty:
            print("\nNo entries found.")
        else:
            print("\nCurrent Applications:")
            pd.set_option('display.max_rows', None)
            df_display = self.df.copy()
            
            print("\nColumns available:")
            for i, col in enumerate(df_display.columns):
                print(f"Col {i}: {col}")
            
            print("\nData:")

            for idx, row in df_display.iterrows():
                print(f"\nRow {idx}:")
                for col in df_display.columns:
                    print(f"{col}: {row[col]}")
                print("-" * 80)  
            
            print(f"\nTotal entries: {len(df_display)}")

    def add_entry(self):
        while True:
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
            self.save_file()
            
            if self.return_to_menu():
                break

    def update_entry(self):
        while True:
            if self.df.empty:
                print("\nNo entries to update.")
                return
            
            self.display_data()
            try:
                row_idx = int(input("\nEnter row number to update: "))
                print("\nAvailable columns:")
                for i, col in enumerate(self.df.columns):
                    print(f"{i}: {col}")
                column = input("Enter column name or number to update: ")
                
                if column.isdigit():
                    column = self.df.columns[int(column)]
                
                new_value = input("Enter new value: ")
                self.df.at[row_idx, column] = new_value
                self.save_file()
                
                if self.return_to_menu():
                    break
            except Exception as e:
                print(f"Error updating entry: {e}")
                if self.return_to_menu():
                    break

    def delete_entry(self):
        while True:
            if self.df.empty:
                print("\nNo entries to delete.")
                return
                
            self.display_data()
            try:
                row_idx = int(input("\nEnter row number to delete: "))
                confirm = input(f"Are you sure you want to delete row {row_idx}? (yes/no): ")
                if confirm.lower() == 'yes':
                    self.df = self.df.drop(row_idx)
                    self.save_file()
                
                if self.return_to_menu():
                    break
            except Exception as e:
                print(f"Error deleting entry: {e}")
                if self.return_to_menu():
                    break

    def clear_all(self):
        if self.df.empty:
            print("\nNo data to clear.")
            return
            
        confirm = input("Are you sure you want to clear all data? (yes/no): ")
        if confirm.lower() == 'yes':
            self.df = pd.DataFrame(columns=self.df.columns)
            self.save_file()
            print("All data cleared.")

    def return_to_menu(self):
        choice = input("\nReturn to main menu? (yes/no): ")
        return choice.lower() in ['yes', 'y']

def main():
    tracker = JobTracker()
    
    while True:
        print("\n=== Job Application Tracker ===")
        print("1. Display all entries")
        print("2. Add new entry")
        print("3. Update entry")
        print("4. Delete entry")
        print("5. Clear all data")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '6':
            confirm = input("Are you sure you want to exit? (yes/no): ")
            if confirm.lower() in ['yes', 'y']:
                print("Goodbye!")
                break
            continue
            
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
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()