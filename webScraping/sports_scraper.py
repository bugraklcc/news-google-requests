import requests
from bs4 import BeautifulSoup
import pymysql
from pymysql import Error


def scrape_sports_news():
    connection = pymysql.connect(
        host='database-1.cmbjzgj4iu72.us-east-1.rds.amazonaws.com',
        user='admin',
        password='password123.+',
        database='news'
    )

    result = {}

    # Doğrudan spor kategorisi için URL'yi tanımla
    url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        if connection.open:
            cursor = connection.cursor()

            # Extract data and write it to the MySQL database
            news_sections = soup.find_all('div', class_='EctEBd', jsname='rAluZb')

            sports_data = []

            for section in news_sections:
                category_text = section.text.strip()

                if category_text == "Spor":
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
                            "Category": "Spor",  # Kategoriyi sabit olarak "Spor" olarak ayarlayın
                            "Source": source_text,
                            "URL": news_url,
                            "ShortDescription": summary_text,
                            "PublicationDate": date_text
                        }

                        sports_data.append(news_item)

                        # Insert data into the MySQL database
                        insert_query = 'INSERT INTO news.news_articles (category, source, url, short_description, publication_date) VALUES (%s, %s, %s, %s, %s)'
                        data = ("Spor", source_text, news_url, summary_text, date_text)
                        cursor.execute(insert_query, data)
                        connection.commit()

            result["Status"] = "Success"
            result["Message"] = "Sports data successfully inserted into the MySQL database."
            result["SportsData"] = sports_data

    except Error as e:
        result["Status"] = "Error"
        result["Message"] = f"MySQL Error: {e}"

    finally:
        if 'cursor' in locals():
            cursor.close()

    return result


if __name__ == "__main__":
    scrape_sports_news()
