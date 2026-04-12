import time
from langchain_core.tools import tool

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options=Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
options.add_argument("user-data-dir=/home/spiralmonster/.config/google-chrome/selenium-profile")


driver=webdriver.Chrome(options=options)

wait=WebDriverWait(driver,timeout=15)

def scrape_pages(driver):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(2)

    news_articles=[]
    publishing_time=[]

    articles = driver.find_elements(
        By.CSS_SELECTOR, ".n0jPhd.y9Qqsf.ynAwRc.MBeuO"
    )

    for article in articles:
        text = article.text
        if text:
            news_articles.append(text)

    time_elements = driver.find_elements(
        By.CSS_SELECTOR, ".OSrXXb.rbYSKb.LfVVr"
    )

    for t in time_elements:
        text = t.text
        if text:
            publishing_time.append(text)


    return news_articles,publishing_time


@tool
def scrape_news_articles(query:str,num_articles_to_scrape:int)->dict:
    """
    Scrapes the news articles based upon the user query
    Args:
        query (str): The user query
        num_articles_to_scrape (int): The number of articles to scrape.
    Returns:
        dict: The scrapped news articles.

    """
    query=query.split(" ")
    query="+".join(query)

    search_query=f"https://www.google.com/search?q={query}"

    try:
        news_articles=[]
        publishing_time=[]

        driver.get(search_query)

        for page in range(1,3):
            print(f"Scrapping news from Page {page}")

            if page==1:
                element=wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH,"//a[contains(.,'News')]")
                    )
                )
                element.click()
                time.sleep(2)



            else:
                element=wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH,f"//a[@aria-label='Page {page}']")
                    )
                )
                element.click()
                time.sleep(2)

            articles, pub_time = scrape_pages(driver)
            news_articles.extend(articles)
            publishing_time.extend(pub_time)

            news_articles=news_articles[:num_articles_to_scrape]
            publishing_time=publishing_time[:num_articles_to_scrape]


        response=[]
        for t,article in zip(publishing_time,news_articles):
            resp={
                "news_article":article,
                "published":t
            }
            response.append(resp)



        tool_response={
            "tool_name":"News Scrapper",
            "tool_success":True,
            "tool_response":response
        }


    except Exception as e:
        print(e)
        print("Error in scrapping news articles.")

        tool_response = {
            "tool_name": "News Scrapper",
            "tool_success": False,
            "tool_response": "Error in scrapping news articles."
        }

    driver.quit()

    return tool_response


if __name__=="__main__":
    query="latest news in Italy"
    tool_response=scrape_news_articles(query)

    if tool_response["tool_success"]:
        for resp in tool_response["tool_response"]:
            print(f"Published: {resp['published']}")
            print(f"News: {resp['news_article']}")
            print("=" * 50)
            print()


    else:
        print(tool_response)





