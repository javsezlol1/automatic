import gradio as gr
import gradio.components
import json
import os
import modules.shared as shared
refresh_symbol = '\U0001f504'  # 🔄
close_symbol = '\U0000274C'  # ❌


def generate_html_code(selected_tag=None):
    style = None
    style_html = ""
    tags_list = []
    styles_dir = os.path.join("models", "styles")
    try:
        for filename in os.listdir(styles_dir):
            if filename.endswith(".json"):
                with open(os.path.join(styles_dir, filename), "r", encoding="utf-8") as f:
                    try:
                        style = json.load(f)
                        title = style.get("name", "")
                        preview_image = style.get("thumbnail", "")
                        description = style.get("description", "")
                        img = os.path.join("models", "styles") + "/" + preview_image
                        prompt = style.get("prompt", "")
                        prompt_negative = style.get("negative", "")
                        extra = style.get("extra", "")
                        tags = style.get("tags", "")

                        for tag in tags:
                            if tag not in tags_list:
                                tags_list.append(tag)

                        #if the selected tag is not non and any value from the selected tag is in tags then continue
                        if selected_tag != None and any(value in selected_tag for value in tags) == False:
                            continue
                        style_html  += f"""
                        <div class="style_card">
                        <div>{title}</div>
                        <img src="{"file=" + os.path.abspath(img)}" alt="{title} Preview">
                        <p>{description}</p>
                        <div>
                                <button onclick="applystyle('{prompt}','{prompt_negative}','{extra}')">test</button>
                        </div>
                        </div>
                            """
                        #create_styles(style_html, prompt, prompt_negative, extra)
                    except json.JSONDecodeError:
                        print(f"Error parsing JSON in file: {filename}")
                    except KeyError as e:
                        print(f"KeyError: {e} in file: {filename}")
    except FileNotFoundError:
        print("Directory '/models/styles' not found.")
    return style_html, tags_list

class StylesUi:
    def __init__(self):
        self.search = None


def search_tags(tag):
    if len(tag) == 0 or tag  == "[]" or tag == None:
        newhtml = generate_html_code()
    else:
        newhtml = generate_html_code(tag)
    newhtml_sendback = newhtml[0]
    return newhtml_sendback

def refresh(): 
    newhtml = generate_html_code()
    newhtml_sendback = newhtml[0]
    return newhtml_sendback

def create_ui(container, button):
    ui = StylesUi()
    generate_styles_and_tags = generate_html_code()
    with gr.Column():
        gr.HTML("<h2>Styles</h2>", label="Title", lines=1)
        with gr.Row(elem_id="style_search_row"):
            ui.search = gr.Textbox('', show_label=False, elem_id="style_search", placeholder="Search...", elem_classes="textbox", lines=1)
            refresh_button = gr.Button(refresh_symbol, label="Refresh", elem_id="style_refresh", elem_classes="button", lines=1)
        with gr.Row(elem_id="style_cards_row"):
            tag_dropdown = gr.Dropdown(label="Tags", choices=generate_styles_and_tags[1], default=None, lines=1, elem_id="style_tags", elem_classes="dropdown", multiselect=True)
            with gr.Group():
                with gr.Row():
                    Styles_html=gr.HTML(generate_styles_and_tags[0])
                    

            # Call the generate_html_code function
    refresh_button.click(fn=refresh,inputs=[], outputs=Styles_html)
    tag_dropdown.select(fn=search_tags, inputs=[tag_dropdown], outputs=[Styles_html])
    def toggle_visibility(is_visible):
        is_visible = not is_visible
        return is_visible, gr.update(visible=is_visible), gr.update(variant=("secondary-down" if is_visible else "secondary"))
   
    state_visible = gr.State(value=False)  # pylint: disable=abstract-class-instantiated
    button.click(fn=toggle_visibility, inputs=[state_visible], outputs=[state_visible, container, button])

