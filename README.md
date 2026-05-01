🤖 Polymarket BTC 5min Bot
Bot de trading automatisé sur Polymarket pour les marchés Bitcoin Up/Down 5 minutes.
---
📋 Description
Ce bot place automatiquement des ordres sur les marchés BTC Up/Down de Polymarket toutes les 5 minutes. Il utilise l'API CLOB V2 de Polymarket et le client Python officiel `py-clob-client-v2`.
---
⚙️ Prérequis
Python 3.10+
Un wallet MetaMask sur le réseau Polygon
Des fonds en pUSD sur votre wallet
Du POL pour le gas (0.05 POL suffit)
Un compte Polymarket avec clés API
---
📦 Installation
```bash
# Cloner le projet
git clone https://github.com/YanraSama/polymarket\_btc\_5mn\_strat.git
cd polymarket\_btc\_5mn\_strat

# Installer les dépendances
pip install py-clob-client-v2 web3 python-dotenv eth-account requests
```
---
🔐 Configuration
Créez un fichier `.env` à la racine du projet :
```env
PRIVATE\_KEY=0x...                  # Clé privée de votre wallet MetaMask
ALCHEMY\_RPC=https://polygon-mainnet.g.alchemy.com/v2/VOTRE\_CLE
FUNDER\_ADDRESS=0x...               # Adresse de votre wallet
```
> ⚠️ \*\*Ne partagez jamais votre clé privée.\*\* Le fichier `.env` est dans `.gitignore`.
---
🏗️ Architecture
```
polymarket-bot/
│
├── poly\_bot\_v1.py       # Script principal
├── .env                 # Variables d'environnement (non versionné)
├── .gitignore           # Ignore .env et fichiers sensibles
└── README.md            # Ce fichier
```
---
🔑 Obtenir vos clés API
Connectez-vous sur polymarket.com avec MetaMask
Allez dans Settings → Builder Codes
Copiez votre Builder Code et vos clés API
Ajoutez-les dans votre fichier `.env`
---
💰 Préparer vos fonds
Achetez des USDC sur le réseau Polygon
Convertissez-les en pUSD via l'interface Polymarket (Deposit)
Vérifiez que votre wallet a au moins 0.05 POL pour le gas
---
🚀 Utilisation
```bash
python poly\_bot\_v1.py
```
Le bot va :
Dériver votre adresse wallet depuis la clé privée
Vérifier votre balance POL
Approuver les contrats Polymarket si nécessaire
Récupérer le marché BTC 5min en cours
Placer un ordre GTC au meilleur prix disponible
---
📊 Paramètres de l'ordre
Paramètre	Valeur	Description
`price`	`best\_ask`	Prix du marché en temps réel
`size`	`5` minimum	Nombre de tokens achetés
`side`	`BUY`	Achat de tokens YES ou NO
`order\_type`	`GTC`	Good Till Cancelled
---
--
⚠️ Avertissements
Ce bot est fourni à titre éducatif uniquement
Le trading de prédiction comporte des risques de perte en capital
Testez toujours avec de petits montants avant de scaler
Ne laissez jamais votre clé privée dans le code source
---
📚 Ressources
Documentation Polymarket
Migration V2
py-clob-client-v2
Polygonscan
---
