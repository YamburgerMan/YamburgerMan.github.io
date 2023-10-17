import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_imdb_info(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    search_url = f"https://www.imdb.com/find?q={query}&s=tt&ttype=ft&ref_=fn_ft"
    
    print(f"Searching IMDb for: {query}")
    
    response = requests.get(search_url, headers=headers)
    time.sleep(5)  # Delay

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Locate the link for the top result based on the provided HTML structure
    results = soup.find_all('a', {'tabindex': '0'})

    for result in results:
        link = result.get('href')
        if link and "/title/" in link:  # Check if link is the one we are interested in
            link = "https://www.imdb.com" + link
            print(f"Fetching details from: {link}")
            return fetch_movie_details(link)
    
    print(f"No results found for: {query}")
    return None, None, None, None  # Ensure four values are returned

def fetch_movie_details(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    response = requests.get(link, headers=headers)
    time.sleep(2)  # Delay

    if response.status_code != 200:
        print(f"Failed to retrieve details for: {link}")
        return None, None, None, None  # Ensure four values are returned

    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('h1').text.strip()

    # Extract year and runtime from the ul list
    ul_list = soup.find('ul', class_='ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt')
    list_items = ul_list.find_all('li') if ul_list else []

    # Assuming the structure you mentioned holds true, we can fetch year and runtime directly
    year = list_items[0].get_text() if len(list_items) > 0 else None
    runtime = list_items[2].get_text() if len(list_items) > 2 else None

    return title, year, runtime,link

if __name__ == "__main__":
    df = pd.read_excel('input.xlsx')
    df['Full Title'], df['Year'], df['Runtime'],df['Link']  = zip(*df.iloc[:, 0].apply(get_imdb_info))
    
    df['HTML String'] = df.apply(lambda x: f'<a href="{x["Link"]}">{x["Full Title"]} ({x["Year"]}) -- {x["Runtime"]}</a><br><br>', axis=1)
    
    df.to_excel('output.xlsx', index=False)
