let competences = [];

// Exécutée au chargement de la page
window.onload = function() {
  try {
    const hidden = document.getElementById('competences-hidden');
    if (hidden && hidden.value) {
      competences = JSON.parse(hidden.value);
      updateCompetencesDisplay();
    }
  } catch(e){}
}

// Ajouter une compétence
function addCompetence() {
  const nom = document.getElementById('comp-nom').value.trim();
  const desc = document.getElementById('comp-desc').value.trim();

  if(nom && desc) {
    if (competences.length >= 6) {
      alert("Vous ne pouvez pas ajouter plus de 6 compétences.");
      return;
    }

    competences.push({nom, desc});
    updateCompetencesDisplay();

    document.getElementById('comp-nom').value = '';
    document.getElementById('comp-desc').value = '';
    document.getElementById('competences-hidden').value = JSON.stringify(competences);
  }
}

// Mise à jour de l'affichage
function updateCompetencesDisplay() {
  const list = document.getElementById('competences-list');
  list.innerHTML = '';

  competences.forEach((c, i) => {
    list.innerHTML += `
    <div class="mb-2">
      ${c.nom} : ${c.desc}
      <button type="button"
              onclick="removeCompetence(${i})"
              class="btn btn-light px-4 py-1">
        ❌
      </button>
    </div>`
  });

  document.getElementById('competences-hidden').value = JSON.stringify(competences);
}

// Supprimer une compétence
function removeCompetence(index) {
  competences.splice(index, 1);
  updateCompetencesDisplay();
  document.getElementById('competences-hidden').value = JSON.stringify(competences);
}

// Importation JSON
window.loadCompetencesFromJSON = function(newCompetences) {
  if (!Array.isArray(newCompetences)) return;
  competences = [];
  for (let i = 0; i < newCompetences.length && competences.length < 6; i++) {
    const c = newCompetences[i];
    if (c.nom && c.desc) {
      competences.push({
        nom: String(c.nom).trim().slice(0, 30),
        desc: String(c.desc).trim().slice(0, 200)
      });
    }
  }
  updateCompetencesDisplay();
};
