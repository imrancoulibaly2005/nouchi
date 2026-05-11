"""
Construit dictionary.json final en combinant :
 1. Les 121 mots fournis par l'utilisateur (priorité absolue)
 2. Les mots supplémentaires scrappés depuis nouchi.com qui ont
    une vraie définition en français (pas juste un synonyme nouchi)
"""
import json, re, unicodedata

# ── 121 mots utilisateur ──────────────────────────────────────────────────────
USER_WORDS = [
  {"mot":"agboloh","francais":"muscles, musclé","categorie":"nom","definition":"Muscles, musculature, quelqu'un de musclé","tags":["corps","courant"]},
  {"mot":"agnon","francais":"habits, vêtements","categorie":"nom","definition":"Habits, vêtements, tenue vestimentaire","tags":["vêtements","courant"]},
  {"mot":"apoutchou","francais":"femme pulpeuse aux grosses fesses","categorie":"nom","definition":"Belle jeune femme pulpeuse et callipyge, aux formes généreuses","tags":["corps","personnes","courant"]},
  {"mot":"badrô","francais":"boire","categorie":"verbe","definition":"Boire, consommer une boisson","tags":["boisson","courant"]},
  {"mot":"chier","francais":"crier, réprimander","categorie":"verbe","definition":"Crier sur quelqu'un, le réprimander, le gronder","tags":["courant"]},
  {"mot":"banger","francais":"feu d'artifice","categorie":"nom","definition":"Feu d'artifice. Éclater les bangers : tirer les feux d'artifice","tags":["fête","courant"]},
  {"mot":"barre","francais":"1 000 FCFA","categorie":"nom","definition":"Mille (1 000) francs CFA","tags":["finance","courant"]},
  {"mot":"bédou","francais":"portefeuille, porte-monnaie","categorie":"nom","definition":"Portefeuille, porte-monnaie","tags":["finance","courant"]},
  {"mot":"béou","francais":"fuir, aller","categorie":"verbe","definition":"Fuir, partir rapidement, aller quelque part","tags":["mouvement","courant"]},
  {"mot":"beko","francais":"baiser, bisou","categorie":"nom","definition":"Un baiser, un bisou","tags":["amour","courant"]},
  {"mot":"bengué","francais":"Europe","categorie":"nom","definition":"L'Europe, les pays européens","tags":["géographie","courant"]},
  {"mot":"bigo","francais":"œuf, téléphone","categorie":"nom","definition":"Œuf (nourriture) ou téléphone portable selon le contexte","tags":["courant","nourriture"]},
  {"mot":"binguiste","francais":"quelqu'un qui vient d'Europe","categorie":"nom","definition":"Personne qui vient d'Europe ou de France, expatrié","tags":["personnes","géographie","courant"]},
  {"mot":"bobara-ba","francais":"postérieur généreux","categorie":"nom","definition":"Postérieur généreux, grosses fesses","tags":["corps","courant"]},
  {"mot":"bobara-fitini","francais":"postérieur fin","categorie":"nom","definition":"Postérieur fin, petites fesses","tags":["corps","courant"]},
  {"mot":"borlaï","francais":"ignorant","categorie":"adjectif","definition":"Ignorant, personne qui ne comprend rien","tags":["personnes","courant"]},
  {"mot":"bôrô","francais":"beaucoup, fan, sac","categorie":"nom / adverbe","definition":"Beaucoup ; fan, admirateur ; sac selon le contexte","tags":["courant"]},
  {"mot":"bôtchô","francais":"fesses","categorie":"nom","definition":"Fesses, postérieur","tags":["corps","courant"]},
  {"mot":"brobro","francais":"chercher, travailler dur","categorie":"verbe","definition":"Chercher, travailler dur, se démener","tags":["travail","courant"]},
  {"mot":"brobroli","francais":"travail, job","categorie":"nom","definition":"Travail, job, boulot","tags":["travail","courant"]},
  {"mot":"bourou","francais":"pain","categorie":"nom","definition":"Pain (nourriture)","tags":["nourriture","courant"]},
  {"mot":"broutage","francais":"arnaque internet","categorie":"nom","definition":"Arnaque sur internet, escroquerie en ligne","tags":["internet","arnaque","courant"]},
  {"mot":"brouteur","francais":"arnaqueur internet","categorie":"nom","definition":"Arnaqueur sur internet, cybercriminel spécialisé dans les escroqueries en ligne","tags":["internet","arnaque","courant"]},
  {"mot":"cargo","francais":"fourgon de police","categorie":"nom","definition":"Fourgon de police, panier à salade","tags":["police","courant"]},
  {"mot":"côcô","francais":"quémander","categorie":"verbe","definition":"Quémander, mendier, demander sans cesse","tags":["courant"]},
  {"mot":"côcôta","francais":"coup sur la tête","categorie":"nom","definition":"Coup donné sur la tête","tags":["violence","courant"]},
  {"mot":"cohan","francais":"comme ça","categorie":"adverbe","definition":"Comme ça, ainsi, de cette manière","tags":["courant"]},
  {"mot":"daba","francais":"manger, frapper","categorie":"verbe","definition":"Manger ; ou frapper quelqu'un selon le contexte","tags":["nourriture","violence","courant"]},
  {"mot":"dabali","francais":"nourriture, repas","categorie":"nom","definition":"Nourriture, repas ; ou action de frapper","tags":["nourriture","courant"]},
  {"mot":"dédja","francais":"ouvert, blessé","categorie":"adjectif / verbe","definition":"Ouvert, ouvrir ; blessé, qui saigne","tags":["courant"]},
  {"mot":"dendjô","francais":"comprendre, déshabiller","categorie":"verbe","definition":"Comprendre, piger ; ou déshabiller quelqu'un","tags":["courant"]},
  {"mot":"dja","francais":"tuer","categorie":"verbe","definition":"Tuer, éliminer","tags":["violence","courant"]},
  {"mot":"djafoule","francais":"tout donner, impressionner","categorie":"verbe","definition":"Tout donner, impressionner, mettre le paquet","tags":["courant"]},
  {"mot":"djandjou","francais":"personne aux mœurs légères","categorie":"nom","definition":"Personne aux mœurs légères, de mauvaise réputation","tags":["personnes","familier"]},
  {"mot":"djanterman","francais":"homme stylé","categorie":"nom","definition":"Homme stylé, bien habillé, classe","tags":["personnes","mode","courant"]},
  {"mot":"djantra","francais":"prostituée","categorie":"nom","definition":"Prostituée","tags":["personnes","vulgaire"]},
  {"mot":"djossi","francais":"travail, taf","categorie":"nom","definition":"Travail, boulot, taf","tags":["travail","courant"]},
  {"mot":"dindin","francais":"regarder, surveiller","categorie":"verbe","definition":"Regarder, lorgner, surveiller, hésiter","tags":["courant"]},
  {"mot":"djê","francais":"argent","categorie":"nom","definition":"L'argent, la monnaie","tags":["finance","courant"]},
  {"mot":"dôhi","francais":"mensonge","categorie":"nom","definition":"Mensonge, mensonger","tags":["courant"]},
  {"mot":"enjailler","francais":"s'amuser, plaire","categorie":"verbe","definition":"S'amuser, faire la fête, plaire à quelqu'un","tags":["fête","courant"]},
  {"mot":"enjaillement","francais":"amusement, fête","categorie":"nom","definition":"Amusement, fête, bonne ambiance","tags":["fête","courant"]},
  {"mot":"fal","francais":"cigarette","categorie":"nom","definition":"Cigarette","tags":["courant"]},
  {"mot":"faler","francais":"fumer","categorie":"verbe","definition":"Fumer une cigarette","tags":["courant"]},
  {"mot":"fangan","francais":"force","categorie":"nom","definition":"Force, puissance, énergie","tags":["courant"]},
  {"mot":"fongnon","francais":"se positionner pour se battre, frimer","categorie":"verbe","definition":"Se positionner pour se battre ; frimer, faire le fier","tags":["violence","courant"]},
  {"mot":"fata","francais":"tomber, vendre","categorie":"verbe","definition":"Tomber ; ou vendre quelque chose","tags":["courant"]},
  {"mot":"fatali","francais":"chute","categorie":"nom","definition":"Chute, fait de tomber","tags":["courant"]},
  {"mot":"faux-type","francais":"hypocrite, malhonnête","categorie":"nom / adjectif","definition":"Personne hypocrite, malhonnête, qui fait semblant","tags":["personnes","courant"]},
  {"mot":"fiengal","francais":"maigrichon","categorie":"adjectif","definition":"Maigrichon, très maigre","tags":["corps","courant"]},
  {"mot":"foul","francais":"plein, beaucoup","categorie":"adjectif","definition":"Plein, beaucoup, en grande quantité","tags":["courant"]},
  {"mot":"frapper ahoco","francais":"se masturber","categorie":"expression","definition":"Se masturber (expression vulgaire)","tags":["vulgaire","adulte"]},
  {"mot":"fraya","francais":"fuir, s'échapper","categorie":"verbe","definition":"Fuir, s'échapper rapidement","tags":["mouvement","courant"]},
  {"mot":"flôcô","francais":"mentir, mensonge","categorie":"verbe / nom","definition":"Mentir ; mensonge, histoire inventée","tags":["courant"]},
  {"mot":"fraichnie","francais":"petite amie, demoiselle","categorie":"nom","definition":"Petite amie, jeune femme, demoiselle","tags":["personnes","relations","courant"]},
  {"mot":"gaou","francais":"ignorant, pas branché","categorie":"nom / adjectif","definition":"Personne ignorante, naïve, pas au courant des tendances","tags":["personnes","courant"]},
  {"mot":"gawa","francais":"ringard","categorie":"adjectif","definition":"Ringard, démodé, qui n'est pas dans la tendance","tags":["personnes","courant"]},
  {"mot":"gbagboter","francais":"marcher longtemps","categorie":"verbe","definition":"Marcher beaucoup et sur une longue distance","tags":["mouvement","courant"]},
  {"mot":"gbai","francais":"vérité, conseil, sermon","categorie":"nom","definition":"Vérité ; conseil, sermon, discours de sagesse","tags":["courant"]},
  {"mot":"gbahé","francais":"gronder, conseiller","categorie":"verbe","definition":"Gronder, conseiller, sermonner ; ou s'absenter","tags":["courant"]},
  {"mot":"gbairè","francais":"commérage, ragot","categorie":"nom","definition":"Commérage, ragot, médisance, dénigrement","tags":["courant"]},
  {"mot":"gbêdê","francais":"faire l'amour (vulgaire)","categorie":"verbe","definition":"Avoir des rapports sexuels (terme vulgaire)","tags":["adulte","vulgaire"]},
  {"mot":"gbêss","francais":"500 FCFA","categorie":"nom","definition":"500 francs CFA","tags":["finance","courant"]},
  {"mot":"gbô","francais":"manger, poing","categorie":"verbe / nom","definition":"Manger ; ou poing, coup de poing","tags":["nourriture","violence","courant"]},
  {"mot":"gbôlôzailli","francais":"gros, massif, musclé","categorie":"adjectif","definition":"Gros, massif, musclé, imposant physiquement","tags":["corps","courant"]},
  {"mot":"gbonhon","francais":"5 000 FCFA","categorie":"nom","definition":"Cinq mille francs CFA (5 000 F)","tags":["finance","courant"]},
  {"mot":"gbonhi","francais":"groupe, bande","categorie":"nom","definition":"Groupe, bande, gang","tags":["personnes","courant"]},
  {"mot":"glôglô","francais":"raccourci, bas quartier","categorie":"nom","definition":"Couloirs, raccourci ; bas quartier populaire","tags":["géographie","courant"]},
  {"mot":"gnanhi","francais":"femme cougar","categorie":"nom","definition":"Femme plus âgée qui sort avec des jeunes hommes, femme cougar","tags":["personnes","relations","courant"]},
  {"mot":"gnakoué","francais":"ignorant, couillon","categorie":"nom / adjectif","definition":"Ignorant, couillon, imbécile","tags":["personnes","courant"]},
  {"mot":"gnaga","francais":"bagarre","categorie":"nom","definition":"Bagarre, combat, rixe","tags":["violence","courant"]},
  {"mot":"gnata","francais":"très ignorant","categorie":"adjectif","definition":"Très ignorant, extrêmement naïf","tags":["personnes","courant"]},
  {"mot":"go","francais":"fille, petite amie","categorie":"nom","definition":"Fille, jeune femme, petite amie (très courant)","tags":["personnes","relations","courant"]},
  {"mot":"goumin","francais":"chagrin d'amour","categorie":"nom","definition":"Chagrin d'amour, peine de cœur","tags":["amour","relations","courant"]},
  {"mot":"groto","francais":"homme riche","categorie":"nom","definition":"Homme riche, nanti, qui a de l'argent","tags":["personnes","finance","courant"]},
  {"mot":"grouilleur","francais":"débrouillard","categorie":"nom","definition":"Personne débrouillarde qui trouve toujours une solution","tags":["personnes","courant"]},
  {"mot":"jahin","francais":"jamais","categorie":"adverbe","definition":"Jamais, en aucun cas","tags":["courant"]},
  {"mot":"ken","francais":"chose, deal, affaire","categorie":"nom","definition":"Chose, plan, deal, affaire, truc","tags":["courant"]},
  {"mot":"kener","francais":"planifier, vendre","categorie":"verbe","definition":"Planifier, dealer, vendre quelque chose","tags":["commerce","courant"]},
  {"mot":"keneur","francais":"vendeur, dealeur","categorie":"nom","definition":"Vendeur, dealeur, intermédiaire commercial","tags":["personnes","commerce","courant"]},
  {"mot":"kpakpato","francais":"rapporteur, colporteur","categorie":"nom","definition":"Rapporteur, colporteur de ragots, indiscret","tags":["personnes","courant"]},
  {"mot":"kpakpatoya","francais":"commérage, colportage","categorie":"nom","definition":"Commérage, colportage, action de rapporter","tags":["courant"]},
  {"mot":"kourou bâtard","francais":"coup de poing violent","categorie":"expression","definition":"Coup de poing très violent, uppercut","tags":["violence","courant"]},
  {"mot":"lā","francais":"donner","categorie":"verbe","definition":"Donner, offrir quelque chose à quelqu'un","tags":["courant"]},
  {"mot":"laler","francais":"gifler, frapper","categorie":"verbe / nom","definition":"Gifler, frapper ; téléphone ou endroit selon le contexte","tags":["violence","courant"]},
  {"mot":"maga","francais":"se battre, dérober","categorie":"verbe / nom","definition":"Se battre, battre quelqu'un, dérober ; surprise (magatapé)","tags":["violence","courant"]},
  {"mot":"môgô","francais":"personne, pote","categorie":"nom","definition":"Personne, gens, homme, ami, pote","tags":["personnes","courant"]},
  {"mot":"mono","francais":"policier, gendarme","categorie":"nom","definition":"Policier, gendarme, agent des forces de l'ordre","tags":["police","courant"]},
  {"mot":"moro","francais":"pièce de 5 FCFA","categorie":"nom","definition":"Une pièce de 5 francs CFA","tags":["finance","courant"]},
  {"mot":"mougou","francais":"faire l'amour","categorie":"verbe","definition":"Faire l'amour, avoir des rapports sexuels","tags":["relations","adulte"]},
  {"mot":"mougouli","francais":"rapport sexuel","categorie":"nom","definition":"Rapport sexuel, acte sexuel","tags":["relations","adulte"]},
  {"mot":"mousso","francais":"femme","categorie":"nom","definition":"Femme (du dioula : mousso)","tags":["personnes","dioula","courant"]},
  {"mot":"kpetou","francais":"vulve, vagin","categorie":"nom","definition":"Vulve, vagin (terme vulgaire)","tags":["corps","vulgaire","adulte"]},
  {"mot":"kpôclé","francais":"prostituée","categorie":"nom","definition":"Fille de mauvaises mœurs, prostituée","tags":["personnes","vulgaire"]},
  {"mot":"pahé","francais":"parce que, car","categorie":"conjonction","definition":"Parce que, car, vu que","tags":["courant"]},
  {"mot":"painhou","francais":"prostituée","categorie":"nom","definition":"Prostituée, travailleuse du sexe","tags":["personnes","vulgaire"]},
  {"mot":"pantougouler","francais":"fuir, s'échapper","categorie":"verbe","definition":"Fuir, s'échapper, détaler rapidement","tags":["mouvement","courant"]},
  {"mot":"petit pompier","francais":"gigolo","categorie":"nom","definition":"Gigolo, jeune homme entretenu par une femme plus âgée","tags":["personnes","relations"]},
  {"mot":"pinkou","francais":"faire l'amour","categorie":"verbe","definition":"Faire l'amour, avoir des rapports sexuels","tags":["relations","adulte"]},
  {"mot":"plomb","francais":"100 FCFA","categorie":"nom","definition":"Cent (100) francs CFA","tags":["finance","courant"]},
  {"mot":"propro","francais":"produit éclaircissant, poursuivre","categorie":"nom / verbe","definition":"Produit cosmétique éclaircissant ; ou poursuivre quelqu'un","tags":["courant"]},
  {"mot":"sêkpêl","francais":"maigrichon, poids plume","categorie":"nom / adjectif","definition":"Personne très maigre, poids plume","tags":["corps","courant"]},
  {"mot":"skinny","francais":"belle femme mince","categorie":"nom","definition":"Belle jeune femme mince et élancée","tags":["personnes","corps","courant"]},
  {"mot":"soutra","francais":"aider, sauver","categorie":"verbe","definition":"Aider, sauver, sortir quelqu'un d'une mauvaise passe","tags":["courant"]},
  {"mot":"soayé","francais":"méchant, mauvais","categorie":"adjectif","definition":"Méchant, mauvais, dangereux","tags":["courant"]},
  {"mot":"sri","francais":"attraper","categorie":"verbe","definition":"Attraper, saisir, appréhender","tags":["courant"]},
  {"mot":"tassaba","francais":"grosses fesses","categorie":"nom","definition":"Grosses fesses, gros postérieur","tags":["corps","courant"]},
  {"mot":"tchiza","francais":"maîtresse d'un homme marié","categorie":"nom","definition":"Maîtresse d'un homme marié, amante clandestine (tchizambengué : maîtresse de haut standing)","tags":["personnes","relations"]},
  {"mot":"tchizo","francais":"homme marié infidèle","categorie":"nom","definition":"Homme marié qui a une ou plusieurs maîtresses","tags":["personnes","relations"]},
  {"mot":"togo","francais":"100 ou 100 000 FCFA","categorie":"nom","definition":"100 francs CFA ; ou 100 000 francs CFA selon le contexte","tags":["finance","courant"]},
  {"mot":"tolo","francais":"gifler","categorie":"verbe","definition":"Gifler, donner une gifle","tags":["violence","courant"]},
  {"mot":"wéh","francais":"chose, truc, deal","categorie":"nom","definition":"Chose, truc, plan, deal, affaire","tags":["courant"]},
  {"mot":"wéman","francais":"dealeur","categorie":"nom","definition":"Dealeur, vendeur, intermédiaire","tags":["personnes","commerce","courant"]},
  {"mot":"woro-woro","francais":"taxi collectif","categorie":"nom","definition":"Taxi collectif, taxi communal partagé","tags":["transport","courant"]},
  {"mot":"yafor","francais":"d'accord","categorie":"interjection","definition":"D'accord, oui, entendu, c'est bon","tags":["courant"]},
  {"mot":"yé","francais":"je","categorie":"pronom","definition":"Je (pronom personnel sujet en nouchi)","tags":["courant"]},
  {"mot":"zogotape","francais":"assommer","categorie":"verbe","definition":"Assommer quelqu'un, le frapper jusqu'à l'étourdir","tags":["violence","courant"]},
  {"mot":"zébri manyé","francais":"viol","categorie":"nom","definition":"Viol, agression sexuelle","tags":["violence","adulte"]},
  {"mot":"zo","francais":"beau","categorie":"adjectif","definition":"Beau, joli (neutre, masculin ou féminin)","tags":["courant"]},
  {"mot":"zota","francais":"belle","categorie":"adjectif","definition":"Belle, jolie (féminin)","tags":["courant"]},
  {"mot":"zogor","francais":"ennuyeux","categorie":"adjectif / nom","definition":"Une chose, personne ou idée ennuyeuse, barbante","tags":["courant"]},
]

# ── Mots scrappés nouchi.com ─ on garde ceux avec une vraie def française ──────
scraped = json.load(open("scraped_nouchi.json", encoding="utf-8"))

# Indicateurs d'une définition en français (pas juste un autre mot nouchi)
FR_WORDS = re.compile(
    r'\b(le|la|les|un|une|des|de|du|au|aux|et|ou|qui|que|par|pour|dans|sur|avec|sans|'
    r'être|avoir|faire|aller|venir|prendre|donner|voir|dire|savoir|pouvoir|vouloir|'
    r'personne|homme|femme|fille|garçon|argent|chose|action|beau|belle|grand|petit|'
    r'jamais|toujours|aussi|très|trop|beaucoup|souvent|quelqu|rien|tout|c\'est|se|'
    r'action|fait|façon|manière|genre|type|sorte|même|plus|moins|bien|mal|oui|non|'
    r'signifie|désigne|indique|représente|parler|crier|fuir|marcher|manger|boire)\b',
    re.IGNORECASE
)

user_mots = {w["mot"].lower() for w in USER_WORDS}
extra = []
seen_extra = set()

for w in scraped:
    mot = w["mot"].strip()
    sig = w["sig"].strip()
    if not mot or not sig:
        continue
    key = mot.lower()
    # Skip if already in user list or already seen
    if key in user_mots or key in seen_extra:
        continue
    # Skip if definition looks like just another nouchi word (short, no FR indicators)
    if len(sig) < 8 or not FR_WORDS.search(sig):
        continue
    # Skip obviously circular refs
    if sig.lower() == mot.lower():
        continue
    seen_extra.add(key)
    cat = w.get("type", "nom").strip() or "nom"
    # Normalize category
    cat_map = {"expression": "expression", "adjectif": "adjectif", "verbe": "verbe",
               "nom": "nom", "adverbe": "adverbe", "interjection": "interjection",
               "pronom": "pronom", "conjonction": "conjonction"}
    cat_clean = cat_map.get(cat.lower().split()[0], "nom")
    extra.append({
        "mot": mot,
        "francais": sig[:60],
        "categorie": cat_clean,
        "definition": sig,
        "tags": ["courant"],
    })

print(f"Mots utilisateur : {len(USER_WORDS)}")
print(f"Mots nouchi.com retenus : {len(extra)}")

# ── Fusion et numérotation ────────────────────────────────────────────────────
final = []
for i, w in enumerate(USER_WORDS + extra, start=1):
    entry = {
        "id": i,
        "mot": w["mot"],
        "francais": w.get("francais", ""),
        "phonetique": w.get("phonetique", None),
        "categorie": w.get("categorie", "nom"),
        "definition": w.get("definition", ""),
        "exemple": w.get("exemple", None),
        "traduction_exemple": w.get("traduction_exemple", None),
        "tags": w.get("tags", ["courant"]),
        "contributeur": w.get("contributeur", "équipe Dico Nouchi"),
    }
    final.append(entry)

with open("dictionary.json", "w", encoding="utf-8") as f:
    json.dump(final, f, ensure_ascii=False, indent=2)

print(f"Total final : {len(final)} mots -> dictionary.json")
