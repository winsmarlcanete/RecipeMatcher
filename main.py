from dataPreprocess import clean_recipe_data
from recommendersAlgorithm import string_match_recommender, brute_force_recommender, greedy_recommender
import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial
from PIL import Image, ImageTk


df = clean_recipe_data("dataset/recipes.csv")

class RecipeRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Matcher")
        self.ingredients = []
        self.root.state('zoomed')

        self.create_splash_screen()

    def create_splash_screen(self):
        self.splash_frame = tk.Frame(self.root)
        self.splash_frame.pack(fill="both", expand=True)

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Load and resize image
        image = Image.open("assets/home.png")  # <-- use your actual path
        image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.splash_photo = ImageTk.PhotoImage(image)

        # Display image as full-screen label
        self.image_label = tk.Label(self.splash_frame, image=self.splash_photo)
        self.image_label.pack(fill="both", expand=True)

        # Make the splash image clickable to continue
        self.image_label.bind("<Button-1>", self.open_home_screen)

    def open_home_screen(self, event=None):
        self.splash_frame.destroy()
        self.create_home_screen()

    def create_home_screen(self):
        self.home_frame = tk.Frame(self.root, padx=20, pady=20)
        self.home_frame.pack(expand=True)

        # Ingredient input
        input_frame = tk.Frame(self.home_frame)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Enter Ingredient:").pack(side=tk.LEFT)
        self.ingredient_entry = tk.Entry(input_frame, width=30)
        self.ingredient_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="Add", command=self.add_ingredient).pack(side=tk.LEFT)

        # Dropdown for algorithm
        algo_frame = tk.Frame(self.home_frame)
        algo_frame.pack(pady=5)

        tk.Label(algo_frame, text="Select Algorithm:").pack(side=tk.LEFT)
        self.algo_choice = tk.StringVar()
        algo_dropdown = ttk.Combobox(algo_frame, textvariable=self.algo_choice,
                                     values=["String Match", "Brute Force", "Greedy"], state="readonly")
        algo_dropdown.pack(side=tk.LEFT, padx=5)
        algo_dropdown.current(0)

        # Ingredient list
        tk.Label(self.home_frame, text="Your Ingredients:").pack(pady=(10, 0))
        self.ingredient_listbox = tk.Listbox(self.home_frame, height=6, width=40)
        self.ingredient_listbox.pack(pady=5)

        # Buttons for Remove and Clear
        button_frame = tk.Frame(self.home_frame)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Remove", command=self.remove_ingredient).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Clear All", command=self.clear_all_ingredients).pack(side=tk.LEFT, padx=5)

        # Recommend Button
        tk.Button(self.home_frame, text="Recommend", command=self.run_algorithm).pack(pady=10)

        # Results
        tk.Label(self.home_frame, text="Results:").pack(pady=(10, 0))
        self.results_text = tk.Text(self.home_frame, height=10, width=60)
        self.results_text.pack()

    def add_ingredient(self):
        ingredient = self.ingredient_entry.get().strip().lower()
        if ingredient:
            self.ingredients.append(ingredient)
            self.ingredient_listbox.insert(tk.END, ingredient)
            self.ingredient_entry.delete(0, tk.END)

    def remove_ingredient(self):
        selected_index = self.ingredient_listbox.curselection()
        if selected_index:
            # Get the ingredient name from the listbox and remove it from the ingredients list
            ingredient = self.ingredient_listbox.get(selected_index)
            self.ingredients.remove(ingredient)
            self.ingredient_listbox.delete(selected_index)
        else:
            messagebox.showwarning("No Selection", "Please select an ingredient to remove.")

    def clear_all_ingredients(self):
        # Clear the ingredients list and the listbox
        self.ingredients.clear()
        self.ingredient_listbox.delete(0, tk.END)

    def run_algorithm(self):
        algo = self.algo_choice.get()
        if not self.ingredients:
            messagebox.showwarning("No Ingredients", "Please add at least one ingredient.")
            return

        # Clear the previous results from the Text widget
        self.results_text.delete("1.0", tk.END)

        # Run the appropriate algorithm based on the user's choice
        if algo == "String Match":
            results = string_match_recommender(df, self.ingredients)
        elif algo == "Brute Force":
            results = brute_force_recommender(df, self.ingredients)
        else:
            results = greedy_recommender(df, self.ingredients)

        # Insert the new results into the Text widget
        if results:
            for recipe in results:
                self.results_text.insert(tk.END, f"Recipe: {recipe['name']} - Match: {recipe['score']}\n")
        else:
            self.results_text.insert(tk.END, "No matching recipes found.\n")

# Start the app
if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeRecommenderApp(root)
    root.mainloop()

    print(df.head())