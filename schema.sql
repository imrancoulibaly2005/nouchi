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
);

CREATE INDEX IF NOT EXISTS mots_statut_idx ON mots(statut);
CREATE INDEX IF NOT EXISTS mots_mot_idx    ON mots(mot);
