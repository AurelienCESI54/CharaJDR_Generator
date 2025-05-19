// Obtenir les informations
function getFormData() {
  const form = document.getElementById('charForm');
  return {
    nom: form.nom.value,
    age: form.age.value,
    sexe: form.sexe.value,
    race: form.race.value,
    pv: form.pv.value,
    pd: form.pd.value,
    descP: form.descP.value,
    descH: form.descH.value,
    competences: form['competences-hidden'].value,
    background_filename: form.background_filename.value,
    avatar_filename: form.avatar_filename.value
  };
}

// Charger les informations
function setFormData(data) {
  const form = document.getElementById('charForm');
  if ('nom' in data) form.nom.value = data.nom;
  if ('age' in data) form.age.value = data.age;
  if ('sexe' in data) form.sexe.value = data.sexe;
  if ('race' in data) form.race.value = data.race;
  if ('pv' in data) form.pv.value = data.pv;
  if ('pd' in data) form.pd.value = data.pd;
  if ('descP' in data) form.descP.value = data.descP;
  if ('descH' in data) form.descH.value = data.descH;
  if ('competences' in data) {
    try {
      const competences = JSON.parse(data.competences);
      if (typeof window.loadCompetencesFromJSON === 'function') {
        window.loadCompetencesFromJSON(competences);
      } else {
        form['competences-hidden'].value = data.competences;
      }
    } catch (e) {
      form['competences-hidden'].value = data.competences;
    }
  }
  if ('background_filename' in data) form.background_filename.value = data.background_filename;
  if ('avatar_filename' in data) form.avatar_filename.value = data.avatar_filename;
}

// Sauvegarde en JSON
function saveFormAsJSON() {
  const data = getFormData();
  const blob = new Blob([JSON.stringify(data, null, 2)], {type: "application/json"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = (data.nom ? data.nom.replace(/\s+/g,'_') : "fiche") + ".json";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Charger le JSON
function loadFormFromJSON(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const data = JSON.parse(e.target.result);
      setFormData(data);
    } catch (err) {
      alert("Fichier JSON invalide.");
    }
  };
  reader.readAsText(file);
}

window.setFormData = setFormData;
window.getFormData = getFormData;
