#extract ingredients from the listing's title and description
def get_ingredients_from_listing(listing):
    title_ingredients = listing.title.split(' ')
    description_ingredients = listing.description.split(' ')
    
    #combine both title and description ingredients
    ingredients = title_ingredients + description_ingredients
    
    #remove any empty strings and return the list of ingredients
    return [ingredient for ingredient in ingredients if ingredient.strip()]
