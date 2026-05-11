require('dotenv').config();
const { neon } = require('@neondatabase/serverless');
const words = require('./dictionary.json');

async function reseed() {
  const sql = neon(process.env.DATABASE_URL);

  await sql`TRUNCATE TABLE mots RESTART IDENTITY`;
  console.log('Table vidée.');

  let ok = 0, fail = 0;
  for (const w of words) {
    try {
      await sql`
        INSERT INTO mots
          (mot, francais, phonetique, categorie, definition, exemple, traduction_exemple, tags, contributeur, statut)
        VALUES (
          ${w.mot}, ${w.francais || null}, ${w.phonetique || null}, ${w.categorie || 'nom'},
          ${w.definition}, ${w.exemple || null}, ${w.traduction_exemple || null},
          ${w.tags || []}, ${w.contributeur || 'équipe Dico Nouchi'}, 'publié'
        )
      `;
      ok++;
    } catch (e) {
      console.error(`  ERREUR ${w.mot}: ${e.message}`);
      fail++;
    }
  }
  console.log(`Reseed termine: ${ok} inseres, ${fail} erreurs.`);
}

reseed().catch(e => { console.error(e); process.exit(1); });
