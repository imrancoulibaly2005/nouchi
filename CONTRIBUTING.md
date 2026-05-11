# Guide de contribution — Dico Nouchi

Merci de vouloir contribuer ! Ce guide explique comment ajouter un mot, corriger une erreur ou améliorer le projet.

## 🗣 Ajouter un mot sans connaître GitHub

Si tu ne connais pas GitHub, pas de problème :

1. Clique sur ce lien : [Proposer un mot](https://github.com/imrancoulibaly2005/nouchi/issues/new?template=nouveau-mot.md)
2. Connecte-toi (ou crée un compte GitHub gratuit)
3. Remplis le formulaire et clique sur **"Submit new issue"**
4. Un modérateur traitera ta demande sous 48h

## 🛠 Ajouter un mot via Pull Request

### 1. Fork le dépôt

Clique sur **Fork** en haut à droite de la page GitHub.

### 2. Clone ton fork

```bash
git clone https://github.com/TON-PSEUDO/nouchi.git
cd nouchi
```

### 3. Ajoute ton mot dans `dictionary.json`

Ouvre `dictionary.json` et ajoute une entrée à la fin du tableau (avant le `]` final).  
Utilise l'`id` suivant disponible et respecte ce format :

```json
{
  "id": 26,
  "mot": "le mot en nouchi",
  "phonetique": "prononciation",
  "categorie": "nom",
  "definition": "Définition claire en français",
  "exemple": "Phrase exemple en nouchi.",
  "traduction_exemple": "Traduction de la phrase en français.",
  "tags": ["courant"],
  "contributeur": "ton-pseudo-github"
}
```

### 4. Commit et Push

```bash
git add dictionary.json
git commit -m "feat: ajouter le mot 'exemple'"
git push
```

### 5. Ouvre une Pull Request

Va sur la page de ton fork sur GitHub et clique sur **"Compare & pull request"**.

---

## ✅ Règles de qualité

- Le mot doit être réellement utilisé en nouchi / en Côte d'Ivoire
- La définition doit être claire et en bon français
- L'exemple doit être une vraie phrase (pas juste un mot isolé)
- Pas de contenu offensant, discriminatoire ou vulgaire sans contexte culturel clair
- Un seul mot par issue / PR

## 🚫 Ce qu'on n'accepte pas

- Les inventions personnelles sans usage réel
- Les définitions copiées sans source
- Les mots en doublon (vérifie d'abord que le mot n'existe pas déjà)

---

*Merci pour ta contribution — On est ensemble !* 🇨🇮
