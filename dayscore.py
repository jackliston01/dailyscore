import cv2
import numpy as np
import requests

GOOGLE_FORMS_URL = "https://docs.google.com/forms/u/0/d/e/YOURURL/formResponse"

def submit_to_google_form(score, notes):
    form_data = {
        "entry.YOUR ENTRY": score,
        "entry.YOUR ENTRY": notes
    }
    response = requests.post(GOOGLE_FORMS_URL, data=form_data)
    return response.status_code == 200

def wrap_text(text, max_width=60):
    words = text.split()
    lines = []
    current_line = []
    current_width = 0
    
    for word in words:
        if current_width + len(word) <= max_width:
            current_line.append(word)
            current_width += len(word) + 1
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = len(word) + 1
    
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def draw_textbox(img, text, pos, active=False, is_notes=False):
    x, y = pos
    padding = 10
    box_color = (0, 255, 0) if active else (200, 200, 200)
    
    if is_notes:
        wrapped_text = wrap_text(text, max_width=55) 
        box_height = min(len(wrapped_text) * 40 + padding * 2, 200)  
        cv2.rectangle(img, (x-padding, y-30), (x + 800, y + box_height), box_color, 2)
        
        visible_lines = min(len(wrapped_text), 5)  
        for i in range(visible_lines):
            cv2.putText(img, wrapped_text[i], (x, y + i*40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    else:
        cv2.rectangle(img, (x-padding, y-30), (x + 400, y+10), box_color, 2)
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def lock_screen():
    window_name = 'Day Score Entry'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    img = np.zeros((720, 1280, 3), np.uint8)
    score = ""
    notes = ""
    message = "Enter your day score (1-10) to unlock the system"
    input_active = "score"
    cursor_visible = True
    cursor_timer = 0
    
    while True:
        img_display = img.copy()
        
        cursor_timer += 1
        if cursor_timer % 30 == 0:
            cursor_visible = not cursor_visible
        
        score_text = score + ("|" if input_active == "score" and cursor_visible else "")
        notes_text = notes + ("|" if input_active == "notes" and cursor_visible else "")
        
        cv2.putText(img_display, message, (320, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        draw_textbox(img_display, f"Score: {score_text}", (320, 250), input_active == "score")
        draw_textbox(img_display, f"Notes: {notes_text}", (320, 350), input_active == "notes", True)
        
        cv2.putText(img_display, "TAB: Switch fields | ENTER: Submit ", 
                    (320, 650), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        cv2.imshow(window_name, img_display)
        
        key = cv2.waitKey(100) & 0xFF
        
        if key != 255:
            if key == 27: 
                break
            elif key == 9:  
                input_active = "notes" if input_active == "score" else "score"
            elif key == 13:  
                try:
                    score_float = float(score)
                    if 1 <= score_float <= 10:
                        if submit_to_google_form(score_float, notes):
                            message = "Score submitted! Unlocking system..."
                            cv2.waitKey(2000)
                            break
                        else:
                            message = "Failed to submit score. Try again."
                    else:
                        message = "Please enter a score between 1 and 10."
                except ValueError:
                    message = "Invalid input. Please enter a valid number."
            elif key == 8:  
                if input_active == "score":
                    score = score[:-1]
                else:
                    notes = notes[:-1]
            elif input_active == "score" and len(score) < 4:
                if chr(key) in "0123456789.":
                    score += chr(key)
            elif input_active == "notes" and len(notes) < 500:
                notes += chr(key)
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    lock_screen()
