import threading
import customtkinter as ctk

from core.strength import check_strength
from core.breach import check_local, check_hibp
from core.suggestions import improve_password, generate_strong

COLORS = {'Weak': '#e74c3c', 'Medium': '#f1c40f', 'Strong': '#2ecc71'}

app = ctk.CTk()
app.title('Password Checker')
app.geometry('500x450')
app.resizable(False, False)
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

# ── Title ──
ctk.CTkLabel(app, text='Password Strength & Breach Checker',
             font=('Segoe UI', 20, 'bold')).pack(pady=(20, 15))

# ── Entry row ──
entry_frame = ctk.CTkFrame(app, fg_color='transparent')
entry_frame.pack(pady=5)
pw_entry = ctk.CTkEntry(entry_frame, width=300, show='•',
                        placeholder_text='Enter password…', font=('Segoe UI', 14))
pw_entry.pack(side='left', padx=(0, 8))
show_var = [False]


def toggle_vis():
    show_var[0] = not show_var[0]
    pw_entry.configure(show='' if show_var[0] else '•')
    eye_btn.configure(text='🙈' if show_var[0] else '👁')


eye_btn = ctk.CTkButton(entry_frame, text='👁', width=36, command=toggle_vis)
eye_btn.pack(side='left')

# ── Results frame ──
result_frame = ctk.CTkFrame(app)
result_frame.pack(pady=15, padx=30, fill='x')
strength_lbl = ctk.CTkLabel(result_frame, text='Strength: —', font=('Segoe UI', 15, 'bold'))
strength_lbl.pack(pady=(12, 4))
breach_lbl = ctk.CTkLabel(result_frame, text='Breach status: —', font=('Segoe UI', 13))
breach_lbl.pack(pady=4)
suggest_lbl = ctk.CTkLabel(result_frame, text='Suggestion: —',
                           font=('Segoe UI', 13), wraplength=420)
suggest_lbl.pack(pady=(4, 12))


def show_breach(password):
    """Run HIBP check in a background thread to keep UI responsive."""
    count = check_hibp(password)
    if count == -1:
        msg = '⚠️ HIBP unavailable, local check only'
        color = '#f1c40f'
    elif count == 0:
        msg = '✅ Not found in breaches'
        color = '#2ecc71'
    else:
        msg = f'🚨 Found in {count:,} breaches!'
        color = '#e74c3c'
    breach_lbl.configure(text=f'Breach status: {msg}', text_color=color)


def check():
    password = pw_entry.get()
    if not password:
        return

    # Strength
    result = check_strength(password)
    level = result['level']
    strength_lbl.configure(
        text=f"Strength: {level}  ({result['score']}/5)",
        text_color=COLORS[level],
    )

    # Local check + suggestion
    local = check_local(password)
    suggestion = improve_password(password) if level != 'Strong' else generate_strong()
    tag = '  ⚠ (common password!)' if local else ''
    suggest_lbl.configure(text=f'Suggestion: {suggestion}{tag}')

    # HIBP in background
    breach_lbl.configure(text='Breach status: checking…', text_color='gray')
    threading.Thread(target=show_breach, args=(password,), daemon=True).start()


ctk.CTkButton(app, text='Check Password', width=200, height=38,
              font=('Segoe UI', 14, 'bold'), command=check).pack(pady=10)

