# Smart Food Redistribution - Projet de Problem Solving

Ce projet scolaire vise à concevoir un système intelligent de redistribution alimentaire afin de lutter contre le gaspillage, optimiser la logistique de livraison, et répondre à la demande en temps réel à l’aide de techniques avancées d’algorithmique et d’intelligence artificielle.

---

## Objectifs du projet

- Réduire les pertes alimentaires liées à la péremption.  
- Optimiser les trajets et plannings de distribution.  
- Classifier automatiquement les dons alimentaires.  
- Simuler différentes situations (pics de dons, urgences, pénuries).  
- Intégrer des modèles de prédiction (demande, expiration...).

---

## Technologies utilisées

### Langages & frameworks
- **Python 3.11+**  
- **SimPy** — simulation événementielle  
- **Mesa** — modélisation multi-agents  
- **NetworkX** — graphes de routes logistiques  
- **PuLP** — optimisation linéaire  
- **DEAP** — algorithmes génétiques  
- **TensorFlow / Keras** — deep learning  
- **Scikit‑learn** — machine learning classique  
- **Pandas / NumPy** — traitement de données  
- **Matplotlib / Plotly** — visualisation de données  

---

## Structure du projet

```text
distribution-alimentaire/
│
├── src/                  # Code source Python
│   ├── models/           # Classes des agents (Donor, Receiver, etc.)
│   └── simulation.py     # Script principal de simulation
│
├── data/                 # Données d’entrée et résultats de simulation
├── docs/                 # UML, diagrammes et documentation
├── notebooks/            # Notebooks Jupyter d’expérimentation
├── requirements.txt      # Dépendances Python
└── README.md             # Ce fichier

```
--- 
## Exécution rapide 

**Installer les dépendances** :

Voici comment installer les dépendances et exécuter une simulation simple :

```bash
pip install -r requirements.txt
```
**Lancer une simulation basique** :
```bash
python src/simulation.py
```
Assurez-vous d’exécuter ces commandes depuis le répertoire racine du projet.

---

## 🧭 Scénarios simulés 

Les scénarios simulés permettent d'évaluer la performance et l'efficacité de notre système de redistribution dans différents contextes. Voici les scénarios pris en compte :

- Redistribution en zone urbaine saturée  
- Pic de dons le week‑end  
- Urgence alimentaire régionale  
- Optimisation dynamique des trajets  
- Prédiction de la demande et de la péremption  

---

## 🧾 Informations complémentaires

- **Cours** : Problem Solving – ISG Tunis  
- **Encadrant** : M. Chaouki Bayoudhi  
- **Groupe** : 2BIS  
- **Année** : 2024 – 2025  
- **Date de remise** : 06 mai 2025  

---

## 👩‍💻 Équipe projet

- Nour  
- Ghada Dagdagui  
- Hene Trigui  
- Taher  

---

## 🔗 Ressources utiles

- [SimPy documentation](https://simpy.readthedocs.io/)  
- [Mesa (agent-based) docs](https://mesa.readthedocs.io/en/stable/)  
- [PuLP (optimization)](https://coin-or.github.io/pulp/)  
- [DEAP (evolutionary) docs](https://deap.readthedocs.io/en/master/)  
- [TensorFlow / Keras](https://www.tensorflow.org/)  
- [Scikit‑learn](https://scikit-learn.org/stable/)  
- [Pandas](https://pandas.pydata.org/docs/)  
- [NumPy](https://numpy.org/doc/)  
- [Matplotlib](https://matplotlib.org/stable/)  
- [Plotly](https://plotly.com/python/)  
