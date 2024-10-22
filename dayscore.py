import tkinter as tk
import requests

GOOGLE_FORMS_URL = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSfCy2Ll923EqIaS_-kUkDVQqFnmDLQu0oMKTGdJxR2OpIeoBA/formResponse"

def submit_to_google_form(score, notes):
    form_data = {
        "entry.318239957": score,
        "entry.1566268890": notes
    }
    response = requests.post(GOOGLE_FORMS_URL, data=form_data)
    return response.status_code == 200

def lock_screen():
    root = tk.Tk()
    root.attributes("-fullscreen", True)  
    root.configure(bg='black')
    root.wm_attributes("-topmost", 1)
    root.overrideredirect(True)

    def close_app():
        label.config(text="Closed. Unlocking system...", fg="red")
        root.after(2000, root.destroy) 

    close_button = tk.Button(root, text="X", font=("Helvetica", 16), command=close_app, bg="red", fg="white")
    close_button.pack(anchor="ne", padx=20, pady=20)
    
    def submit_score():
        score = entry.get()
        notes = entry1.get()
        try:
            score = float(score)
            if 1 <= score <= 10 and len(score.as_integer_ratio()) <= 2:
                if submit_to_google_form(score, notes):
                    label.config(text="Score submitted! Unlocking system...", fg="green")
                    root.after(2000, root.destroy)  
                else:
                    label.config(text="Failed to submit score. Try again.", fg="red")
            else:
                label.config(text="Please enter a score between 1 and 10 with up to 2 decimal places.", fg="red")
        except ValueError:
            label.config(text="Invalid input. Please enter a valid number.", fg="red")

    label = tk.Label(root, text="Enter your day score (1-10) to unlock the system:",
                     font=("Helvetica", 20), fg="white", bg="black")
    label.pack(expand=True)

    input_frame = tk.Frame(root, bg="black")
    input_frame.pack(side="bottom", pady=50)

    score_label = tk.Label(input_frame, text="Score:", font=("Helvetica", 16), fg="white", bg="black")
    score_label.grid(row=0, column=0, padx=10, pady=10)

    entry = tk.Entry(input_frame, font=("Helvetica", 16), justify='center', width=10)
    entry.grid(row=0, column=1, padx=10, pady=10)

    notes_label = tk.Label(input_frame, text="Notes:", font=("Helvetica", 16), fg="white", bg="black")
    notes_label.grid(row=1, column=0, padx=10, pady=10)

    entry1 = tk.Entry(input_frame, font=("Helvetica", 16), justify='center', width=30)
    entry1.grid(row=1, column=1, padx=10, pady=10)

    submit_button = tk.Button(input_frame, text="Submit", font=("Helvetica", 16), command=submit_score)
    submit_button.grid(row=2, column=0, columnspan=2, pady=20)
   


    def submit_score():
        score = entry.get()
        notes = entry1.get()
        try:
            score = float(score)
            score = score(round(score, 1))

            if 1 <= score <= 10:
                if submit_to_google_form(score, notes):
                    label.config(text="Score submitted! Unlocking system...", fg="green")
                    root.after(2000, root.destroy)  
                else:
                    label.config(text="Failed to submit score. Try again.", fg="red")
            else:
                label.config(text="Please enter a score between 1 and 10 with up to 2 decimal places.", fg="red")
        except ValueError:
            label.config(text="Invalid input. Please enter a valid number.", fg="red")

    
    root.mainloop()

if __name__ == "__main__":
    lock_screen()
