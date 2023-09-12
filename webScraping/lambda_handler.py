import requests
from bs4 import BeautifulSoup

# Google Haberler sitesinden veri çekme işlemi
url = "https://news.google.com/home?hl=tr&gl=TR&ceid=TR:tr"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Haberleri depolamak için boş bir liste oluşturun
haberler = []

# Kategorileri, kaynakları, URL'leri, kısa açıklamaları ve yayınlanma tarihlerini liste olarak kaydedin
news_sections = soup.find_all('div', class_='EctEBd')
sources = soup.find_all('div', class_='MCAGUe')
links = soup.find_all('a', class_='WwrzSb')
summaries = soup.find_all('h4', class_='gPFEn')
dates = soup.find_all('time', class_='hvbAAd')

for i, (category, source, link, summary, date) in enumerate(zip(news_sections, sources, links, summaries, dates), start=1):
    category_text = category.text.strip()
    source_div = source.find('div', class_='vr1PYe')

    if source_div:
        source_text = source_div.text.strip()
    else:
        source_text = "Kaynak bulunamadı"

    news_url = f"https://news.google.com{link['href']}" if link else "URL bulunamadı"
    summary_text = summary.text.strip() if summary else "Açıklama bulunamadı"
    date_text = date.get('datetime') if date else "Tarih bulunamadı"

    # Haberi bir sözlük olarak oluşturun ve haberler listesine ekleyin
    haber = {
        "Kategori": category_text,
        "Kaynak": source_text,
        "URL": news_url,
        "Kısa Açıklama": summary_text,
        "Yayınlanma Tarihi": date_text
    }
    haberler.append(haber)

# Tüm haberleri yazdırın
for i, haber in enumerate(haberler, start=1):
    print(f"{i}. Haber:")
    print(f"Kategori: {haber['Kategori']}")
    print(f"Kaynak: {haber['Kaynak']}")
    print(f"URL: {haber['URL']}")
    print(f"Kısa Açıklama: {haber['Kısa Açıklama']}")
    print(f"Yayınlanma Tarihi: {haber['Yayınlanma Tarihi']}")
    print("----------------------------------------")
