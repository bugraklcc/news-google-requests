import json
import requests
from bs4 import BeautifulSoup
import pymysql
from pymysql import Error


def scrape_news(category, url):
    result = {}

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    news_data = []

    news_sections = soup.find_all('div', class_='EctEBd', jsname='rAluZb')

    for section in news_sections:
        category_text = section.text.strip()

        if category_text == category:
            sources = section.find_all_next('div', class_='MCAGUe')
            links = section.find_all_next('a', class_='WwrzSb')
            summaries = section.find_all_next('h4', class_='gPFEn')
            dates = section.find_all_next('time', class_='hvbAAd')

            for i, (source, link, summary, date) in enumerate(
                    zip(sources, links, summaries, dates), start=1):
                source_div = source.find('div', class_='vr1PYe')

                if source_div:
                    source_text = source_div.text.strip()
                else:
                    source_text = "Source not found"

                news_url = f"https://news.google.com{link['href']}" if link else "URL not found"
                summary_text = summary.text.strip() if summary else "Description not found"
                date_text = date.get('datetime') if date else "Date not found"

                news_item = {
                    "Category": category,
                    "Source": source_text,
                    "URL": news_url,
                    "ShortDescription": summary_text,
                    "PublicationDate": date_text
                }

                news_data.append(news_item)

    result["Status"] = "Success"
    result["Message"] = f"{category} data scraped successfully."
    result[f"{category}Data"] = news_data

    return result


if __name__ == "__main__":
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

    json_data = json.dumps(all_news, indent=4, ensure_ascii=False)
    print(json_data)


def create_connection():
    host = 'database-1.cmbjzgj4iu72.us-east-1.rds.amazonaws.com'
    user = 'admin'
    password = 'password123.+'
    database = 'news'

    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return connection


def insert_to_db(connection, all_news):
    try:
        if connection.open:
            cursor = connection.cursor()

            for news_item in all_news:
                insert_query = 'INSERT INTO news.news_articles (category, source, url, short_description, publication_date) VALUES (%s, %s, %s, %s, %s)'
                data = (news_item["Category"], news_item["Source"], news_item["URL"], news_item["ShortDescription"],
                        news_item["PublicationDate"])
                cursor.execute(insert_query, data)
                connection.commit()
    except Error as e:
        print(f"MySQL Error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
