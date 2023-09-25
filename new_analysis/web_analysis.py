import matplotlib.pyplot as plt
import pymysql

# MySQL veritabanı bağlantısı
connection = pymysql.connect(
    host='database-1.cmbjzgj4iu72.us-east-1.rds.amazonaws.com',
    user='admin',
    password='password123.+',
    database='news'
)

categories = input(
    "Analiz yapmak istediğiniz kategorileri virgülle ayırarak girin (örneğin: Spor,Teknoloji,Ekonomi): ").split(',')


# Fonksiyon: Veritabanı sorgusu çalıştırma ve sonuçları alma
def run_query(query, *params):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


# Kaynak Dağılımı Analizi SQL Sorgusu
source_query = """
SELECT
    category,
    source,
    COUNT(*) AS news_count
FROM
    news.news_articles
WHERE
    category IN %s
GROUP BY
    category, source
ORDER BY
    news_count DESC;
"""

# Tarih Dağılımı Analizi SQL Sorgusu
date_query = """
SELECT
    category,
    DATE(publication_date) AS news_date,
    COUNT(*) AS news_count
FROM
    news.news_articles
WHERE
    category IN %s
GROUP BY
    category, news_date
ORDER BY
    news_date;
"""

hourly_news_query = """
SELECT
    HOUR(publication_date) AS hour,
    COUNT(*) AS news_count
FROM
    news.news_articles
WHERE
    category = %s
GROUP BY
    hour
ORDER BY
    hour;
"""

# En Popüler Haberler SQL Sorgusu
popular_news_query = """
SELECT
    category,
    source,
    url,
    short_description,
    publication_date
FROM
    news.news_articles
ORDER BY
    publication_date DESC
LIMIT 10;
"""

# Kaynak ve Tarih Dağılımı sonuçlarını saklamak için sözlükler
source_results = {}
date_results = {}

# Kaynak Dağılımı Analizi
source_data = run_query(source_query, tuple(categories))
for row in source_data:
    category = row[0]
    source = row[1]
    count = row[2]
    if category not in source_results:
        source_results[category] = {}
    source_results[category][source] = count

# Tarih Dağılımı Analizi
date_data = run_query(date_query, tuple(categories))
for row in date_data:
    category = row[0]
    date = str(row[1])
    count = row[2]
    if category not in date_results:
        date_results[category] = {"dates": [], "counts": []}
    date_results[category]["dates"].append(date)
    date_results[category]["counts"].append(count)

# Kategorilere Göre Saatlik Haber Sayısı Analizi ve Grafiği
for category in categories:
    hourly_results = run_query(hourly_news_query, category)
    hourly_hours = [result[0] for result in hourly_results]
    hourly_news_count = [result[1] for result in hourly_results]

    # Saatlik haber sayısı grafiği
    plt.figure(figsize=(10, 6))
    plt.bar(hourly_hours, hourly_news_count)
    plt.xlabel('Saat')
    plt.ylabel('Haber Sayısı')
    plt.title(f'Saatlik {category} Haber Sayısı Grafiği')
    plt.xticks(hourly_hours)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# En Popüler Haberler
popular_news_data = run_query(popular_news_query)
popular_news_results = []

for row in popular_news_data:
    category = row[0]
    source = row[1]
    url = row[2]
    short_description = row[3]
    publication_date = row[4]
    popular_news_results.append({
        "category": category,
        "source": source,
        "url": url,
        "short_description": short_description,
        "publication_date": publication_date
    })

# Veri Görselleştirmeleri

# Kategorilere Göre Kaynak Dağılımı Grafiği
for category, data in source_results.items():
    plt.figure(figsize=(12, 6))
    plt.bar(data.keys(), data.values())
    plt.xlabel('Kaynaklar')
    plt.ylabel('Haber Sayısı')
    plt.title(f'{category} Kategorisi Kaynak Dağılımı Analizi')
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Kategorilere Göre Tarih Dağılımı Grafiği
for category, data in date_results.items():
    dates = data["dates"]
    news_counts = data["counts"]
    plt.figure(figsize=(12, 6))
    plt.plot(dates, news_counts, marker='o')
    plt.xlabel('Tarih')
    plt.ylabel('Haber Sayısı')
    plt.title(f'{category} Kategorisi Tarih Dağılımı Analizi')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# En Popüler Haberler Grafiği
popular_news_categories = [news["category"] for news in popular_news_results]
popular_news_view_counts = [news["publication_date"] for news in popular_news_results]

plt.figure(figsize=(12, 6))
plt.barh(popular_news_categories, popular_news_view_counts, color='skyblue')
plt.xlabel('Görüntülenme Sayısı')
plt.ylabel('Haber Kategorileri')
plt.title('En Popüler Haberler')
plt.gca().invert_yaxis()  # Kategorileri tersten sırala
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# En Popüler Haberler Tablosu
print("En Popüler Haberler: \n")
for i, news in enumerate(popular_news_results, start=1):
    print(f"{i}. Kategori: {news['category']}")
    print(f"Kaynak: {news['source']}")
    print(f"URL: {news['url']}")
    print(f"Kısa Açıklama: {news['short_description']}")
    print(f"Yayın Tarihi: {news['publication_date']}\n")
