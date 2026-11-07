# Communalis

## Livre et édition PDF

Le livre est organisé en fichiers texte modifiables, à lire dans cet ordre :

1. [Avant-propos et introduction](Livre_Introduction.txt)
2. [Partie A — Préparer](Livre_Partie_A.txt)
3. [Partie B — Énergie et infrastructure](Livre_Partie_B.txt)
4. [Partie C — Couche linguistique](Livre_Partie_C.txt)
5. [Partie D — Connecter le territoire](Livre_Partie_D.txt)
6. [Partie E — Agir en sécurité](Livre_Partie_E.txt)
7. [Partie F — Durer et essaimer](Livre_Partie_F.txt)
8. [Annexes et registre de suivi](Livre_Annexes.txt)

Les repères « À ACTUALISER » signalent les éléments qui évoluent avec le
projet ; « RÉSULTATS TOGO À INSÉRER » réserve les observations non encore
disponibles. Le registre de suivi, en fin d'annexes, précise les responsables
à désigner, les déclencheurs et les preuves à réunir. Il ne crée pas de
notification automatique.

Le [cahier terrain PDF](Communalis_Cahier_Terrain.pdf) est une édition
de travail au format A4, avec un sommaire paginé, des titres hiérarchisés,
des schémas en police à chasse fixe et des tableaux lisibles. Les tableaux
de plus de trois colonnes sont présentés en fiches avec des champs étiquetés,
sans réduction excessive de la police. Les champs colorés signalent les données, décisions, preuves et
autorisations réelles à fournir par l'équipe. Aucun résultat de terrain n'a
été inventé : le livre ne pourra devenir un récit factuel achevé qu'après
validation de ces éléments. Le [manuscrit initial](Manuscrit_Communalis.txt)
est conservé comme version de référence antérieure.

Pour régénérer le PDF avec les polices FreeSerif installées :

```sh
python3 -m venv .venv-pdf
.venv-pdf/bin/pip install -r requirements-pdf.txt
.venv-pdf/bin/python build_book.py
```

La pagination découle du contenu : aucun nombre de pages n'est imposé.
L'annexe G contient le glossaire ; l'annexe H propose une bibliographie
à compléter avec les sources effectivement utilisées et les preuves de terrain.
L'ancien export suffixé `300p` est remplacé par le PDF ci-dessus.

Les contrôles du générateur peuvent être lancés avec :

```sh
.venv-pdf/bin/python -m unittest discover -s tests
```