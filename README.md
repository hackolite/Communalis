# Communalis

## Guide de référence pour le Togo

Le [Guide de référence Communalis au Togo](Guide_Reference_Communalis_Togo.md)
complète le livre de terrain par un cadre opérationnel pour un pilote à
Baguida : services HubCity, architecture Code–Hardware–Design, indicateurs,
apprentissage par renforcement sous contrôle, catalogue de projets,
bootcamp, déploiement, gouvernance et réplication. Il distingue les méthodes
proposées des résultats qui restent à établir sur le terrain.

## Livre et édition PDF

Le cahier terrain complet suit une progression unique : parcours produit,
dossiers techniques, puis annexes pratiques. Les sources texte sont
assemblées dans cet ordre :

1. [Avant-propos et introduction](Livre_Introduction.txt)
2. [Parcours produit — de l'idée à l'adoption](Livre_Parcours_Produit.txt)
3. [Partie A — Préparer](Livre_Partie_A.txt)
4. [Partie B — Énergie et infrastructure](Livre_Partie_B.txt)
5. [Partie C — Services linguistiques](Livre_Partie_C.txt)
6. [Partie D — Capteurs et territoire](Livre_Partie_D.txt)
7. [Partie E — Décider et agir en sécurité](Livre_Partie_E.txt)
8. [Partie F — Maintenance et réplication](Livre_Partie_F.txt)
9. [Annexes pratiques et registre de suivi](Livre_Annexes.txt)

Les repères « À ACTUALISER » signalent les éléments qui évoluent avec le
projet ; « RÉSULTATS TOGO À INSÉRER » réserve les observations non encore
disponibles. Le registre de suivi, en fin d'annexes, précise les responsables
à désigner, les déclencheurs et les preuves à réunir. Il ne crée pas de
notification automatique.

Le [cahier terrain PDF](Communalis_Cahier_Terrain.pdf) est le volume complet,
destiné aux institutions, équipes produit et participants du bootcamp. Il
ouvre sur l'adoption et l'usage, poursuit avec les dossiers techniques, puis
termine par les annexes. Une édition
[séparée des dossiers techniques](Communalis_Dossiers_Techniques.pdf) est
aussi générée pour consultation ciblée. Le cahier principal inclut les
services HubCity, 26 pistes de projets, les jalons de déploiement et un
gabarit d'équipe. Ses champs signalent les informations à confirmer ;
aucun résultat de terrain n'est inventé. Le
[guide de référence détaillé pour le Togo](Guide_Reference_Communalis_Togo.md)
reste disponible comme ressource complémentaire. Le
[manuscrit initial](Manuscrit_Communalis.txt) est conservé comme version
antérieure.

Pour régénérer le PDF avec les polices FreeSerif installées :

```sh
python3 -m venv .venv-pdf
.venv-pdf/bin/pip install -r requirements-pdf.txt
.venv-pdf/bin/python build_book.py
```

La commande génère le cahier complet et l'édition technique séparée. La
pagination découle du contenu ; aucun nombre de pages n'est imposé. Les
annexes contiennent des gabarits, un glossaire et des références à compléter
avec les sources effectivement utilisées et les preuves de terrain. Les
anciens exports suffixés `300p` ne sont pas les éditions de référence.

Les contrôles du générateur peuvent être lancés avec :

```sh
.venv-pdf/bin/python -m unittest discover -s tests
```