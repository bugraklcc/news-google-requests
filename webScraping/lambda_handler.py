import json

from my_news.scrape_news import scrape_news, create_connection, insert_to_db


def lambda_handler(event, context):
    category_url_map = {
        "Türkiye": "https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNREY2Ym1OZkVnSjBjaWdBUAE?hl=tr&gl=TR&ceid=TR%3Atr",
        "Dünya": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr",
        "Yerel": "https://news.google.com/topics/CAAqHAgKIhZDQklTQ2pvSWJHOWpZV3hmZGpJb0FBUAE/sections/CAQiUENCSVNOam9JYkc5allXeGZkakpDRUd4dlkyRnNYM1l5WDNObFkzUnBiMjV5Q3hJSkwyMHZNRGs1TkRsdGVnc0tDUzl0THpBNU9UUTViU2dBKjEIACotCAoiJ0NCSVNGem9JYkc5allXeGZkako2Q3dvSkwyMHZNRGs1TkRsdEtBQVABUAE?hl=tr&gl=TR&ceid=TR%3Atr",
        "İş": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr",
        "Bilim ve Teknoloji": "https://news.google.com/topics/CAAqKAgKIiJDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSjBjaG9DVkZJb0FBUAE?hl=tr&gl=TR&ceid=TR%3Atr",
        "Eğlence": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr",
        "Spor": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr",
        "Sağlık": "https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FuUnlLQUFQAQ?hl=tr&gl=TR&ceid=TR%3Atr",
    }

    all_news = []

    for category, url in category_url_map.items():
        scrape_result = scrape_news(category, url)
        all_news += scrape_result.get(f"{category}Data", [])

    connection = create_connection()
    
    insert_to_db(connection, all_news)

    return all_news
