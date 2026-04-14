import time
from langchain_core.tools import tool

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@tool
def scrape_from_reddit(query:str,num_articles_to_scrape:int)->dict:
    """
    Scrapes the articles from Reddit based upon the user query.
    Args:
        query (str): The user query
        num_articles_to_scrape (int): The number of articles to scrape.
    Returns:
        dict: The scrapped articles.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
    options.add_argument("user-data-dir=/home/spiralmonster/.config/google-chrome/selenium-profile")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)


    query=query.split(" ")
    query="+".join(query)

    search_query=f"https://www.google.com/search?q={query}"

    try:

        driver.get(search_query)

        element = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(., 'Forums')]")
            )
        )

        element.click()
        time.sleep(2)

        results=wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,"a h3"))
        )

        reddit_clicked=False

        for r in results:
            parent=r.find_element(By.XPATH,"./ancestor::a")
            href=parent.get_attribute("href")

            if href and "reddit.com" in href:
                print("Opening:",href)
                parent.click()
                reddit_clicked=True
                break

        if not reddit_clicked:
            print("No Reddit link found")
            tool_response={
                "tool_name":"Reddit Scrapper",
                "tool_success":False,
                "tool_response":"No Reddit link found."
            }


        else:
            wait.until(EC.presence_of_element_located((By.TAG_NAME,"body")))
            time.sleep(3)

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(2)

            articles=[]
            try:
                posts=driver.find_elements(
                    By.XPATH,"//div[contains(@id,'post-rtjson-content')]"
                )

                for p in posts:
                    text=p.text
                    if text:
                        articles.append(text)

                    if len(articles)==num_articles_to_scrape:
                        break


                tool_response={
                    "tool_name": "Reddit Scrapper",
                    "tool_success": True,
                    "tool_response":articles
                }



            except:
                tool_response={
                    "tool_name": "Reddit Scrapper",
                    "tool_success": False,
                    "tool_response":"No articles found."
                }






    except:
        print("Error in scrapping the data")
        tool_response={
            "tool_name": "Reddit Scrapper",
            "tool_success": False,
            "tool_response":"Error in scrapping the data."
        }


    driver.quit()
    return tool_response



if __name__=="__main__":
    query="when is the best time to visit italy"
    tool_response=scrape_from_reddit.invoke(
        {
            "query":query,
            "num_articles_to_scrape":5
        }
    )

    if tool_response["tool_success"]:
        articles_scrapped=tool_response["tool_response"]
        for art in articles_scrapped:
            print(art)
            print("="*50)
            print()


    else:
        print(tool_response)







