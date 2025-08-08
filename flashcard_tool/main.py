import tkinter as tk
from flashcard_tool.database import FlashcardDatabase
from flashcard_tool.translation import JapaneseTranslator
from flashcard_tool.gui import FlashcardGUI

def main():
    # Initialize components
    db = FlashcardDatabase()
    translator = JapaneseTranslator()
    
    # Create and run GUI
    root = tk.Tk()
    app = FlashcardGUI(root, db, translator)
    root.mainloop()

if __name__ == "__main__":
    main()