import pandas as pd
import pymysql


connection = pymysql.connect(
    host='database-1.cmbjzgj4iu72.us-east-1.rds.amazonaws.com',
    user='admin',
    password='password123.+',
    database='news'
)

try:

    with connection.cursor() as cursor:

        sql_query = "SELECT * FROM news.news_articles"  # "tablo_adı" kısmını mevcut tablonuzun adıyla değiştirin
        cursor.execute(sql_query)
        result = cursor.fetchall()

        df = pd.DataFrame(result, columns=[i[0] for i in cursor.description])
        df['publication_date'] = pd.to_datetime(df['publication_date'])

        df.to_excel('new_result.xlsx', index=False)

finally:

    connection.close()
