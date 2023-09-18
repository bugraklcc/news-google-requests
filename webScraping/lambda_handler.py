from my_news.scrape_news import scrape_news


def lambda_handler(event, context):
    categories = ["Türkiye", "Dünya", "Yerel", "İş", "Bilim ve Teknoloji", "Eğlence", "Spor", "Sağlık"]
    final_result = {}

    for category in categories:
        scrape_result = scrape_news(category)
        final_result[f"{category}Result"] = scrape_result

    return final_result
