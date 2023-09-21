from my_news.scrape_news import read_config_file, get_category_url_map, scrape_news, create_connection, insert_to_db


def lambda_handler(event, context):
    config = read_config_file("my_news/config.json")
    if config is None:
        return "Configuration file not found."

    category_url_map = get_category_url_map(config)

    all_news = []

    for category, url in category_url_map.items():
        scrape_result = scrape_news(category, url)
        all_news += scrape_result.get(f"{category}Data", [])

    db_config = config.get("db_config", {})

    db_host = db_config.get("host", "")
    db_user = db_config.get("user", "")
    db_password = db_config.get("password", "")
    db_database = db_config.get("database", "")

    connection = create_connection(db_host, db_user, db_password, db_database)
    if connection:
        insert_to_db(connection, all_news)
        return "The data has been added successfully.", all_news
    else:
        return "Could not create database connection."
