import time
from langchain_core.tools import tool

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

options=Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
options.add_argument("user-data-dir=/home/spiralmonster/.config/google-chrome/selenium-profile")

driver=webdriver.Chrome(options=options)

wait=WebDriverWait(driver,timeout=15)


@tool
def scrape_from_quora(query:str,num_articles_to_scrape:int)->dict:
    """
    Scrapes the articles from Quora based upon the user query.
    Args:
        query (str): The user query
        num_articles_to_scrape (int): The number of articles to scrape.
    Returns:
        dict: The scrapped articles.
    """
    query=query.split(" ")
    query="+".join(query)

    search_query=f"https://www.google.com/search?q={query}"

    try:
        driver.get(search_query)

        element=wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,"//a[contains(., 'Forums')]")
            )
        )

        element.click()
        time.sleep(2)

        results=wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR,"a h3")
            )
        )

        quora_clicked=False

        for r in results:
            parent=r.find_element(By.XPATH,"./ancestor::a")
            href=parent.get_attribute("href")

            if href and "quora.com" in href:
                print("Opening: ",href)
                parent.click()
                quora_clicked=True
                break


        if quora_clicked:
            wait.until(
                EC.presence_of_element_located(
                    (By.TAG_NAME,"body")
                )
            )
            time.sleep(3)

            all_buttons = driver.find_elements(By.CSS_SELECTOR, ".q-click-wrapper.puppeteer_test_read_more_button")
            for button in all_buttons:
                driver.execute_script("arguments[0].click();", button)

            time.sleep(3)


            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(3)




            articles=[]
            related_questions=[]
            try:

                questions=driver.find_elements(
                    By.CSS_SELECTOR,".q-box.qu-cursor--pointer.qu-display--block.qu-hover--textDecoration--none.b2c1r2a.puppeteer_test_link"
                )
                for ques in questions:
                    ques=ques.text
                    if ques:
                        related_questions.append(ques)


                post = driver.find_elements(
                    By.CSS_SELECTOR, ".q-box.qu-userSelect--text"
                )

                ind=0

                while ind<len(post):
                    p=post[ind]
                    text=p.text
                    if text:
                        if text not in related_questions:
                            if "?" in text:
                                ind+=1

                            else:
                                articles.append(text)

                    if len(articles)==num_articles_to_scrape:
                        break

                    ind+=1



                tool_response={
                    "tool_name":"Quora Scrapper",
                    "tool_success":True,
                    "tool_response":articles
                }


            except Exception as e:
                print(e)
                tool_response={
                    "tool_name": "Quora Scrapper",
                    "tool_success": False,
                    "tool_response": "No articles found."
                }


        else:
            print("No Quora link found")
            tool_response={
                "tool_name": "Quora Scrapper",
                "tool_success": False,
                "tool_response": "No Quora link found."
            }



    except Exception as e:
        print(e)
        tool_response={
            "tool_name": "Quora Scrapper",
            "tool_success": False,
            "tool_response": "Error in scrapping the data."
        }


    driver.quit()

    return tool_response


if __name__=="__main__":
    query="when is the best time to visit Italy"
    tool_response=scrape_from_quora(query)

    if tool_response["tool_success"]:
        for article in tool_response["tool_response"]:
            print(article)
            print("=" * 50)
            print()


    else:
        print(tool_response)






