# 🇨🇮 Dico Nouchi — Dictionnaire Participatif Nouchi-Français

Le **Dico Nouchi** est un dictionnaire communautaire et open source du **nouchi**, le parler populaire d'Abidjan. Il est accessible en ligne via GitHub Pages et tout le monde peut y contribuer !

## 🌐 Voir le dictionnaire en ligne

👉 **[imrancoulibaly2005.github.io/nouchi](https://imrancoulibaly2005.github.io/nouchi)**

## ✨ Fonctionnalités

- 🔍 Recherche instantanée par mot ou définition
- 🔤 Filtre alphabétique
- 🏷️ Filtre par catégorie / tag
- 📖 Fiche détaillée avec exemples et traductions
- 📱 100% responsive (mobile et desktop)
- 🤝 Contribution ouverte à tous via GitHub

## 🤝 Comment contribuer ?

### Option 1 — Proposer un mot (facile, sans code)

1. Va sur [Issues > Nouveau mot](https://github.com/imrancoulibaly2005/nouchi/issues/new?template=nouveau-mot.md)
2. Remplis le formulaire avec le mot, sa définition et un exemple
3. Soumet l'issue — ton mot sera ajouté après vérification !

### Option 2 — Pull Request (pour ceux qui connaissent GitHub)

1. Fork ce dépôt
2. Ajoute ton mot dans `dictionary.json` en respectant le format
3. Crée une Pull Request

👉 [Lire le guide complet de contribution](CONTRIBUTING.md)

## 📁 Structure du projet

```
nouchi/
├── index.html          # Page principale du site
├── style.css           # Styles (design)
├── app.js              # Logique de recherche et filtres
├── dictionary.json     # Les mots du dictionnaire
├── CONTRIBUTING.md     # Guide de contribution
└── .github/
    └── ISSUE_TEMPLATE/
        ├── nouveau-mot.md   # Template : proposer un mot
        └── correction.md    # Template : signaler une erreur
```

## 📝 Format d'une entrée

```json
{
  "id": 26,
  "mot": "exemple",
  "phonetique": "eg-zam-ple",
  "categorie": "nom",
  "definition": "Signification du mot en français",
  "exemple": "Phrase exemple en nouchi.",
  "traduction_exemple": "Traduction de la phrase en français.",
  "tags": ["courant", "finance"],
  "contributeur": "Ton pseudo GitHub"
}
```

### Catégories disponibles

| Catégorie | Description |
|-----------|-------------|
| `nom` | Nom commun |
| `verbe` | Verbe d'action |
| `adjectif` | Qualificatif |
| `interjection` | Exclamation |
| `expression` | Locution ou phrase figée |
| `nom / verbe` | Mot à double fonction |

### Tags disponibles

`courant` · `finance` · `nourriture` · `transport` · `personnes` · `relations` · `musique` · `culture` · `compliment` · `expression` · `solidarité` · `problème` · `mouvement` · `commerce` · `restauration` · `sortie` · `familier` · `interjection` · `sensation` · `état` · `dioula` · `cadeau`

## 📜 Licence

Ce projet est open source sous licence [MIT](LICENSE). Les contributions appartiennent à leurs auteurs respectifs.

---

*Fait avec ❤️ pour la culture ivoirienne — On est ensemble !*
