
import tkinter as tk
import requests
GOOGLE_FORMS_URL = "https://docs.google.com/forms/u/0/d/e/YOURURL/formResponse"

def submit_to_google_form():
    score = dayscore.get()
    note = notes.get("1.0", tk.END).strip()

    if note == "":
        note = "No notes"
    
    print(score, note)
    form_data = {
        "entry.YOUR ENTRY": score,
        "entry.YOUR ENTRY": note
    }
    response = requests.post(GOOGLE_FORMS_URL, data=form_data)
    return response.status_code == 200


def validitychecker(event=None):
    score = dayscore.get()
    if score:
        
        try:
            score = float(score)
            print(score)
            if score >= 0 and score < 10: 
                if len(str(score)) <= 3:
                    return submit_to_google_form()
                else:
                    error2 = tk.Label(root, text="Number must be only 1 decimal place or less", font=("Arial", 14), fg="blue")
                    error2.pack()
                    root.after(3000, error2.destroy)
                    return False
            else:
                error1 = tk.Label(root, text="Number must be from 0 to 10", font=("Arial", 14), fg="blue")
                error1.pack()
                root.after(3000, error1.destroy)
                return False
            
        except Exception as e:
            error3 = tk.Label(root, text="An unknown error occurred", font=("Arial", 14), fg="blue")
            error3.pack()
            root.after(3000, error3.destroy)
            return False

def lock_window():
    pass
def quitw(event=None):
    root.quit()

root = tk.Tk()
root.attributes('-fullscreen', True)
root.protocol("WM_DELETE_WINDOW", lock_window)
root.attributes('-fullscreen', True)
root.config(bg="#191d1e")

root.title("DailyScore")


tk.Label(root, text="Enter Day Score(0-10):", font=("Arial", 12,), width = 20, height=1).pack()

dayscore = tk.Entry(root)
dayscore.pack(pady=10)
tk.Label(root, text="Enter Notes:", font=("Arial", 12,), width = 10, height=1).pack()

notes = tk.Text(root, width = 50, height = 10)
notes.pack(pady=10)

submit = tk.Button(root, text="Submit", command=validitychecker, bg = "#404d71",  font=("Arial", 12,), width = 10, height=2)
submit.pack(pady=20)


instructions = tk.Label(root, text="Tab - Move Fields | Enter - Submit | Escape - Close", font=("Arial", 18, "bold"), bg = "#191d1e", fg="#ffffff",)

# Pack the label at the bottom with the anchor option
instructions.pack(side="bottom", pady=30)


root.bind("<Escape>", quitw)
root.bind("<Return>", validitychecker)


root.mainloop()
