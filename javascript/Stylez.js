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



