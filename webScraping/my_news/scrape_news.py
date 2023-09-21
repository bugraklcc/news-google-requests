import json
import requests
from bs4 import BeautifulSoup
import pymysql
from pymysql import Error


# Function to read the configuration file
def read_config_file(config_file_path):
    try:
        with open(config_file_path, "r", encoding="utf-8") as config_file:
            config_data = json.load(config_file)
        return config_data
    except FileNotFoundError:
        print("Config file not found.")
        return None
    except json.JSONDecodeError:
        print("Config file is in an invalid JSON format.")
        return None


# Function to get the category-url mapping from the configuration
def get_category_url_map(config=None):
    if not config:
        config = read_config_file("config.json")  # Default path for the config file

    return config.get("category_url_map", {})


# Function to scrape news articles from a given category and URL
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


# Function to create a database connection
def create_connection(db_host, db_user, db_password, db_database):
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )
    return connection


# Function to insert scraped news data into a database
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


if __name__ == "__main__":
    # Read the configuration file
    config = read_config_file("config.json")  # Default path for the config file
    category_url_map = get_category_url_map(config)

    all_news = []

    # Scrape news data for each category and store it in the all_news list
    for category, url in category_url_map.items():
        scrape_result = scrape_news(category, url)
        all_news += scrape_result.get(f"{category}Data", [])

    # Convert the scraped data to JSON format and print it
    json_data = json.dumps(all_news, indent=4, ensure_ascii=False)
    print(json_data)

    # Get database configuration from the config file
    db_config = config.get("db_config", {})

    db_host = db_config.get("host", "")
    db_user = db_config.get("user", "")
    db_password = db_config.get("password", "")
    db_database = db_config.get("database", "")

    # Create a database connection
    connection = create_connection(db_host, db_user, db_password, db_database)

    if connection:
        print("Database connection successfully established.")
        # Insert scraped news data into the database
        insert_to_db(connection, all_news)
    else:
        print("Database connection could not be established.")
