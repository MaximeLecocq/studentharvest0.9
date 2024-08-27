from django.shortcuts import render
import requests
from .utils import get_ingredients_from_listing

#this function interacts with the Spoonacular API to get recipe suggestions based on a list of ingredients.
#it sends a request to the API with the ingredients and retrieves up to 5 recipes.
def get_recipe_suggestions(ingredients):
    api_key = 'edae9cc8988d4cf18a9f7adf2642416a'
    #send GET request to the Spoonacular API with the list of ingredients and the API key
    response = requests.get(
        f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=5&apiKey={api_key}'
    )
    #check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        #if the API request fails or returns an error, return an empty list
        return []

#this view renders a page with recipe suggestions based on hardcoded ingredients.
#it gets a list of recipes from the get_recipe_suggestions function and displays them.
def recipe_suggestions(request):
    ingredients = "tomato,onion"
    #get recipe suggestions based on the ingredients
    recipes = get_recipe_suggestions(ingredients)
    return render(request, 'recipes/recipe_suggestions.html', {'recipes': recipes})
