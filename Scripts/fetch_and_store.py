import requests
import psycopg2
from datetime import datetime

# PostgreSQL config
DB_HOST = 'localhost'
DB_NAME = 'crypto_data'
DB_USER = 'postgres'
DB_PASS = '5050'

def fetch_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': False
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def insert_data(data):
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()

    for coin in data:
        cur.execute("""
            INSERT INTO raw_coin_data (
                name, symbol, current_price, market_cap, market_cap_rank,
                total_volume, high_24h, low_24h, price_change_24h,
                price_change_percentage_24h, last_updated
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            coin['name'], coin['symbol'], coin['current_price'], coin['market_cap'],
            coin['market_cap_rank'], coin['total_volume'], coin['high_24h'], coin['low_24h'],
            coin['price_change_24h'], coin['price_change_percentage_24h'],
            datetime.fromisoformat(coin['last_updated'].replace('Z', '+00:00'))
        ))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    data = fetch_data()
    insert_data(data)
    print("✅ Data successfully inserted into database.")
