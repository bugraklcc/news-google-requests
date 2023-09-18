import requests
from bs4 import BeautifulSoup
import pymysql
from pymysql import Error


def scrape_news(category):
    connection = pymysql.connect(
        host='database-1.cmbjzgj4iu72.us-east-1.rds.amazonaws.com',
        user='admin',
        password='password123.+',
        database='news'
    )

    result = {}

    # Create the URL based on the category
    category_urls_map = {
        "Türkiye": "https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNREY2Ym1OZkVnSjBjaWdBUAE?hl=tr&gl=TR&ceid=TR%3Atr",
        "Dünya": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr",
        "Yerel": "https://news.google.com/topics/CAAqHAgKIhZDQklTQ2pvSWJHOWpZV3hmZGpJb0FBUAE/sections/CAQiUENCSVNOam9JYkc5allXeGZkakpDRUd4dlkyRnNYM1l5WDNObFkzUnBiMjV5Q3hJSkwyMHZNRGs1TkRsdGVnc0tDUzl0THpBNU9UUTViU2dBKjEIACotCAoiJ0NCSVNGem9JYkc5allXeGZkako2Q3dvSkwyMHZNRGs1TkRsdEtBQVABUAE?hl=tr&gl=TR&ceid=TR%3Atr",
        "İş": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr",
        "Bilim ve Teknoloji": "https://news.google.com/topics/CAAqKAgKIiJDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSjBjaG9DVkZJb0FBUAE?hl=tr&gl=TR&ceid=TR%3Atr",
        "Eğlence": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr",
        "Spor": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr",
        "Sağlık": "https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FuUnlLQUFQAQ?hl=tr&gl=TR&ceid=TR%3Atr",
    }

    url = category_urls_map.get(category)

    if not url:
        result["Status"] = "Error"
        result["Message"] = f"Invalid category: {category}"
        return result

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        if connection.open:
            cursor = connection.cursor()

            # Extract data and write it to the MySQL database
            news_sections = soup.find_all('div', class_='EctEBd', jsname='rAluZb')

            news_data = []

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

                        # Insert data into the MySQL database
                        insert_query = 'INSERT INTO news.news_articles (category, source, url, short_description, publication_date) VALUES (%s, %s, %s, %s, %s)'
                        data = (category, source_text, news_url, summary_text, date_text)
                        cursor.execute(insert_query, data)
                        connection.commit()

            result["Status"] = "Success"
            result["Message"] = f"{category} data successfully inserted into the MySQL database."
            result[f"{category}Data"] = news_data

    except Error as e:
        result["Status"] = "Error"
        result["Message"] = f"MySQL Error: {e}"

    finally:
        if 'cursor' in locals():
            cursor.close()

    return result
