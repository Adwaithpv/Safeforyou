# Women's Safety Geo-Fencing Project

This project focuses on analyzing and visualizing women's safety incidents in Chennai through web scraping, data processing, and interactive mapping.

## Project Overview

The project consists of several components that work together to:
1. Scrape news articles related to women's safety incidents in Chennai
2. Extract and process relevant information about incidents and locations
3. Visualize crime hotspots on an interactive map
4. Generate refined datasets for analysis

## Project Structure

- `article_extraction.py`: Main script for scraping and processing news articles
- `webscraping.py`: Web scraping utilities
- `map.html`: Interactive map visualization of crime hotspots
- `women_safety_news_chennai.csv`: Raw dataset of news articles
- `refined_articles.csv`: Processed dataset with extracted information
- `refined_articles_cleaned.csv`: Cleaned and refined dataset

## Features

- **Web Scraping**: Automated extraction of news articles using Selenium
- **Natural Language Processing**: Extraction of incident types and locations using LLM (Llama3)
- **Interactive Mapping**: Visualization of crime hotspots using Leaflet.js
- **Data Processing**: Cleaning and refinement of extracted information

## Prerequisites

- Python 3.x
- Selenium WebDriver
- Edge WebDriver
- Required Python packages:
  - selenium
  - pandas
  - requests
- Ollama (for LLM processing)
- Web browser for viewing the interactive map

## Installation

1. Clone this repository
2. Install required Python packages:
   ```bash
   pip install selenium pandas requests
   ```
3. Download and install Edge WebDriver
4. Install Ollama and set up the Llama3 model

## Usage

1. Run the article extraction script:
   ```bash
   python article_extraction.py
   ```
2. View the interactive map by opening `map.html` in a web browser

## Data Processing Flow

1. The script reads URLs from `women_safety_news_chennai.csv`
2. For each URL:
   - Scrapes the article content
   - Extracts incident type and location using LLM
   - Processes and stores the information
3. Results are saved to `refined_articles.csv`
4. The interactive map displays crime hotspots based on the processed data

## Output Files

- `refined_articles.csv`: Contains processed data with URLs and extracted information
- `refined_articles_cleaned.csv`: Final cleaned dataset
- Interactive map showing crime hotspots in Chennai

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenStreetMap for map data
- News sources for providing the original articles
- Ollama for LLM capabilities 