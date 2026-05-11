require('dotenv').config();
const { neon } = require('@neondatabase/serverless');
const fs = require('fs');

const words = JSON.parse(fs.readFileSync('./dictionary.json', 'utf8'));

async function seed() {
  const sql = neon(process.env.DATABASE_URL);

  // Create table
  await sql`
    CREATE TABLE IF NOT EXISTS mots (
      id            SERIAL PRIMARY KEY,
      mot           VARCHAR(200)  NOT NULL,
      phonetique    VARCHAR(200),
      categorie     VARCHAR(100),
      definition    TEXT          NOT NULL,
      exemple       TEXT,
      traduction_exemple TEXT,
      tags          TEXT[]        DEFAULT '{}',
      contributeur  VARCHAR(200)  DEFAULT 'anonyme',
      statut        VARCHAR(20)   NOT NULL DEFAULT 'en_attente',
      created_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW()
    )
  `;
  await sql`CREATE INDEX IF NOT EXISTS mots_statut_idx ON mots(statut)`;
  await sql`CREATE INDEX IF NOT EXISTS mots_mot_idx ON mots(mot)`;

  console.log('Table créée.');

  for (const w of words) {
    await sql`
      INSERT INTO mots (mot, phonetique, categorie, definition, exemple, traduction_exemple, tags, contributeur, statut)
      VALUES (
        ${w.mot}, ${w.phonetique || null}, ${w.categorie || 'nom'},
        ${w.definition}, ${w.exemple || null}, ${w.traduction_exemple || null},
        ${w.tags || []}, ${w.contributeur || 'équipe Dico Nouchi'}, 'publié'
      )
      ON CONFLICT DO NOTHING
    `;
    console.log(`  ✓ ${w.mot}`);
  }

  console.log(`\nSeed terminé — ${words.length} mots insérés.`);
}

seed().catch(err => { console.error(err); process.exit(1); });
