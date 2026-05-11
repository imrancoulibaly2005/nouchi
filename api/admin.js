const { neon } = require('@neondatabase/serverless');

// GET  /api/admin?secret=XXX          → liste les mots en attente
// POST /api/admin?secret=XXX&id=N&action=approuver|rejeter
module.exports = async function handler(req, res) {
  if (req.query.secret !== process.env.ADMIN_SECRET) {
    return res.status(401).json({ error: 'Non autorisé' });
  }

  const sql = neon(process.env.DATABASE_URL);

  if (req.method === 'GET') {
    const mots = await sql`SELECT * FROM mots WHERE statut = 'en_attente' ORDER BY created_at ASC`;
    return res.json(mots);
  }

  if (req.method === 'POST') {
    const { id, action } = req.query;
    const statut = action === 'approuver' ? 'publié' : 'rejeté';
    await sql`UPDATE mots SET statut = ${statut} WHERE id = ${id}`;
    return res.json({ message: `Mot ${statut}.` });
  }

  res.status(405).json({ error: 'Method not allowed' });
};
