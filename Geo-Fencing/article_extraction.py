import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

edge_options = Options()
edge_options.add_argument("--headless")  
edge_driver_path = "C:/Users/rohan/OneDrive/Desktop/edgedriver_win64/msedgedriver.exe" 
service = Service(edge_driver_path)
driver = webdriver.Edge(service=service, options=edge_options) 

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def scrape_article(url):
    try:
        driver.get(url)
        time.sleep(3)  
        
        if driver.find_elements(By.TAG_NAME, 'item'):
            article_body = driver.find_element(By.TAG_NAME, 'item')
        elif driver.find_elements(By.TAG_NAME, 'article'):
            article_body = driver.find_element(By.TAG_NAME, 'article')
        elif driver.find_elements(By.TAG_NAME, 'div'):
            article_body = driver.find_element(By.TAG_NAME, 'div')
        elif driver.find_elements(By.TAG_NAME, 'body'):
            article_body = driver.find_element(By.TAG_NAME, 'body')
        else:
            print(f"No suitable tag found for {url}")
            return None

        return article_body.text

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def extract_incident_and_location(text):
    prompt = f"""Extract the incident type (e.g., molestation, assault, etc.) and the location 
    (e.g., city name) from the following article text. Respond ONLY with the incident type 
    and location in the format: 'incident_type, location, Chennai'. Example: 'Assault, T Nagar, Chennai'
    
    Article text: {text}"""
    
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "max_tokens": 100
        }
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        if response.status_code == 200:
            return response.json()['response'].strip()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"API Error: {str(e)}"

def process_urls(urls):
    extracted_data = []
    for url in urls:
        try:
            article_content = scrape_article(url)
            if article_content:
                extracted_info = extract_incident_and_location(article_content)
                extracted_data.append({
                    'URL': url,
                    'Extracted Info': extracted_info
                })
        except Exception as e:
            print(f"Error processing {url}: {e}")
            continue
    return extracted_data

df = pd.read_csv('women_safety_news_chennai.csv')
urls = df['link'].dropna().tolist() 

extracted_data = process_urls(urls)

df_extracted = pd.DataFrame(extracted_data)
df_extracted.to_csv('refined_articles.csv', index=False)

driver.quit()

print("Processing complete! Extracted data saved to refined_articles.csv.")
