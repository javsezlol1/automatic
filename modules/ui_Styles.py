import gradio as gr
import gradio.components
import json
from json import loads
from PIL import Image
import os
import csv
import modules.shared as shared
import datetime
import urllib.parse
refresh_symbol = '\U0001f504'  # 🔄
close_symbol = '\U0000274C'  # ❌
save_symbol = '\U0001F4BE' #💾
delete_style = '\U0001F5D1' #🗑️
clear_symbol = '\U0001F9F9' #🧹
download_symbol = '\U00002B07' #⬇️

def create_json_objects_from_csv(csv_file):
    json_objects = []
    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row.get('name', None)
            prompt = row.get('prompt', None)
            negative_prompt = row.get('negative_prompt', None)
            if name is None or prompt is None or negative_prompt is None:
                print("Warning: Skipping row with missing values.")
                continue
            json_data = {
                "name": name,
                "description": "converted from csv",
                "categories": ["CSV-Converted"],
                "tags": ["CSV-Converted"],
                "thumbnail": f"{name}.jpg",
                "prompt": prompt,
                "negative": negative_prompt,
                "extra": "Steps:20, Sampler:LMSD, CFG scale: 6, Seed: -1, Size: 1024x1024"
            }
            json_objects.append(json_data)
    return json_objects

def save_json_objects(json_objects):
    if not json_objects:
        print("Warning: No JSON objects to save.")
        return

    styles_dir = os.path.join("models", "styles")
    csv_conversion_dir = os.path.join(styles_dir, "CSVConversion")
    os.makedirs(csv_conversion_dir, exist_ok=True)

    for json_obj in json_objects:
        json_file_path = os.path.join(csv_conversion_dir, f"{json_obj['name']}.json")
        with open(json_file_path, 'w') as jsonfile:
            json.dump(json_obj, jsonfile, indent=4)

        image_path = os.path.join(csv_conversion_dir, f"{json_obj['name']}.jpg")
        img = Image.open(os.path.join("html", "no-style-preview.jpg"))
        img.save(image_path)
current_directory = os.path.dirname(__file__)
csv_file_path = os.path.join("styles.csv")
json_objects = create_json_objects_from_csv(csv_file_path)
save_json_objects(json_objects)
try:
    os.remove(csv_file_path)
    print("CSV file deleted successfully.")
except OSError as e:
    print(f"Error deleting the CSV file: {e.filename}")
#styles libary --> starts here
def generate_html_code(selected_category=None, selected_tag=None, search=None):
    style = None
    style_html = ""
    tags_list = []
    categories_list = ["all"]
    styles_dir = os.path.join("models", "styles")
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%H:%M:%S.%f')
    formatted_time = formatted_time.replace(":", "")
    formatted_time = formatted_time.replace(".", "")
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
                            img = os.path.abspath(img)
                            prompt = style.get("prompt", "")
                            prompt_negative = style.get("negative", "")
                            extra = style.get("extra", "")
                            categories = style.get("categories", "")
                            tags = style.get("tags", "")
                            imghack = img.replace("\\", "/")
                            json_file_path = json_file_path.replace("\\", "/")
                            encoded_filename = urllib.parse.quote(filename, safe="")
                            encoded_save_folder = urllib.parse.quote(json_file_path, safe="")
                            for category in categories:
                                if category.lower() not in categories_list:
                                    categories_list.append(category.lower())
                            tagsstring = ", ".join(tags)
                            categoriesstring = ", ".join(categories)
                            if selected_category is not None and selected_category != "all" and not any(value in selected_category for value in [category.lower() for category in categories]):
                                continue
                            for tag in tags:
                                if tag.lower() not in tags_list:
                                    tags_list.append(tag.lower())
                            tags_list = sorted(tags_list)
                            if selected_tag is not None and not any(value in selected_tag for value in [tag.lower() for tag in tags]):
                                continue
                            if search is not None and search.lower() not in title.lower() and search.lower() not in description.lower():
                                continue
                            style_html += f"""
                            <div class="style_card" style="height:{shared.opts.extra_networks_card_size}px;">
                                <img class="styles_thumbnail" src="{"file=" + img +"?timestamp"+ formatted_time}" alt="{title} Preview">
                                    <button class="EditStyleJson" onclick="editStyle('{title}','{imghack}','{description}','{prompt}','{prompt_negative}','{extra}','{categoriesstring}','{tagsstring}','{encoded_filename}','{encoded_save_folder}')">🖉</button>
                                    <div onclick="applyStyle('{prompt}','{prompt_negative}','{extra}')" onmouseenter="event.stopPropagation(); hoverPreviewStyle('{prompt}','{prompt_negative}','{extra}')" onmouseleave="hoverPreviewStyleOut()" class="styles_overlay"></div>
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
    if cat is None or len(cat) == 0 or cat  == "[]" :
        cat = None
    newhtml = generate_html_code(cat,None)
    newhtml_sendback = newhtml[0]
    newtags_sendback = newhtml[1]
    newcat_sendback = newhtml[2]
    return newhtml_sendback,gr.update(value=[],choices=newtags_sendback),gr.update(choices=newcat_sendback)

def filter_tags(cat,tag,search):
    if search is None or len(search) == 0 or search  == "[]" :
        search = None
    if cat is None or len(cat) == 0 or cat  == "[]" :
        cat = None
    if tag is None or len(tag) == 0 or tag  == "[]":
        tag = None
    newhtml = generate_html_code(cat,tag,search)
    newhtml_sendback = newhtml[0]
    return newhtml_sendback

def filter_category(cat):
    if cat is None or len(cat) == 0 or cat  == "[]" :
        cat = None
    newhtml = generate_html_code(cat,None)
    newhtml_sendback = newhtml[0]
    newtags_sendback = newhtml[1]
    return newhtml_sendback ,gr.update(choices=newtags_sendback,value=[]),gr.update(value=""),

def StylesFolderList():
    styles_dir = os.path.join("models", "styles")
    subfolders = []

    for root, dirs, _files in os.walk(styles_dir):
        for folder in dirs:
            folder_path = os.path.relpath(os.path.join(root, folder), styles_dir)
            folder_path = folder_path.replace("\\", "/")
            subfolders.append(folder_path)

    return subfolders

def RefreshStylesFolderList():
    styles_dir = os.path.join("models", "styles")
    subfolders = []

    for root, dirs, _files in os.walk(styles_dir):
        for folder in dirs:
            folder_path = os.path.relpath(os.path.join(root, folder), styles_dir)
            folder_path = folder_path.replace("\\", "/")
            subfolders.append(folder_path)
    return gr.update(choices=subfolders)

def tempfolderbox(dropdown):
    return gr.update(value=dropdown)

def save_style(title, img, description, categories, tags, prompt, prompt_negative, extra, filename, save_folder):
    if save_folder and categories and tags and filename:
        tags = tags.replace(", ", ",")
        tags = tags.lower()
        categories = categories.replace(", ", ",")
        categories = categories.lower()
        if img is None or img == "":
            img = Image.open(os.path.join("html", "no-style-preview.jpg"))

        img = img.resize((200, 200))
        save_folder_path = os.path.join("models", "styles", save_folder)
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)

        shared.log.debug(tags)
        json_data = {
            "name": title,
            "description": description,
            "categories": categories.split(","),
            "tags": tags.split(","),
            "thumbnail": filename + ".jpg",
            "prompt": prompt,
            "negative": prompt_negative,
            "extra": extra
        }
        json_file_path = os.path.join(save_folder_path, filename + ".json")
        with open(json_file_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)
        img_path = os.path.join(save_folder_path, filename + ".jpg")
        img.save(img_path)
        msg = f"""<p style="color:green;">File Saved to '{save_folder}'</p>"""
    else:
        msg = """<p style="color:red;">Please provide a valid save folder, category, tags.</p>"""
    return filename_check(save_folder,filename),gr.update(value=msg)

def img_to_thumbnail(img):
    return gr.update(value=img)

def clear_style():
    return gr.update(value=None),gr.update(value=None),gr.update(value=None),gr.update(value=None),gr.update(value=None),gr.update(value=None),gr.update(value=None),gr.update(value=None),gr.update(value=None),gr.update(value=None)

def filename_check(folder,filename):
    if filename is None or len(filename) == 0 :
        warning = """<p id="style_filename_check" style="color:red;">please add a file name</p>"""
    else:
        save_folder_path = os.path.join("models", "styles", folder)
        json_file_path = os.path.join(save_folder_path, filename + ".json")
        if os.path.exists(json_file_path):
            warning = f"""<p id="style_filename_check" style="color:red;">Overwrite!! File Already Exists In '{folder}'</p>"""
        else:
            warning = """<p id="style_filename_check" style="color:green;">Filename Is Valid</p>"""
    return gr.update(value=warning)

def deletestyle(folder, filename):
    base_path = os.path.join("models", "styles", folder)
    json_file_path = os.path.join(base_path, filename + ".json")
    jpg_file_path = os.path.join(base_path, filename + ".jpg")

    if os.path.exists(json_file_path):
        os.remove(json_file_path)
        print(f"Deleted {json_file_path}")

        if os.path.exists(jpg_file_path):
            os.remove(jpg_file_path)
            print(f"Deleted {jpg_file_path}")
        else:
            shared.log.warning(f"Error: {jpg_file_path} not found.")
    else:
        shared.log.warning(f"Error: {json_file_path} not found.")

def create_ui(container, button):
    folderlist = StylesFolderList()
    generate_styles_and_tags = generate_html_code()
    with gr.Tabs():
        with gr.TabItem(label="Style Libary",elem_id="styles_libary"):
            with gr.Column():
                gr.HTML(f"""<h2 data-cardcover="{shared.opts.extra_networks_card_cover}" data-sidebarwidth="{shared.opts.extra_networks_sidebar_width}"></h2>""", label="Title", lines=1,visible=False)
                with gr.Row(elem_id="style_search_search"):
                    Style_Search = gr.Textbox('', show_label=False, elem_id="style_search", placeholder="Search...", elem_classes="textbox", lines=1)
                    refresh_button = gr.Button(refresh_symbol, label="Refresh", elem_id="style_refresh", elem_classes="button", lines=1)
                with gr.Row(elem_id="style_cards_row"):
                    with gr.Column(elem_id="style_tags_column"):
                        category_dropdown = gr.Dropdown(label="Catagory", choices=generate_styles_and_tags[2], default="all", lines=1, elem_id="style_Catagory", elem_classes="dropdown styles_dropdown")
                        tag_dropdown = gr.Dropdown(label="Tags", choices=generate_styles_and_tags[1], default=None, lines=1, elem_id="style_tags", elem_classes="dropdown styles_dropdown", multiselect=True)
                        with gr.Column(elem_id="style_cards_Pref"):
                            gr.Checkbox(label="Apply Prompt",value=True, default=True, elem_id="styles_apply_prompt", elem_classes="styles_checkbox checkbox", lines=1)
                            gr.Checkbox(label="Apply Negative",value=True, default=True, elem_id="styles_apply_neg", elem_classes="styles_checkbox checkbox", lines=1)
                            gr.Checkbox(label="Apply Extras",value=False, default=True, elem_id="styles_apply_extra", elem_classes="styles_checkbox checkbox", lines=1)
                            gr.Checkbox(label="Hover Over Preview",value=True, default=True, elem_id="HoverOverStyle_preview", elem_classes="styles_checkbox checkbox", lines=1)
                    with gr.Column(elem_id="style_cards_column"):
                        with gr.Row():
                            Styles_html=gr.HTML(generate_styles_and_tags[0])
        with gr.TabItem(label="Style Editor",elem_id="styles_editor"):
            with gr.Column():
                with gr.Row():
                    with gr.Column():
                        style_title_txt = gr.Textbox(label="Title:", lines=1,placeholder="Title goes here",elem_id="style_title_txt")
                        with gr.Row():
                            with gr.Column(elem_id="style_img_btn_column"):
                                style_lastgen_btn =gr.Button("⇝",label="Save Style", lines=1,elem_id="style_lastgen_btn")
                            with gr.Column(elem_id="style_img_column"):
                                thumbnailbox = gr.Image(value=None,label="Thumbnail:",elem_id="style_thumbnailbox",elem_classes="image",interactive=True,type='pil')
                                style_img_url_txt = gr.Text(label=None,lines=1,placeholder="Description goes here", elem_id="style_img_url_txt",visible=False)
                        style_description_txt = gr.Textbox(label="Description:", lines=1,placeholder="Description goes here", elem_id="style_description_txt")
                        style_category_txt = gr.Textbox(label="Categories:", lines=1,placeholder="Please add 1 or more tags", elem_id="style_category_txt")
                        style_tags_txt = gr.Textbox(label="Tags:", lines=1,placeholder="Please add 1 or more categories", elem_id="style_tags_txt")
                    with gr.Column():
                        with gr.Row(elem_id="style_command_btn_row"):
                            style_save_check = gr.HTML("""<p id="style_filename_check" style="color:red;"></p>""",elem_id="style_save_status_container")
                            style_grab_current_btn = gr.Button(download_symbol,label="Grab Current", lines=1,elem_classes="tool", elem_id="style_grab_current_btn")
                            style_save_btn = gr.Button(save_symbol,label="Save Style", lines=1,elem_classes="tool", elem_id="style_save_btn")
                            style_clear_btn = gr.Button(clear_symbol,label="Clear", lines=1,elem_classes="tool" ,elem_id="style_clear_btn")
                            style_delete_btn = gr.Button(delete_style,label="Delete Style", lines=1,elem_classes="tool", elem_id="style_delete_btn")
                        style_prompt_txt = gr.Textbox(label="Prompt:", lines=2,placeholder="Prompt goes here", elem_id="style_prompt_txt")
                        style_negative_txt = gr.Textbox(label="Negative:", lines=2,placeholder="Negative goes here", elem_id="style_negative_txt")
                        style_extra_txt = gr.Textbox(label="Extra:", lines=1,placeholder="Extra goes here", elem_id="style_extra_txt")
                        style_filename_txt = gr.Textbox(label="Filename Name:", lines=1,placeholder="Filename", elem_id="style_filename_txt")
                        style_filname_check = gr.HTML("""<p id="style_filename_check" style="color:red;">Please Add a Filename</p>""",elem_id="style_filename_check_container")
                        with gr.Row(elem_id="gradio_style_savefolder_row"):
                            style_savefolder_refrsh_btn = gr.Button(refresh_symbol, label="Refresh", lines=1,elem_classes="tool")
                            style_savefolder_txt = gr.Dropdown(label="Save Folder:", choices=folderlist, default="Style 1", lines=1, elem_id="style_savefolder_txt", elem_classes="dropdown",allow_custom_value=True)
                            style_savefolder_temp = gr.Textbox(label="Save Folder:",default="Style 1", lines=1, elem_id="style_savefolder_temp",visible=False)

    # Call the generate_html_code function
    style_grab_current_btn.click(fn=None,_js='grabCurrentSettings')
    style_filename_txt.change(fn=filename_check, inputs=[style_savefolder_temp,style_filename_txt], outputs=[style_filname_check])
    style_savefolder_temp.change(fn=filename_check, inputs=[style_savefolder_temp,style_filename_txt], outputs=[style_filname_check])
    style_lastgen_btn.click(fn=None,_js='grabLastGeneratedimage')
    style_clear_btn.click(fn=clear_style, outputs=[style_title_txt,thumbnailbox,style_img_url_txt,style_description_txt,style_category_txt,style_tags_txt,style_prompt_txt,style_negative_txt,style_extra_txt,style_filename_txt])
    style_delete_btn.click(fn=deletestyle, inputs=[style_savefolder_temp,style_filename_txt])
    style_savefolder_txt.change(fn=tempfolderbox, inputs=[style_savefolder_txt], outputs=[style_savefolder_temp])
    style_save_btn.click(fn=save_style, inputs=[style_title_txt, thumbnailbox, style_description_txt, style_category_txt, style_tags_txt, style_prompt_txt, style_negative_txt, style_extra_txt, style_filename_txt, style_savefolder_temp], outputs=[style_filname_check,style_save_check])
    style_savefolder_refrsh_btn.click(fn=RefreshStylesFolderList, outputs=[style_savefolder_txt])
    style_img_url_txt.change(fn=img_to_thumbnail, inputs=[style_img_url_txt],outputs=[thumbnailbox])
    refresh_button.click(fn=refresh_styles,inputs=[category_dropdown], outputs=[Styles_html,tag_dropdown,category_dropdown])
    Style_Search.change(fn=filter_tags, inputs=[category_dropdown,tag_dropdown,Style_Search], outputs=[Styles_html])
    tag_dropdown.select(fn=filter_tags, inputs=[category_dropdown,tag_dropdown,Style_Search], outputs=[Styles_html])
    category_dropdown.select(fn=filter_category, inputs=[category_dropdown], outputs=[Styles_html,tag_dropdown,Style_Search])
    def toggle_visibility(is_visible):
        is_visible = not is_visible
        return is_visible, gr.update(visible=is_visible), gr.update(variant=("secondary-down" if is_visible else "secondary"))
    state_visible = gr.State(value=False)  # pylint: disable=abstract-class-instantiated
    button.click(fn=toggle_visibility, inputs=[state_visible], outputs=[state_visible, container, button])

