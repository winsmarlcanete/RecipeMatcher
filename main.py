from dataPreprocess import clean_recipe_data
from recommendersAlgorithm import string_match_recommender, brute_force_recommender, greedy_recommender
import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial

df = clean_recipe_data("dataset/recipes.csv")

class RecipeRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Recommender")
        self.ingredients = []

        self.create_splash_screen()

    def create_splash_screen(self):
        self.splash_frame = tk.Frame(self.root)
        self.splash_frame.pack(fill="both", expand=True)

        # You can replace this with a real image
        self.image_label = tk.Label(self.splash_frame, text="Click to Start", bg="lightblue", font=("Arial", 24), width=30, height=10)
        self.image_label.pack(expand=True)
        self.image_label.bind("<Button-1>", self.open_home_screen)

    def open_home_screen(self, event=None):
        self.splash_frame.destroy()
        self.create_home_screen()

    def create_home_screen(self):
        self.home_frame = tk.Frame(self.root, padx=10, pady=10)
        self.home_frame.pack(fill="both", expand=True)

        # Ingredient input
        input_label = tk.Label(self.home_frame, text="Enter Ingredient:")
        input_label.grid(row=0, column=0, sticky="w")

        self.ingredient_entry = tk.Entry(self.home_frame, width=30)
        self.ingredient_entry.grid(row=0, column=1)

        add_btn = tk.Button(self.home_frame, text="Add", command=self.add_ingredient)
        add_btn.grid(row=0, column=2)

        # Dropdown for algorithm
        algo_label = tk.Label(self.home_frame, text="Select Algorithm:")
        algo_label.grid(row=1, column=0, sticky="w")

        self.algo_choice = tk.StringVar()
        algo_dropdown = ttk.Combobox(self.home_frame, textvariable=self.algo_choice, values=["String Match", "Brute Force", "Greedy"], state="readonly")
        algo_dropdown.grid(row=1, column=1)
        algo_dropdown.current(0)

        # Ingredient list panel
        tk.Label(self.home_frame, text="Your Ingredients:").grid(row=2, column=0, sticky="nw")
        self.ingredient_listbox = tk.Listbox(self.home_frame, height=6)
        self.ingredient_listbox.grid(row=2, column=1, sticky="nsew")

        # Buttons to remove a selected ingredient and clear all ingredients
        remove_btn = tk.Button(self.home_frame, text="Remove", command=self.remove_ingredient)
        remove_btn.grid(row=3, column=0, pady=10)

        clear_btn = tk.Button(self.home_frame, text="Clear All", command=self.clear_all_ingredients)
        clear_btn.grid(row=3, column=2, pady=10)

        # Run button
        run_btn = tk.Button(self.home_frame, text="Recommend", command=self.run_algorithm)
        run_btn.grid(row=4, column=1, pady=10)

        # Results panel
        tk.Label(self.home_frame, text="Results:").grid(row=5, column=0, sticky="nw")
        self.results_text = tk.Text(self.home_frame, height=10, width=50)
        self.results_text.grid(row=5, column=1, columnspan=2)

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