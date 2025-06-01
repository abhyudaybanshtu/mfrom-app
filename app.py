import streamlit as st
from PIL import Image
from datetime import date
import os

# --- CONFIGURATION ---
digit_folder = "digits"
template_folder = "templates"  # folder containing virender.png, vikram.png, etc.

# Digit positioning and spacing
big_y = 1124
big_date_x = 815
big_time_x = 1018
big_gap_default = 20
big_gap_after_one = 15
big_gap_after_dash = 13
big_gap_after_colon = 33

small_y = 319
small_date_x = 955
small_time_x = 1060
small_size_default = (10, 16)
small_size_one = (8, 16)
small_gap_default = 11
small_gap_after_one = 9
small_gap_after_dash = 4
small_gap_after_colon = 4

def get_small_digit_img_and_gap(char):
    size = small_size_one if char == '1' else small_size_default
    gap = small_gap_after_one if char == '1' else small_gap_default
    img = Image.open(f"{digit_folder}/{char}.png").convert("RGBA").resize(size, Image.LANCZOS)
    return img, gap

def generate_form(input_date, input_time, form_template):
    form = Image.open(form_template).convert("RGBA")

    # Big Date
    x = big_date_x
    for char in input_date:
        digit_img = Image.open(f"{digit_folder}/{char}.png").convert("RGBA")
        form.paste(digit_img, (x, big_y), digit_img)
        gap = big_gap_after_one if char == '1' else big_gap_after_dash if char == '-' else big_gap_default
        x += gap

    # Big Time
    x = big_time_x
    for char in input_time:
        if char == ':':
            colon_img = Image.open(f"{digit_folder}/colon.png").convert("RGBA")
            colon_img.thumbnail((10, 30), Image.LANCZOS)
            form.paste(colon_img, (x, big_y), colon_img)
            x += colon_img.width + 2
        else:
            digit_img = Image.open(f"{digit_folder}/{char}.png").convert("RGBA")
            form.paste(digit_img, (x, big_y), digit_img)
            x += big_gap_after_one if char == '1' else big_gap_default

    # Small Date
    x = small_date_x
    for char in input_date:
        if char == '-':
            dash_img = Image.open(f"{digit_folder}/-.png").convert("RGBA").resize(small_size_default, Image.LANCZOS)
            form.paste(dash_img, (x, small_y), dash_img)
            x += small_gap_after_dash
        else:
            digit_img, gap = get_small_digit_img_and_gap(char)
            form.paste(digit_img, (x, small_y), digit_img)
            x += gap

    # Small Time
    x = small_time_x
    for char in input_time:
        if char == ':':
            colon_img = Image.open(f"{digit_folder}/colon.png").convert("RGBA")
            colon_img.thumbnail(small_size_default, Image.LANCZOS)
            form.paste(colon_img, (x, small_y), colon_img)
            x += small_gap_after_colon
        else:
            digit_img, gap = get_small_digit_img_and_gap(char)
            form.paste(digit_img, (x, small_y), digit_img)
            x += gap

    return form


# --- STREAMLIT UI ---
st.title("🧾 M-Form Generator")

# Load available templates dynamically from the folder
template_options = [f for f in os.listdir(template_folder) if f.endswith(".png")]
template_name = st.selectbox("Choose Form Template", template_options)
form_template_path = os.path.join(template_folder, template_name)

# Auto-set today's date
input_date = date.today().strftime("%Y-%m-%d")
st.write(f"📅 Today's Date: {input_date}")

# Let user input time
input_time = st.text_input("Enter Time (HH:MM)", "16:21")

if st.button("Generate M-Form"):
    try:
        result_img = generate_form(input_date, input_time, form_template_path)
        result_img.save("mform_final_output.png")
        st.success("✅ Form generated successfully!")
        st.image(result_img, caption="Generated M-Form", use_column_width=True)
    except Exception as e:
        st.error(f"❌ Error: {e}")
