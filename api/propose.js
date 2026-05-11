const { neon } = require('@neondatabase/serverless');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { mot, phonetique, categorie, definition, exemple, traduction_exemple, tags, contributeur } = req.body || {};

  if (!mot || !mot.trim()) return res.status(400).json({ error: 'Le mot est obligatoire.' });
  if (!definition || !definition.trim()) return res.status(400).json({ error: 'La définition est obligatoire.' });

  try {
    const sql = neon(process.env.DATABASE_URL);
    const tagsArray = tags ? tags.split(',').map(t => t.trim()).filter(Boolean) : [];

    await sql`
      INSERT INTO mots (mot, phonetique, categorie, definition, exemple, traduction_exemple, tags, contributeur, statut)
      VALUES (
        ${mot.trim().toLowerCase()},
        ${phonetique?.trim() || null},
        ${categorie || 'nom'},
        ${definition.trim()},
        ${exemple?.trim() || null},
        ${traduction_exemple?.trim() || null},
        ${tagsArray},
        ${contributeur?.trim() || 'anonyme'},
        'en_attente'
      )
    `;
    res.status(201).json({ message: 'Merci ! Ton mot a été soumis et sera publié après validation.' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Erreur serveur, réessaie plus tard.' });
  }
};
