const { neon } = require('@neondatabase/serverless');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const sql = neon(process.env.DATABASE_URL);
    const mots = await sql`
      SELECT id, mot, phonetique, categorie, definition, exemple, traduction_exemple, tags, contributeur
      FROM mots
      WHERE statut = 'publié'
      ORDER BY mot ASC
    `;
    res.setHeader('Cache-Control', 's-maxage=30, stale-while-revalidate=120');
    res.json(mots);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Erreur serveur' });
  }
};
