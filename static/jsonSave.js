// Get the form data
function getFormData() {
  const form = document.getElementById('charForm');
  return {
    name: form.name.value,
    age: form.age.value,
    gender: form.gender.value,
    race: form.race.value,
    hp: form.hp.value,
    dmg: form.dmg.value,
    descP: form.descP.value,
    descH: form.descH.value,
    skills: form['skills-hidden'].value,
    background_filename: form.background_filename.value,
    avatar_filename: form.avatar_filename.value
  };
}

// Load the form data
function setFormData(data) {
  const form = document.getElementById('charForm');
  if ('name' in data) form.name.value = data.name;
  if ('age' in data) form.age.value = data.age;
  if ('gender' in data) form.gender.value = data.gender;
  if ('race' in data) form.race.value = data.race;
  if ('hp' in data) form.hp.value = data.hp;
  if ('dmg' in data) form.dmg.value = data.dmg;
  if ('descP' in data) form.descP.value = data.descP;
  if ('descH' in data) form.descH.value = data.descH;
  if ('skills' in data) {
    try {
      const skills = JSON.parse(data.skills);
      if (typeof window.loadSkillsFromJSON === 'function') {
        window.loadSkillsFromJSON(skills);
      } else {
        form['skills-hidden'].value = data.skills;
      }
    } catch (e) {
      form['skills-hidden'].value = data.skills;
    }
  }
  if ('background_filename' in data) form.background_filename.value = data.background_filename;
  if ('avatar_filename' in data) form.avatar_filename.value = data.avatar_filename;
}

// Save as JSON
function saveFormAsJSON() {
  const data = getFormData();
  const blob = new Blob([JSON.stringify(data, null, 2)], {type: "application/json"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = (data.name ? data.name.replace(/\s+/g,'_') : "sheet") + ".json";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Load from JSON
function loadFormFromJSON(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const data = JSON.parse(e.target.result);
      setFormData(data);
    } catch (err) {
      alert("Invalid JSON file.");
    }
  };
  reader.readAsText(file);
}

window.setFormData = setFormData;
window.getFormData = getFormData;
