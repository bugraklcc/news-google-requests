import matplotlib.pyplot as plt
import pymysql

# MySQL veritabanı bağlantısı
connection = pymysql.connect(
    host='database-1.cmbjzgj4iu72.us-east-1.rds.amazonaws.com',
    user='admin',
    password='password123.+',
    database='news'
)

# Kategorileri veritabanından al
category_query = """
SELECT DISTINCT category FROM news.news_articles;
"""

# Kategorileri al
with connection.cursor() as cursor:
    cursor.execute(category_query)
    categories = [row[0] for row in cursor.fetchall()]

# Fonksiyon: Veritabanı sorgusu çalıştırma ve sonuçları alma
def run_query(query, *params):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

# Kaynak, tarih ve saatlik analiz
source_results_all_categories = {}
date_results_all_categories = {}
hourly_results_all_categories = {}

for category in categories:
    source_query = """
    SELECT
        source,
        COUNT(*) AS news_count
    FROM
        news.news_articles
    WHERE
        category = %s
    GROUP BY
        source
    ORDER BY
        news_count DESC;
    """

    date_query = """
    SELECT
        DATE(publication_date) AS news_date,
        COUNT(*) AS news_count
    FROM
        news.news_articles
    WHERE
        category = %s
    GROUP BY
        news_date
    ORDER BY
        news_date;
    """

    hourly_query = """
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

    source_results = run_query(source_query, category)
    source_data = {row[0]: row[1] for row in source_results}

    date_results = run_query(date_query, category)
    date_data = {str(row[0]): row[1] for row in date_results}

    hourly_results = run_query(hourly_query, category)
    hourly_data = {row[0]: row[1] for row in hourly_results}

    source_results_all_categories[category] = source_data
    date_results_all_categories[category] = date_data
    hourly_results_all_categories[category] = hourly_data

# Kaynak Dağılımı Analizi Grafiği (Tek Bir Grafik)
plt.figure(figsize=(12, 6))
for category, data in source_results_all_categories.items():
    plt.bar(data.keys(), data.values(), label=category)

plt.xlabel('Kaynaklar')
plt.ylabel('Haber Sayısı')
plt.title('Tüm Kategoriler İçin Kaynak Dağılımı Analizi')
plt.xticks(rotation=45)  # Eksen etiketlerini 45 derece döndürme
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout(pad=0.5)  # Boşluğu azaltma
plt.show()

# Tarih Dağılımı Analizi Grafiği (Tek Bir Grafik)
plt.figure(figsize=(12, 6))
for category, data in date_results_all_categories.items():
    dates = list(data.keys())
    news_counts = list(data.values())
    plt.plot(dates, news_counts, marker='o', label=category)

plt.xlabel('Tarih')
plt.ylabel('Haber Sayısı')
plt.title('Tüm Kategoriler İçin Tarih Dağılımı Analizi')
plt.xticks(rotation=45)  # Eksen etiketlerini 45 derece döndürme
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout(pad=0.5)  # Boşluğu azaltma
plt.show()

# Saatlik Haber Sayısı Analizi Grafiği (Tek Bir Grafik)
plt.figure(figsize=(12, 6))
for category, data in hourly_results_all_categories.items():
    hours = list(data.keys())
    news_counts = list(data.values())
    plt.plot(hours, news_counts, marker='o', label=category)

plt.xlabel('Saat')
plt.ylabel('Haber Sayısı')
plt.title('Tüm Kategoriler İçin Saatlik Haber Sayısı Analizi')
plt.xticks(range(24))  # Saat etiketlerini 0'dan 23'e ayarlama
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout(pad=0.5)  # Boşluğu azaltma
plt.show()

# Veritabanı bağlantısını kapat
connection.close()
