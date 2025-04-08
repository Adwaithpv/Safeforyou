import time  # To add delay for page loading
import requests  # To send HTTP requests to the LLM API
import pandas as pd  # For handling CSVs and tabular data
from selenium import webdriver  # For web automation and scraping
from selenium.webdriver.common.by import By  # To locate HTML elements
from selenium.webdriver.edge.service import Service  # For managing the Edge WebDriver service
from selenium.webdriver.edge.options import Options  # To configure Edge browser options

# Set Edge browser options to run in headless mode (no UI)
edge_options = Options()
edge_options.add_argument("--headless")

# Set up the path to the Edge WebDriver
edge_driver_path = "C:/Users/rohan/OneDrive/Desktop/edgedriver_win64/msedgedriver.exe"
service = Service(edge_driver_path)

# Initialize the Edge WebDriver with the specified options
driver = webdriver.Edge(service=service, options=edge_options)

# URL for local LLaMA3 API (Ollama server) that processes prompts
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Function to scrape article content from a given URL
def scrape_article(url):
    try:
        driver.get(url)  # Open the URL in the browser
        time.sleep(3)  # Wait for the content to load
        
        # Try different HTML tags that might contain the article content
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

        # Return the text content of the found tag
        return article_body.text

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Function to extract incident type and location from article text using LLaMA3
def extract_incident_and_location(text):
    prompt = f"""Extract the incident type (e.g., molestation, assault, etc.) and the location 
    (e.g., city name) from the following article text. Respond ONLY with the incident type 
    and location in the format: 'incident_type, location, Chennai'. Example: 'Assault, T Nagar, Chennai'
    
    Article text: {text}"""
    
    # Construct API request payload
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
        # Send POST request to the local LLaMA3 API
        response = requests.post(OLLAMA_API_URL, json=payload)
        if response.status_code == 200:
            return response.json()['response'].strip()  # Return clean extracted result
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"API Error: {str(e)}"

# Function to process a list of URLs and extract structured info
def process_urls(urls):
    extracted_data = []
    for url in urls:
        try:
            article_content = scrape_article(url)  # Scrape content
            if article_content:
                extracted_info = extract_incident_and_location(article_content)  # Extract info using LLM
                extracted_data.append({
                    'URL': url,
                    'Extracted Info': extracted_info
                })
        except Exception as e:
            print(f"Error processing {url}: {e}")
            continue
    return extracted_data

# Load list of article URLs from previously saved CSV
df = pd.read_csv('women_safety_news_chennai.csv')
urls = df['link'].dropna().tolist()

# Extract incident-related information from each article
extracted_data = process_urls(urls)

# Save the structured extracted information to a new CSV file
df_extracted = pd.DataFrame(extracted_data)
df_extracted.to_csv('refined_articles.csv', index=False)

# Close the Selenium browser session
driver.quit()

# Notify completion
print("Processing complete! Extracted data saved to refined_articles.csv.")
