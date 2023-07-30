var org_prompt="";
var org_negative="";

function applystyle(prompt,negative,extras) {

  const tabname = getENActiveTab();
  console.log(extras);
  const prompt_pos = gradioApp().querySelector(`#${tabname}_prompt > label > textarea`);
  applyprompts(prompt_pos, prompt);
  const prompt_ne = gradioApp().querySelector(`#${tabname}_neg_prompt > label > textarea`);
  applyprompts(prompt_ne, negative);
  //extras
  extrasjson = JSON.parse(extras_to_json(extras));
  console.log(extrasjson);
  const steps = gradioApp().querySelector(`#${tabname}_steps > div > div > input`);
  applyvalues(steps, extrasjson.Steps);
  const CFG = gradioApp().querySelector(`#${tabname}_cfg_scale > div > div > input`);
  applyvalues(CFG, extrasjson.scale);
  const Seed = gradioApp().querySelector(`#${tabname}_seed > label >input`);
  applyvalues(Seed, extrasjson.Seed);
  //extact width and height
    dimensions = extrasjson.Size.split("x");

    const WidthValue = parseInt(dimensions[0], 10);
    const width = gradioApp().querySelector(`#${tabname}_width > div > div > input`);
    applyvalues(width, WidthValue);

    const HeightValue = parseInt(dimensions[1], 10);
    const height = gradioApp().querySelector(`#${tabname}_height > div > div > input`);
    applyvalues(height, HeightValue);

  //not working
  const sampler = gradioApp().querySelector(`#${tabname}_sampling > label > div > div > div > input`);
  applyvalues(sampler, extrasjson.Sampler);

}
  
function HoverPreviewStyle(prompt,negative) {
  const enablePreviewChk = gradioApp().querySelector(`#HoverOverStyle_preview > label > input`);
  const enablePreview = enablePreviewChk.checked;
  console.log(enablePreview);
  if (enablePreview === true) {
    const tabname = getENActiveTab();
    const prompt_pos = gradioApp().querySelector(`#${tabname}_prompt > label > textarea`);
    const prompt_ne = gradioApp().querySelector(`#${tabname}_neg_prompt > label > textarea`);
    org_prompt = prompt_pos.value;
    org_negative = prompt_ne.value;
    const preview_prompt = prompt_pos.value + "," + prompt;
    const preview_negative = prompt_ne.value + "," + negative;
    prompt_pos.value = preview_prompt;
    prompt_ne.value = preview_negative;
    updateInput(prompt_pos);
    updateInput(prompt_ne);
  }
}

function HoverPreviewStyleOut() {
  const enablePreview = gradioApp().querySelector(`#HoverOverStyle_preview > label > input`).checked;
  if (enablePreview === true) {
    const tabname = getENActiveTab();
    const prompt_pos = gradioApp().querySelector(`#${tabname}_prompt > label > textarea`);
    const prompt_ne = gradioApp().querySelector(`#${tabname}_neg_prompt > label > textarea`);
    prompt_pos.value = org_prompt;
    prompt_ne.value = org_negative;
    updateInput(prompt_pos);
    updateInput(prompt_ne);
    org_prompt = "";
    org_negative = "";
  }
}


function extras_to_json(extras) {
    const regex = /(\w+):\s*([^,]+)/g;
    let match;
    const data = {};
    while ((match = regex.exec(extras)) !== null) {
      data[match[1]] = match[2];
    }
    const extrasjson = JSON.stringify(data);
    return extrasjson;
}

function applyprompts(a, b) {
  if (a.value === "") {
    a.value = b;
  } else {
    a.value = a.value + "," + b;
  }
  updateInput(a);
}

function applyvalues(a, b) {
    a.value = b;
    updateInput(a);
}


function setupStylesTab(tabname,cardcover, sidebarwidth,cardsize) {

  console.log(cardcover);
  //for (const el of Array.from(gradioApp().querySelectorAll('.styles_thubmnail'))) el.style.height = `${cardsize}px`;
  const en = gradioApp().querySelector(`#${tabname}_styles_popout`);
  if (cardcover === 'cover') {
    en.style.transition = '';
    en.style.zIndex = 9999;
    en.style.position = 'absolute';
    en.style.right = 'unset';
    en.style.width = 'unset';
    en.style.height = 'unset';
    gradioApp().getElementById(`${tabname}_settings`).parentNode.style.width = 'unset';
  } else if (cardcover === 'sidebar') {
    en.style.transition = 'width 0.2s ease';
    en.style.zIndex = 1;
    en.style.position = 'absolute';
    en.style.right = '0';
    en.style.width = `${sidebarwidth}vw`;
    en.style.height = 'unset';
    gradioApp().getElementById(`${tabname}_settings`).parentNode.style.width = `${100 - 2 -sidebarwidth}vw`;
  } else {
    en.style.transition = '';
    en.style.zIndex = 1;
    en.style.position = 'relative';
    en.style.right = 'unset';
    en.style.width = 'unset';
    en.style.height = 'unset';
   gradioApp().getElementById(`${tabname}_settings`).parentNode.style.width = 'unset';
  }
}

function setupStyles() {
  const tabname = getENActiveTab();
  const h2tag = gradioApp().querySelector(`#${tabname}_styles_popout > div > div > div > div > h2`);
  const cardcover = h2tag.dataset.cardcover;
  const cardsize = h2tag.dataset.cardsize;
  const sidebarwidth = h2tag.dataset.sidebarwidth;
  
  const styleTagEl = gradioApp().querySelector(`#style_tags_column`);
  const observerConfig = {
    childList: true, // Observe direct children being added or removed
    subtree: true,   // Observe all descendants of the target element
  };
  const observer = new MutationObserver((evt) => {
    console.log("changed")
    //setupStylesTab('txt2img',cardcover, sidebarwidth,cardsize);
    //setupStylesTab('img2img',cardcover, sidebarwidth,cardsize);
  });   
  observer.observe(styleTagEl, observerConfig);

  setupStylesTab('txt2img',cardcover, sidebarwidth,cardsize);
  setupStylesTab('img2img',cardcover, sidebarwidth,cardsize);
}

onUiLoaded(setupStyles);