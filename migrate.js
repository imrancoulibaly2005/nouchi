require('dotenv').config();
const { neon } = require('@neondatabase/serverless');
const words = require('./dictionary.json');

async function migrate() {
  const sql = neon(process.env.DATABASE_URL);

  // Add francais column if missing
  await sql`ALTER TABLE mots ADD COLUMN IF NOT EXISTS francais VARCHAR(200)`;
  console.log('Colonne francais ajoutée.');

  // Update existing rows with francais field
  for (const w of words) {
    if (!w.francais) continue;
    await sql`UPDATE mots SET francais = ${w.francais} WHERE mot = ${w.mot}`;
  }
  console.log('Mots existants mis à jour avec leur traduction française.');

  // Insert new words (id > 25)
  const newWords = words.filter(w => w.id > 25);
  for (const w of newWords) {
    const exists = await sql`SELECT id FROM mots WHERE mot = ${w.mot}`;
    if (exists.length > 0) { console.log(`  = ${w.mot} (déjà présent)`); continue; }
    await sql`
      INSERT INTO mots (mot, francais, phonetique, categorie, definition, exemple, traduction_exemple, tags, contributeur, statut)
      VALUES (
        ${w.mot}, ${w.francais || null}, ${w.phonetique || null}, ${w.categorie || 'nom'},
        ${w.definition}, ${w.exemple || null}, ${w.traduction_exemple || null},
        ${w.tags || []}, ${w.contributeur || 'équipe Dico Nouchi'}, 'publié'
      )
    `;
    console.log(`  + ${w.mot} → ${w.francais}`);
  }

  console.log(`\nMigration terminée — ${newWords.length} nouveaux mots ajoutés.`);
}

migrate().catch(err => { console.error(err); process.exit(1); });
