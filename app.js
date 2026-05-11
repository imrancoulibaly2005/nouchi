let allWords = [];
let filtered = [];
let activeAlpha = 'all';
let activeCat = 'all';
let searchQuery = '';

async function loadDictionary() {
  const res = await fetch('/api/words');
  if (!res.ok) throw new Error('Erreur chargement');
  allWords = await res.json();
  allWords.sort((a, b) => a.mot.localeCompare(b.mot, 'fr'));
  buildAlphaFilter();
  buildCatFilter();
  applyFilters();
  updateStats();
}

function buildAlphaFilter() {
  const letters = ['all', ...new Set(allWords.map(w => w.mot[0].toUpperCase()))].sort((a, b) => {
    if (a === 'all') return -1;
    if (b === 'all') return 1;
    return a.localeCompare(b);
  });
  const container = document.getElementById('alphaFilter');
  container.innerHTML = letters.map(l => `
    <button class="alpha-btn ${l === 'all' ? 'all' : ''} ${activeAlpha === l ? 'active' : ''}"
            data-letter="${l}">${l === 'all' ? 'Tous' : l}</button>
  `).join('');
  container.querySelectorAll('.alpha-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      activeAlpha = btn.dataset.letter;
      container.querySelectorAll('.alpha-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      applyFilters();
    });
  });
}

function buildCatFilter() {
  const cats = ['all', ...new Set(allWords.flatMap(w => w.tags || []))].filter(Boolean);
  const container = document.getElementById('catFilter');
  container.innerHTML = `<span class="cat-label">Tags :</span>` + cats.map(c => `
    <button class="cat-btn ${activeCat === c ? 'active' : ''}" data-cat="${c}">
      ${c === 'all' ? '🗂 Tous' : c}
    </button>
  `).join('');
  container.querySelectorAll('.cat-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      activeCat = btn.dataset.cat;
      container.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      applyFilters();
    });
  });
}

function applyFilters() {
  const q = searchQuery.toLowerCase().trim();
  filtered = allWords.filter(w => {
    const matchAlpha = activeAlpha === 'all' || w.mot[0].toUpperCase() === activeAlpha;
    const matchCat = activeCat === 'all' || (w.tags && w.tags.includes(activeCat));
    const matchSearch = !q ||
      w.mot.toLowerCase().includes(q) ||
      w.definition.toLowerCase().includes(q) ||
      (w.exemple && w.exemple.toLowerCase().includes(q)) ||
      (w.tags && w.tags.some(t => t.toLowerCase().includes(q)));
    return matchAlpha && matchCat && matchSearch;
  });
  renderWords();
  updateStats();
}

function renderWords() {
  const grid = document.getElementById('wordGrid');
  const noResult = document.getElementById('noResult');
  if (filtered.length === 0) {
    grid.innerHTML = '';
    noResult.classList.remove('hidden');
    return;
  }
  noResult.classList.add('hidden');
  grid.innerHTML = filtered.map(w => `
    <article class="word-card" data-id="${w.id}" tabindex="0" role="button" aria-label="Voir le mot ${w.mot}">
      <div class="card-word">${highlight(w.mot, searchQuery)}</div>
      ${w.phonetique ? `<div class="card-phonetic">/${w.phonetique}/</div>` : ''}
      <div class="card-cat">${w.categorie}</div>
      <div class="card-def">${highlight(w.definition, searchQuery)}</div>
      ${w.exemple ? `<div class="card-example">"${w.exemple}"</div>` : ''}
      <div class="card-tags">${(w.tags || []).map(t => `<span class="tag">${t}</span>`).join('')}</div>
    </article>
  `).join('');

  grid.querySelectorAll('.word-card').forEach(card => {
    card.addEventListener('click', () => openModal(parseInt(card.dataset.id)));
    card.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') openModal(parseInt(card.dataset.id)); });
  });
}

function highlight(text, query) {
  if (!query) return text;
  const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return text.replace(new RegExp(`(${escaped})`, 'gi'), '<mark>$1</mark>');
}

function updateStats() {
  const total = allWords.length;
  const shown = filtered.length;
  const bar = document.getElementById('statsBar');
  if (searchQuery || activeAlpha !== 'all' || activeCat !== 'all') {
    bar.textContent = `${shown} mot${shown > 1 ? 's' : ''} trouvé${shown > 1 ? 's' : ''} sur ${total}`;
  } else {
    bar.textContent = `${total} mots dans le dictionnaire — et ça grandit grâce à vous !`;
  }
}

function openModal(id) {
  const w = allWords.find(x => x.id === id);
  if (!w) return;
  const content = document.getElementById('modalContent');
  content.innerHTML = `
    <div class="modal-word">${w.mot}</div>
    ${w.phonetique ? `<div class="modal-phonetic">/${w.phonetique}/</div>` : ''}
    <div class="modal-cat">${w.categorie}</div>
    <div class="modal-section">
      <div class="modal-label">Définition</div>
      <div class="modal-def">${w.definition}</div>
    </div>
    ${w.exemple ? `
    <div class="modal-section">
      <div class="modal-label">Exemple</div>
      <div class="modal-ex">"${w.exemple}"</div>
      ${w.traduction_exemple ? `<div class="modal-ex-tr">→ ${w.traduction_exemple}</div>` : ''}
    </div>` : ''}
    ${w.tags && w.tags.length ? `
    <div class="modal-section">
      <div class="modal-label">Tags</div>
      <div class="modal-tags">${w.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
    </div>` : ''}
    <div class="modal-contrib">Contribué par : ${w.contributeur || 'communauté'}</div>
  `;
  document.getElementById('modalOverlay').classList.remove('hidden');
  document.getElementById('modalClose').focus();
}

function closeModal() {
  document.getElementById('modalOverlay').classList.add('hidden');
}

// ===== PROPOSE FORM =====
async function handlePropose(e) {
  e.preventDefault();
  const form = e.target;
  const btn = document.getElementById('submitBtn');
  const msg = document.getElementById('formMsg');

  btn.disabled = true;
  btn.textContent = 'Envoi en cours...';
  msg.className = 'form-msg hidden';

  const data = Object.fromEntries(new FormData(form).entries());

  try {
    const res = await fetch('/api/propose', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const json = await res.json();
    if (res.ok) {
      msg.className = 'form-msg success';
      msg.textContent = json.message;
      form.reset();
    } else {
      msg.className = 'form-msg error';
      msg.textContent = json.error || 'Une erreur est survenue.';
    }
  } catch {
    msg.className = 'form-msg error';
    msg.textContent = 'Impossible de contacter le serveur.';
  } finally {
    btn.disabled = false;
    btn.textContent = 'Envoyer ma proposition';
    msg.classList.remove('hidden');
    msg.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

// ===== INIT EVENTS =====
document.addEventListener('DOMContentLoaded', () => {
  loadDictionary();

  const searchInput = document.getElementById('searchInput');
  const clearBtn = document.getElementById('clearBtn');

  searchInput.addEventListener('input', () => {
    searchQuery = searchInput.value;
    clearBtn.style.display = searchQuery ? 'flex' : 'none';
    applyFilters();
  });

  clearBtn.style.display = 'none';
  clearBtn.addEventListener('click', () => {
    searchInput.value = '';
    searchQuery = '';
    clearBtn.style.display = 'none';
    searchInput.focus();
    applyFilters();
  });

  document.getElementById('proposeForm').addEventListener('submit', handlePropose);

  document.getElementById('modalClose').addEventListener('click', closeModal);
  document.getElementById('modalOverlay').addEventListener('click', e => {
    if (e.target === e.currentTarget) closeModal();
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
});
