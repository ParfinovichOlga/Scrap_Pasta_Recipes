import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://food52.com/recipes/pasta?preview=true&recipe_landing_term=pasta&o=popular"
URL_BASE = "https://food52.com"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
    "84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(URL, headers=header)
print(response.status_code)

web_page = response.text
soup = BeautifulSoup(web_page, "html.parser")
recipes = soup.select('h3.collectable__name a')
rating_data = soup.select('div.rating > span')

recipes_titles = [recipe.getText() for recipe in recipes]
recipes_links = [URL_BASE+link.get('href') for link in recipes]
rating = [rating.getText().split('(')[1].split()[0] for rating in rating_data]

ingredients = []
cook_time = []

for link in recipes_links:
    resp = requests.get(link).text
    sp = BeautifulSoup(resp, "html.parser")
    total_info = sp.select('ul.recipe__details>li')
    ing = sp.select('div.recipe__list ul li')

    time = ', '.join([t.getText().replace('\n', '').replace('     ', ' ').rstrip() for t in total_info])
    cook_time.append(time)
    ingredient = ','.join([i.getText().replace('\n', '') for i in ing])
    ingredients.append(ingredient)


df = pd.DataFrame({'Titles': recipes_titles, 'Links': recipes_links, 'Time info': cook_time, 'Ingredients': ingredients,
                   'Rating': rating})

df.to_csv('pasta_recipes.csv')
