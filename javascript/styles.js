/* eslint-disable linebreak-style */
/* eslint-disable no-use-before-define */
/* eslint-disable linebreak-style */
/* eslint-disable no-undef */
/* eslint-disable no-unused-vars */
let orgPrompt = '';
let orgNegative = '';
let orgSteps = '';
let orgSampler = '';
let orgCFG = '';
let orgSeed = '';
let orgWidth = '';
let orgHeight = '';

function applyStyle(prompt, negative, extras) {
  const tabname = getENActiveTab();
  const applyStylePrompt = gradioApp().querySelector('#styles_apply_prompt > label > input');
  if (applyStylePrompt.checked === true) {
    const promptPos = gradioApp().querySelector(`#${tabname}_prompt > label > textarea`);
    if (prompt.includes('{prompt}')) {
      orgPrompt = promptPos.value;
      prompt = prompt.replace('{prompt} .', orgPrompt);
      promptPos.value = prompt;
      updateInput(promptPos);
    } else {
      if (orgPrompt === '') orgPrompt = prompt;
      else { orgPrompt += `,${prompt}`; }
      applyPrompts(promptPos, prompt);
    }
  }
  const applyStyleNeg = gradioApp().querySelector('#styles_apply_neg > label > input');
  if (applyStyleNeg.checked === true) {
    const promptNeg = gradioApp().querySelector(`#${tabname}_neg_prompt > label > textarea`);
    if (negative !== '') {
      if (orgNegative === '') orgNegative = negative;
      else { orgNegative += `,${negative}`; }
      applyPrompts(promptNeg, negative);
    }
  }
  // extras
  const applyStyleExtra = gradioApp().querySelector('#styles_apply_extra > label > input');
  if (applyStyleExtra.checked === true) {
    try {
      const extrasjson = JSON.parse(extrasToJson(extras));
      try {
        const steps = gradioApp().querySelector(`#${tabname}_steps > div > div > input`);
        applyValues(steps, extrasjson.Steps);
      } catch (e) {}
      try {
        const CFG = gradioApp().querySelector(`#${tabname}_cfg_scale > div > div > input`);
        applyValues(CFG, extrasjson.scale);
      } catch (e) {}
      try {
        const Seed = gradioApp().querySelector(`#${tabname}_seed > label >input`);
        applyValues(Seed, extrasjson.Seed);
      } catch (e) {}
      try {
        // extact width and height
        dimensions = extrasjson.Size.split('x');
        const WidthValue = parseInt(dimensions[0], 10);
        const width = gradioApp().querySelector(`#${tabname}_width > div > div > input`);
        applyValues(width, WidthValue);
        const HeightValue = parseInt(dimensions[1], 10);
        const height = gradioApp().querySelector(`#${tabname}_height > div > div > input`);
        applyValues(height, HeightValue);
      } catch (e) {}
      // not working
      // try {
      // const sampler = gradioApp().querySelector(`#${tabname}_sampling > label > div > div > div > input`);
      // applyValues(sampler, extrasjson.Sampler);
      // } catch (e) {}
    } catch (e) {}
  }
}

function hoverPreviewStyle(prompt, negative, extras) {
  const enablePreviewChk = gradioApp().querySelector('#HoverOverStyle_preview > label > input');
  const enablePreview = enablePreviewChk.checked;
  if (enablePreview === true) {
    const tabname = getENActiveTab();
    const promptPos = gradioApp().querySelector(`#${tabname}_prompt > label > textarea`);
    const promptNeg = gradioApp().querySelector(`#${tabname}_neg_prompt > label > textarea`);
    const steps = gradioApp().querySelector(`#${tabname}_steps > div > div > input`);
    const sampler = gradioApp().querySelector(`#${tabname}_sampling > label > div > div > div > input`);
    const CFG = gradioApp().querySelector(`#${tabname}_cfg_scale > div > div > input`);
    const Seed = gradioApp().querySelector(`#${tabname}_seed > label >input`);
    const width = gradioApp().querySelector(`#${tabname}_width > div > div > input`);
    const height = gradioApp().querySelector(`#${tabname}_height > div > div > input`);
    orgSteps = steps.value;
    orgSampler = sampler.value;
    orgCFG = CFG.value;
    orgSeed = Seed.value;
    orgWidth = width.value;
    orgHeight = height.value;
    orgPrompt = promptPos.value;
    orgNegative = promptNeg.value;
    const previewPrompt = `${promptPos.value},${prompt}`;
    const previewNegative = `${promptNeg.value},${negative}`;
    const applyStylePrompt = gradioApp().querySelector('#styles_apply_prompt > label > input');
    if (applyStylePrompt.checked === true) {
      if (prompt !== '') {
        if (prompt.includes('{prompt}')) {
          prompt = prompt.replace('{prompt}', orgPrompt);
          promptPos.value = prompt;
          updateInput(promptPos);
        } else {
          promptPos.value = previewPrompt;
          updateInput(promptPos);
        }
      }
    }
    const applyStyleNeg = gradioApp().querySelector('#styles_apply_neg > label > input');
    if (applyStyleNeg.checked === true) {
      if (negative !== '') {
        promptNeg.value = previewNegative;
        updateInput(promptNeg);
      }
    }
    const applyStyleExtra = gradioApp().querySelector('#styles_apply_extra > label > input');
    if (applyStyleExtra.checked === true) {
      try {
        const extrasjson = JSON.parse(extrasToJson(extras));
        try {
          steps.value = extrasjson.Steps;
          updateInput(steps);
        } catch (e) {}
        try {
          CFG.value = extrasjson.scale;
          updateInput(CFG);
        } catch (e) {}
        try {
          Seed.value = extrasjson.Seed;
          updateInput(Seed);
        } catch (e) {}
        try {
          dimensions = extrasjson.Size.split('x');
          const WidthValue = parseInt(dimensions[0], 10);
          width.value = WidthValue;
          updateInput(width);
          const HeightValue = parseInt(dimensions[1], 10);
          height.value = HeightValue;
          updateInput(height);
        } catch (e) {}
        try {
          sampler.value = extrasjson.Sampler;
          updateInput(sampler);
        } catch (e) {}
      } catch (e) {}
    }
  }
}

function hoverPreviewStyleOut() {
  const enablePreview = gradioApp().querySelector('#HoverOverStyle_preview > label > input').checked;
  if (enablePreview === true) {
    const tabname = getENActiveTab();
    const promptPos = gradioApp().querySelector(`#${tabname}_prompt > label > textarea`);
    const promptNeg = gradioApp().querySelector(`#${tabname}_neg_prompt > label > textarea`);
    const steps = gradioApp().querySelector(`#${tabname}_steps > div > div > input`);
    const sampler = gradioApp().querySelector(`#${tabname}_sampling > label > div > div > div > input`);
    const CFG = gradioApp().querySelector(`#${tabname}_cfg_scale > div > div > input`);
    const Seed = gradioApp().querySelector(`#${tabname}_seed > label >input`);
    const width = gradioApp().querySelector(`#${tabname}_width > div > div > input`);
    const height = gradioApp().querySelector(`#${tabname}_height > div > div > input`);
    promptPos.value = orgPrompt;
    promptNeg.value = orgNegative;
    steps.value = orgSteps;
    sampler.value = orgSampler;
    CFG.value = orgCFG;
    Seed.value = orgSeed;
    width.value = orgWidth;
    height.value = orgHeight;
    updateInput(promptPos);
    updateInput(promptNeg);
    updateInput(steps);
    updateInput(sampler);
    updateInput(CFG);
    updateInput(Seed);
    updateInput(width);
    updateInput(height);
    orgPrompt = '';
    orgNegative = '';
    orgSteps = '';
    orgSampler = '';
    orgCFG = '';
    orgSeed = '';
    orgWidth = '';
    orgHeight = '';
  }
}

function extrasToJson(extras) {
  const regex = /(\w+):\s*([^,]+)/g;
  let match;
  const data = {};
  // eslint-disable-next-line no-cond-assign
  while ((match = regex.exec(extras)) !== null) {
    // eslint-disable-next-line prefer-destructuring
    data[match[1]] = match[2];
  }
  const extrasjson = JSON.stringify(data);
  return extrasjson;
}

function applyPrompts(a, b) {
  if (a.value === '') {
    a.value = b;
  } else {
    a.value = `${a.value},${b}`;
  }
  updateInput(a);
}

function applyValues(a, b) {
  a.value = b;
  updateInput(a);
}

function setupStylesTab(tabname, cardcover, sidebarwidth) {
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
    gradioApp().getElementById(`${tabname}_settings`).parentNode.style.width = `${100 - 2 - sidebarwidth}vw`;
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
  const h2tag = gradioApp().querySelector(`#${tabname}_styles_popout > div > div > div > div > div > div > div > h2`);
  const { cardcover } = h2tag.dataset;
  const { sidebarwidth } = h2tag.dataset;
  checkkENAndStyles(sidebarwidth);
  setupStylesTab('txt2img', cardcover, sidebarwidth);
  setupStylesTab('img2img', cardcover, sidebarwidth);
  gradioApp().getElementById('style_save_btn').addEventListener('click', () => { saveRefresh(); });
  gradioApp().getElementById('style_delete_btn').addEventListener('click', () => { deleteRefresh(); });
}

function checkkENAndStyles(sidebarwidth) {
  const tabname = getENActiveTab();
  const txt2imgStylesPopoutEl = document.getElementById(`${tabname}_styles_popout`);
  const txt2imgExtraNetworksEl = document.getElementById(`${tabname}_extra_networks`);
  const areElementsHidden = () => txt2imgStylesPopoutEl.classList.contains('hide') && txt2imgExtraNetworksEl.classList.contains('hide');
  const observer = new MutationObserver((mutationsList, _observer) => {
    const bothElementsHidden = areElementsHidden();
    if (bothElementsHidden) {
      gradioApp().getElementById(`${tabname}_settings`).parentNode.style.width = 'unset';
    } else {
      gradioApp().getElementById(`${tabname}_settings`).parentNode.style.width = `${100 - 2 - sidebarwidth}vw`;
    }
  });

  const observerConfig = {
    attributes: true,
  };

  // Start observing both target elements
  observer.observe(txt2imgStylesPopoutEl, observerConfig);
  observer.observe(txt2imgExtraNetworksEl, observerConfig);
}

onUiLoaded(setupStyles);

// editing styles
function editStyle(title, img, description, prompt, promptNeggative, extra, category, tags, filename, saveFolder) {
  const tabname = getENActiveTab();
  // title
  const editorTitle = gradioApp().querySelector('#style_title_txt > label > textarea');
  applyValues(editorTitle, title);
  // img
  const imgUrlHolderElement = gradioApp().querySelector('#style_img_url_txt > label > textarea');
  applyValues(imgUrlHolderElement, img);
  // applyValues(editor_img, title);
  // description
  const editorDescription = gradioApp().querySelector('#style_description_txt > label > textarea');
  applyValues(editorDescription, description);
  // prompt
  const editorPrompt = gradioApp().querySelector('#style_prompt_txt > label > textarea');
  applyValues(editorPrompt, prompt);
  // promptNeggative
  const editorPromptNeggative = gradioApp().querySelector('#style_negative_txt > label > textarea');
  applyValues(editorPromptNeggative, promptNeggative);
  // extra
  const editorExtra = gradioApp().querySelector('#style_extra_txt > label > textarea');
  applyValues(editorExtra, extra);
  // Category
  const editorCategory = gradioApp().querySelector('#style_category_txt > label > textarea');
  applyValues(editorCategory, category);
  // tags
  const editorTags = gradioApp().querySelector('#style_tags_txt > label > textarea');
  applyValues(editorTags, tags);
  // filename
  const editorFilename = gradioApp().querySelector('#style_filename_txt > label > textarea');
  filename = decodeURIComponent(filename); // Decode the filename
  filename = filename.replace('.json', '');
  applyValues(editorFilename, filename);
  // folder
  saveFolder = decodeURIComponent(saveFolder); // Decode the save folder
  saveFolder = saveFolder.replace('models/styles/', '');
  saveFolder = saveFolder.replace(`/${filename}.json`, '');
  saveFolder = saveFolder.replace(/\\/g, '/');
  const editorSaveFolder = gradioApp().querySelector('#style_savefolder_txt > label > div > div > div > input');
  const editorTempFolder = gradioApp().querySelector('#style_savefolder_temp > label > textarea');
  applyValues(editorTempFolder, saveFolder);
  applyValues(editorSaveFolder, saveFolder);

  // press tab button
  const tabsdiv = gradioApp().getElementById(`${tabname}_styles_popout`);
  function findEditorButton() {
    const buttons = tabsdiv.querySelectorAll('button');
    for (const button of buttons) {
      if (button.innerText === 'Style Editor') {
        return button;
      }
    }
    return null;
  }
  const editorButton = findEditorButton();
  if (editorButton) {
    editorButton.click();
  }
}
function deleteRefresh() {
  const galleryrefresh = gradioApp().querySelector('#style_refresh');
  const stylesclear = gradioApp().querySelector('#style_clear_btn');
  galleryrefresh.click();
  stylesclear.click();
}
function saveRefresh() {
  setTimeout(() => {
    const galleryrefresh = gradioApp().querySelector('#style_refresh');
    galleryrefresh.click();
  }, 1000); // 1000 milliseconds = 1 second
}
function grabLastGeneratedimage() {
  const tabname = getENActiveTab();
  const imagegallery = gradioApp().querySelector(`#${tabname}_gallery`);

  if (imagegallery) {
    const firstImage = imagegallery.querySelector('img');
    if (firstImage) {
      let imageSrc = firstImage.src;
      imageSrc = imageSrc.replace(/.*file=/, '');
      imageSrc = decodeURIComponent(imageSrc); // Decode the URL-encoded file name
      const imgUrlHolderElement = gradioApp().querySelector('#style_img_url_txt > label > textarea');
      applyValues(imgUrlHolderElement, imageSrc);
    }
  }
}
function grabCurrentSettings() {
  // prompt
  const tabname = getENActiveTab();
  const promptPos = gradioApp().querySelector(`#${tabname}_prompt > label > textarea`);
  const editorPrompt = gradioApp().querySelector('#style_prompt_txt > label > textarea');
  applyValues(editorPrompt, promptPos.value);
  // promptNeggative
  const promptNeg = gradioApp().querySelector(`#${tabname}_neg_prompt > label > textarea`);
  const editorPromptNeggative = gradioApp().querySelector('#style_negative_txt > label > textarea');
  applyValues(editorPromptNeggative, promptNeg.value);
  // extra
  const steps = gradioApp().querySelector(`#${tabname}_steps > div > div > input`);
  const sampler = gradioApp().querySelector(`#${tabname}_sampling > label > div > div > div > input`);
  const CFG = gradioApp().querySelector(`#${tabname}_cfg_scale > div > div > input`);
  const Seed = gradioApp().querySelector(`#${tabname}_seed > label >input`);
  const width = gradioApp().querySelector(`#${tabname}_width > div > div > input`);
  const height = gradioApp().querySelector(`#${tabname}_height > div > div > input`);
  const extras = `Steps:${steps.value}, Sampler:${sampler.value}, CFG scale: ${CFG.value}, Seed: ${Seed.value}, Size: ${width.value}x${height.value}`;
  const editorExtra = gradioApp().querySelector('#style_extra_txt > label > textarea');
  applyValues(editorExtra, extras);
}
