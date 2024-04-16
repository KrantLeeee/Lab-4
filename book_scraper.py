import requests
from bs4 import BeautifulSoup

# Base URL of the site
base_url = 'https://books.toscrape.com/catalogue'
page = 1

books = []

while True:
    URL = f'{base_url}/page-{page}.html'
    print(f'Scraping page {page}')
    response = requests.get(URL)

    # If the page doesn't exist, break the loop
    if response.status_code == 404:
        break
    
    soup = BeautifulSoup(response.text, 'html.parser')
    book_divs = soup.select('ol.row > li.col-xs-6.col-sm-4.col-md-3.col-lg-3')  # Corrected CSS selector

    for book_div in book_divs:
        title = book_div.select_one('h3 a')['title']
        relative_url = book_div.select_one('h3 a')['href']
        book_url = f'{base_url}/{relative_url}'
        book_response = requests.get(book_url)
        book_soup = BeautifulSoup(book_response.text, 'html.parser')

        description = book_soup.select_one('article.product_page p').text
        price = book_div.select_one('p.price_color').text
        rating = book_div.select_one('p.star-rating')['class'][1]

        books.append({'title': title, 'description': description, 'price': price, 'rating': rating})

    page += 1

# Print or process your collected book data
for book in books:
    print(book)
