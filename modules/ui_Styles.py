import gradio as gr
import gradio.components
import json
import os
import modules.shared as shared
refresh_symbol = '\U0001f504'  # 🔄
close_symbol = '\U0000274C'  # ❌


def generate_html_code(selected_category=None, selected_tag=None, search=None):
    style = None
    style_html = ""
    tags_list = []
    categories_list = ["all"]
    styles_dir = os.path.join("models", "styles")
    
    try:
        for root, _, files in os.walk(styles_dir):
            for filename in files:
                if filename.endswith(".json"):
                    json_file_path = os.path.join(root, filename)
                    with open(json_file_path, "r", encoding="utf-8") as f:
                        try:
                            style = json.load(f)
                            title = style.get("name", "")
                            preview_image = style.get("thumbnail", "")
                            description = style.get("description", "")
                            img = os.path.join(os.path.dirname(json_file_path), preview_image)
                            prompt = style.get("prompt", "")
                            prompt_negative = style.get("negative", "")
                            extra = style.get("extra", "")
                            categories = style.get("categories", "")
                            tags = style.get("tags", "")
                            
                            for category in categories:
                                if category not in categories_list:
                                    categories_list.append(category)
                                    
                            if selected_category is not None and selected_category != "all" and not any(value in selected_category for value in categories):
                                continue
                            
                            for tag in tags:
                                if tag not in tags_list:
                                    tags_list.append(tag)
                            tags_list = sorted(tags_list)
                            
                            if selected_tag is not None and not any(value in selected_tag for value in tags):
                                continue
                            
                            if search is not None and search.lower() not in title.lower() and search.lower() not in description.lower():
                                continue
                            style_html += f"""
                            <div onclick="applystyle('{prompt}','{prompt_negative}','{extra}')" class="style_card">
                                <img class="styles_thumbnail" src="{"file=" + os.path.abspath(img)}" alt="{title} Preview">
                                    <div onmouseenter="HoverPreviewStyle('{prompt}','{prompt_negative}')" onmouseleave="HoverPreviewStyleOut()" class="styles_overlay"></div>
                                    <div class="styles_title">{title}</div>
                                    <p class="styles_description">{description}</p>
                                </img>
                            </div>
                            """
                        except json.JSONDecodeError:
                            print(f"Error parsing JSON in file: {filename}")
                        except KeyError as e:
                            print(f"KeyError: {e} in file: {filename}")
    except FileNotFoundError:
        print("Directory '/models/styles' not found.")
    
    return style_html, tags_list, categories_list

def refresh_styles(cat):
    if cat == None or len(cat) == 0 or cat  == "[]" :
        cat = None 
    newhtml = generate_html_code(cat,None)
    newhtml_sendback = newhtml[0]
    newtags_sendback = newhtml[1]
    return newhtml_sendback,gr.update(value=[],choices=newtags_sendback)

def filter_tags(cat,tag,search):
    if search == None or len(search) == 0 or search  == "[]" :
        search = None
    if cat == None or len(cat) == 0 or cat  == "[]" :
        cat = None 
    if tag == None or len(tag) == 0 or tag  == "[]":
        tag = None
    newhtml = generate_html_code(cat,tag,search)
    newhtml_sendback = newhtml[0]
    return newhtml_sendback

def filter_category(cat):
    if cat == None or len(cat) == 0 or cat  == "[]" :
        cat = None 
    newhtml = generate_html_code(cat,None)
    newhtml_sendback = newhtml[0]
    newtags_sendback = newhtml[1]
    return newhtml_sendback ,gr.update(choices=newtags_sendback,value=[]),gr.update(value=[])

def create_ui(container, button):
    
    generate_styles_and_tags = generate_html_code()
    with gr.Column():
        gr.HTML(f"""<h2 data-cardcover="{shared.opts.extra_networks_card_cover}" data-sidebarwidth="{shared.opts.extra_networks_sidebar_width}" data-cardsize="{shared.opts.extra_networks_card_size}"  >Styles</h2>""", label="Title", lines=1)
        with gr.Row(elem_id="style_search_search"):
            Style_Search = gr.Textbox('', show_label=False, elem_id="style_search", placeholder="Search...", elem_classes="textbox", lines=1)
            refresh_button = gr.Button(refresh_symbol, label="Refresh", elem_id="style_refresh", elem_classes="button", lines=1)
        with gr.Row(elem_id="style_cards_Pref"):
            gr.Checkbox(label="Hover Over Preview",value=True, default=True, elem_id="HoverOverStyle_preview", elem_classes="checkbox", lines=1)
        with gr.Row(elem_id="style_cards_row"):
            with gr.Column(elem_id="style_tags_column"):
                category_dropdown = gr.Dropdown(label="Catagory", choices=generate_styles_and_tags[2], default="all", lines=1, elem_id="style_Catagory", elem_classes="dropdown")
                tag_dropdown = gr.Dropdown(label="Tags", choices=generate_styles_and_tags[1], default=None, lines=1, elem_id="style_tags", elem_classes="dropdown", multiselect=True)
            with gr.Column(elem_id="style_cards_column"):
                with gr.Row():
                    Styles_html=gr.HTML(generate_styles_and_tags[0])                   
            # Call the generate_html_code function
    refresh_button.click(fn=refresh_styles,inputs=[category_dropdown], outputs=[Styles_html,tag_dropdown])
    Style_Search.change(fn=filter_tags, inputs=[category_dropdown,tag_dropdown,Style_Search], outputs=[Styles_html])
    tag_dropdown.select(fn=filter_tags, inputs=[category_dropdown,tag_dropdown,Style_Search], outputs=[Styles_html])
    category_dropdown.select(fn=filter_category, inputs=[category_dropdown], outputs=[Styles_html,tag_dropdown,Style_Search])
    def toggle_visibility(is_visible):
        is_visible = not is_visible
        return is_visible, gr.update(visible=is_visible), gr.update(variant=("secondary-down" if is_visible else "secondary"))
   
    state_visible = gr.State(value=False)  # pylint: disable=abstract-class-instantiated
    button.click(fn=toggle_visibility, inputs=[state_visible], outputs=[state_visible, container, button])

