let skills = [];

// Executed when the page loads
window.onload = function() {
  try {
    const hidden = document.getElementById('skills-hidden');
    if (hidden && hidden.value) {
      skills = JSON.parse(hidden.value);
      updateSkillsDisplay();
    }
  } catch(e){}
}

// Add a skill
function addSkill() {
  const name = document.getElementById('skill-name').value.trim();
  const desc = document.getElementById('skill-desc').value.trim();

  if(name && desc) {
    if (skills.length >= 6) {
      alert("You cannot add more than 6 skills.");
      return;
    }

    skills.push({name, desc});
    updateSkillsDisplay();

    document.getElementById('skill-name').value = '';
    document.getElementById('skill-desc').value = '';
    document.getElementById('skills-hidden').value = JSON.stringify(skills);
  }
}

// Update the display
function updateSkillsDisplay() {
  const list = document.getElementById('skills-list');
  list.innerHTML = '';

  skills.forEach((s, i) => {
    list.innerHTML += `
      <div>
        ${s.name} : ${s.desc} 
        <button type="button" onclick="removeSkill(${i})">❌</button>
      </div>`;
  });

  document.getElementById('skills-hidden').value = JSON.stringify(skills);
}

// Remove a skill
function removeSkill(index) {
  skills.splice(index, 1);
  updateSkillsDisplay();
  document.getElementById('skills-hidden').value = JSON.stringify(skills);
}

// JSON Import
window.loadSkillsFromJSON = function(newSkills) {
  if (!Array.isArray(newSkills)) return;
  skills = [];
  for (let i = 0; i < newSkills.length && skills.length < 6; i++) {
    const s = newSkills[i];
    if (s.name && s.desc) {
      skills.push({
        name: String(s.name).trim().slice(0, 30),
        desc: String(s.desc).trim().slice(0, 200)
      });
    }
  }
  updateSkillsDisplay();
};
