import requests
from bs4 import BeautifulSoup
import pymysql
from pymysql import Error


def scrape_science_and_tech_news():
    connection = pymysql.connect(
        host='database-1.cmbjzgj4iu72.us-east-1.rds.amazonaws.com',
        user='admin',
        password='password123.+',
        database='news'
    )

    result = {}

    # Bilim ve Teknoloji kategorisi için URL'yi tanımla
    url = "https://news.google.com/topics/CAAqKAgKIiJDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSjBjaG9DVkZJb0FBUAE?hl=tr&gl=TR&ceid=TR%3Atr"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        if connection.open:
            cursor = connection.cursor()

            # Verileri çıkar ve MySQL veritabanına yaz
            news_sections = soup.find_all('a', class_='brSCsc', jsname='sCfAK')

            science_and_tech_data = []

            for section in news_sections:
                category_text = section.text.strip()

                if category_text == "Bilim ve Teknoloji":
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
                            source_text = "Kaynak bulunamadı"

                        news_url = f"https://news.google.com{link['href']}" if link else "URL bulunamadı"
                        summary_text = summary.text.strip() if summary else "Açıklama bulunamadı"
                        date_text = date.get('datetime') if date else "Tarih bulunamadı"

                        news_item = {
                            "Category": "Bilim ve Teknoloji",
                            # Kategoriyi sabit olarak "Bilim ve Teknoloji" olarak ayarlayın
                            "Source": source_text,
                            "URL": news_url,
                            "ShortDescription": summary_text,
                            "PublicationDate": date_text
                        }

                        science_and_tech_data.append(news_item)

                        # Verileri MySQL veritabanına ekleyin
                        insert_query = 'INSERT INTO news.news_articles (category, source, url, short_description, publication_date) VALUES (%s, %s, %s, %s, %s)'
                        data = ("Bilim ve Teknoloji", source_text, news_url, summary_text, date_text)
                        cursor.execute(insert_query, data)
                        connection.commit()

            result["Status"] = "Başarılı"
            result["Message"] = "Bilim ve Teknoloji haberleri başarıyla MySQL veritabanına eklenmiştir."
            result["ScienceAndTechData"] = science_and_tech_data

    except Error as e:
        result["Status"] = "Hata"
        result["Message"] = f"MySQL Hatası: {e}"

    finally:
        if 'cursor' in locals():
            cursor.close()

    return result


if __name__ == "__main__":
    scrape_science_and_tech_news()
