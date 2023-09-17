import pandas as pd
import pymysql

# Veritabanı bağlantısını kur
connection = pymysql.connect(
    host='database-1.cmbjzgj4iu72.us-east-1.rds.amazonaws.com',
    user='admin',
    password='password123.+',
    database='news'
)

try:
    # Veritabanı ile etkileşim kurmak için bir cursor oluştur
    with connection.cursor() as cursor:
        # Veritabanından verileri al
        sql_query = "SELECT * FROM news.news_articles"  # "tablo_adı" kısmını mevcut tablonuzun adıyla değiştirin
        cursor.execute(sql_query)
        result = cursor.fetchall()

        # Verileri bir DataFrame'e yükleyin
        df = pd.DataFrame(result, columns=[i[0] for i in cursor.description])
        df['publication_date'] = pd.to_datetime(df['publication_date'])

        # DataFrame'i CSV dosyasına kaydet
        df.to_csv('new_result.csv', index=False, encoding='utf-8')

finally:
    # Bağlantıyı kapat
    connection.close()
