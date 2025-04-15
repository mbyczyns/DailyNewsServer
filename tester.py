import requests
from bs4 import BeautifulSoup

# Podaj URL artykułu, który chcesz pobrać
url = 'https://www.nytimes.com/2025/04/13/your-money/retirement-bessent-stock-market.html'

# Wykonaj zapytanie HTTP, aby pobrać stronę
response = requests.get(url)

# Sprawdź, czy zapytanie się powiodło
if response.status_code == 200:
    # Parsowanie zawartości strony HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Znajdź wszystkie elementy o klasie 'css-7nag3i e1wiw3jv0'
    elements = soup.find_all(class_="css-7nag3i e1wiw3jv0")

    # Sprawdź, czy znaleziono jakiekolwiek elementy
    if elements:
        for element in elements:
            # Pobierz tekst z każdego znalezionego elementu
            print(element.get_text())
    else:
        print("Nie znaleziono elementów o podanej klasie.")
else:
    print(f"Nie udało się pobrać strony. Status: {response.status_code}")