from sports_scraper import scrape_sports_news
from scrape_turkey_news import scrape_turkey_news
from scrape_world_news import scrape_world_news
from scrape_local_news import scrape_local_news
from scrape_business_news import scrape_business_news
from scrape_science_and_tech_news import scrape_science_and_tech_news
from scrape_entertainment_news import scrape_entertainment_news
from scrape_health_news import scrape_health_news


def lambda_handler(event, context):
    turkey_result = scrape_turkey_news()
    world_result = scrape_world_news()
    local_result = scrape_local_news()
    business_result = scrape_business_news()
    sports_result = scrape_sports_news()
    science_and_tech_result = scrape_science_and_tech_news()
    entertainment_result = scrape_entertainment_news()
    health_result = scrape_health_news()
    final_result = {
        "TurkeyResult": turkey_result,
        "WorldResult": world_result,
        "LocalResult": local_result,
        "BusinessResult": business_result,
        "SportsResult": sports_result,
        "ScienceAndTechResult": science_and_tech_result,
        "EntertainmentResult": entertainment_result,
        "HealthResult": health_result,
    }

    return final_result
