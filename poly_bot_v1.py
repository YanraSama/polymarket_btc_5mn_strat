import time
import requests
import json  # Pour convertir la string clobTokenIds en vraie liste

import requests

from py_clob_client_v2.client import ClobClient
import os
from py_clob_client_v2.clob_types import OrderArgs, OrderType, PartialCreateOrderOptions
from py_clob_client_v2.order_builder.constants import BUY

from py_clob_client_v2.clob_types import ApiCreds
from web3 import Web3
from eth_account import Account
import requests as req




# Test direct sans py_clob_client
import requests, time, hmac, hashlib


acct = Account.from_key("0x4460836331a0103c71068ca81c248aff3984d208e6791e6c488525a460b51373")
FUNDER_ADDRESS = acct.address

print("Adresse dérivée :", acct.address)


# ================= CONFIG =================
PRIVATE_KEY = "0x4460836331a0103c71068ca81c248aff3984d208e6791e6c488525a460b51373"  # Mets ta private key ici (ou dans .env)
HOST = "https://clob.polymarket.com"
CHAIN_ID = 137  # Polygon mainnet
FUNDER_ADDRESS = acct.address  # Ton adresse wallet


# ── Ensuite seulement : votre create_and_post_order() ─────────

temp_client = ClobClient(
    host=HOST,
    key=PRIVATE_KEY,
    chain_id=CHAIN_ID,
    
)
proxy_address = temp_client.get_address()
print("Proxy wallet Polymarket :", proxy_address)


api_creds = temp_client.create_or_derive_api_key()
print(api_creds)

# Initialisation du client
client = ClobClient(
    host = HOST,
    key=PRIVATE_KEY,
    chain_id=CHAIN_ID,
    creds=api_creds,   # 🔥 CRUCIAL
    signature_type=1,
    funder="0xdEd07EA1E65193660a959Fb5Cc82E8Eee183Ff40"
)

GAMMA_API = "https://gamma-api.polymarket.com"


#---------------------------------------------------------------------------------------------------------------------------

def get_current_btc_5m_slug():
    now = int(time.time())                    # timestamp actuel
    window_start = (now // 300) * 300         # arrondi au multiple de 300 secondes (5 min)
    slug = f"btc-updown-5m-{window_start}"
    return slug

def get_btc_5m_market():
    slug = get_current_btc_5m_slug()
    
    # Méthode 1 : via events (souvent plus complet)
    response = requests.get(f"{GAMMA_API}/events/slug/{slug}")
    if response.status_code == 200:
        event = response.json()
        # L'event contient souvent les markets
        if event.get("markets"):
            market = event["markets"][0]   # pour les marchés Up/Down, il y en a généralement 2 (Up et Down)
            return market
        
    return None

# Exemple d'utilisation
market = get_btc_5m_market()

if market:
    question = market.get("question")
    clob_token_ids = market.get("clobTokenIds")   # liste de 2 strings : [Yes_token, No_token]
        
    if isinstance(clob_token_ids, str):
        try:
            # Nettoyage et conversion de la string en vraie liste
            clob_token_ids = json.loads(clob_token_ids.replace("'", '"'))
        except json.JSONDecodeError:
            clob_token_ids = []   # en cas d'erreur     
    
    print(f"Marché trouvé : {question}")
    print(f"    Yes Token : {clob_token_ids[0] if len(clob_token_ids) > 0 else 'N/A'}")
    print(f"    No  Token : {clob_token_ids[1] if len(clob_token_ids) > 1 else 'N/A'}")
    
    print(f"FUND ADRESS : {FUNDER_ADDRESS}")
    
    response = requests.get(
    "https://gamma-api.polymarket.com/markets",
    params={"slug": get_current_btc_5m_slug()})
    
    
    market_data = response.json()[0]

    condition_id = market_data["conditionId"]
    
    clob_ids = market_data["clobTokenIds"]

    if isinstance(clob_ids, str):
        clob_ids = json.loads(clob_ids.replace("'", '"'))

    yes_token = clob_ids[1]
    
    print("TOKEN ID utilisé :", yes_token)

    # Fetch market details to get tick size and neg risk
    market_details = client.get_market(condition_id)   # ← ICI on passe le conditionId !


    try:
        client.get_tick_size(yes_token)
    except Exception as e:
        print("Token non tradable :", e)
        exit()

    # ================= PLACEMENT D'ORDRE =================
   # tick_size = str(market["minimum_tick_size"])   # e.g., "0.01"
   # neg_risk = market["neg_risk"]             # e.g., False

    response = client.create_and_post_order(
        OrderArgs(
            token_id=yes_token,
            price=0.10,
            size= 5,           # ← petit montant pour tester
            side=BUY,
        ),
        options= PartialCreateOrderOptions(
            tick_size = "0.01",
            neg_risk  = False,
        ),
        order_type = OrderType.GTC     # Fill Or Kill        — ordre marché, exécution immédiate
    )
        

   # print("Order ID:", response["orderID"])
   # print("Status:", response["status"])

    print("✅ Ordre placé !")
    print("Order ID  :", response.get("orderID"))
    print("Status    :", response.get("status"))
    
    
    # Tu peux maintenant trader avec clob_token_ids[0] pour acheter "Up"
else:
    print("Marché non trouvé (trop tôt ou trop tard ?)")
    
