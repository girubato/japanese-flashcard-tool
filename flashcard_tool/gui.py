import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple

class FlashcardGUI:
    def __init__(self, root, db, translator):
        """Initialize the flashcard application GUI"""
        self.root = root
        self.db = db
        self.translator = translator
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface"""
        self.root.title("Japanese Flashcard Tool")
        self.root.geometry("500x400")
        
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input section
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Add New Flashcard", padding="10")
        self.input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.input_frame, text="Kanji:").grid(row=0, column=0, sticky=tk.W)
        self.kanji_entry = ttk.Entry(self.input_frame, width=30)
        self.kanji_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.add_button = ttk.Button(
            self.input_frame, 
            text="Add Flashcard", 
            command=self._add_flashcard
        )
        self.add_button.grid(row=0, column=2, padx=5)
        
        # Display section
        self.display_frame = ttk.LabelFrame(self.main_frame, text="Your Flashcards", padding="10")
        self.display_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview for displaying flashcards
        self.tree = ttk.Treeview(
            self.display_frame, 
            columns=('kanji', 'hiragana', 'meaning'), 
            show='headings'
        )
        
        # Configure columns
        self.tree.heading('kanji', text='Kanji')
        self.tree.heading('hiragana', text='Hiragana')
        self.tree.heading('meaning', text='English Meaning')
        
        self.tree.column('kanji', width=100, anchor=tk.CENTER)
        self.tree.column('hiragana', width=150, anchor=tk.CENTER)
        self.tree.column('meaning', width=250, anchor=tk.W)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.display_frame, 
            orient=tk.VERTICAL, 
            command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Load existing flashcards
        self._load_flashcards()
    
    def _add_flashcard(self):
        """Add a new flashcard to the database"""
        kanji = self.kanji_entry.get().strip()
        if not kanji:
            messagebox.showerror("Error", "Please enter a kanji word")
            return
        
        translation = self.translator.get_translation_info(kanji)
        if not translation:
            messagebox.showerror("Error", "Could not translate the kanji word")
            return
        
        # Add to database
        success = self.db.add_flashcard(
            kanji=translation['kanji'],
            hiragana=translation['hiragana'],
            english_meaning=translation['english_meaning']
        )
        
        if success:
            messagebox.showinfo("Success", "Flashcard added successfully!")
            self.kanji_entry.delete(0, tk.END)
            self._load_flashcards()
        else:
            messagebox.showerror("Error", "Failed to add flashcard to database")
    
    def _load_flashcards(self):
        """Load flashcards from database into the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch from database
        flashcards = self.db.get_all_flashcards()
        for card in flashcards:
            self.tree.insert('', tk.END, values=card)