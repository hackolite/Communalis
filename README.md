# Communalis

## Guide de référence pour le Togo

Le [Guide de référence Communalis au Togo](Guide_Reference_Communalis_Togo.md)
complète le livre de terrain par un cadre opérationnel pour un pilote à
Baguida : services HubCity, architecture Code–Hardware–Design, indicateurs,
apprentissage par renforcement sous contrôle, catalogue de projets,
bootcamp, déploiement, gouvernance et réplication. Il distingue les méthodes
proposées des résultats qui restent à établir sur le terrain.

## Livre et édition PDF

Le cahier terrain principal est orienté service et adoption ; son parcours
produit est suivi des annexes pratiques. Les chapitres techniques détaillés
sont conservés dans un second volume pour être consultés selon le cas
d'usage. Les sources texte correspondantes sont :

1. [Avant-propos et introduction](Livre_Introduction.txt)
2. [Parcours produit — de l'idée à l'adoption](Livre_Parcours_Produit.txt)
3. [Annexes pratiques et registre de suivi](Livre_Annexes.txt)
4. [Partie A — Préparer](Livre_Partie_A.txt)
5. [Partie B — Énergie et infrastructure](Livre_Partie_B.txt)
6. [Partie C — Services linguistiques](Livre_Partie_C.txt)
7. [Partie D — Capteurs et territoire](Livre_Partie_D.txt)
8. [Partie E — Décider et agir en sécurité](Livre_Partie_E.txt)
9. [Partie F — Maintenance et réplication](Livre_Partie_F.txt)

Les repères « À ACTUALISER » signalent les éléments qui évoluent avec le
projet ; « RÉSULTATS TOGO À INSÉRER » réserve les observations non encore
disponibles. Le registre de suivi, en fin d'annexes, précise les responsables
à désigner, les déclencheurs et les preuves à réunir. Il ne crée pas de
notification automatique.

Le [cahier produit et terrain PDF](Communalis_Cahier_Terrain.pdf) est le
volume principal destiné aux institutions, équipes produit et participants
du bootcamp. Il comprend le parcours d'adoption, les services HubCity,
26 pistes de projets, des jalons de déploiement et un gabarit d'équipe.
Les [dossiers techniques PDF](Communalis_Dossiers_Techniques.pdf) conservent
les chapitres détaillés sur la préparation, l'énergie, les langues, les
capteurs, la sécurité, la maintenance et la réplication. Le volume principal
est structuré pour une relecture et une validation locale ; ses champs
signalent les informations qui restent à confirmer. Aucun résultat de
terrain n'est inventé. Le
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

La commande génère les deux PDF. La pagination découle du contenu ; aucun
nombre de pages n'est imposé. Les annexes contiennent des gabarits, un
glossaire et des références à compléter avec les sources effectivement
utilisées et les preuves de terrain. Les anciens exports suffixés `300p`
ne sont pas les éditions de référence.

Les contrôles du générateur peuvent être lancés avec :

```sh
.venv-pdf/bin/python -m unittest discover -s tests
```