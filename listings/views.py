from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .forms import ListingForm, SearchForm
from .models import Listing
from .utils import get_ingredients_from_listing

import requests


def homepage(request):
    title_query = request.GET.get('title', '')
    city_query = request.GET.get('city', '')
    selected_categories = request.GET.getlist('categories')

    #start with the base queryset
    listings = Listing.objects.all().order_by('-created_at')  #sort by newest listings first

    #apply title search
    if title_query:
        listings = listings.filter(title__icontains=title_query)

    #apply city search
    if city_query:
        listings = listings.filter(city__icontains=city_query)

    #apply category search with OR condition
    if selected_categories:
        queries = Q()
        for category in selected_categories:
            queries |= Q(categories__icontains=category)
        listings = listings.filter(queries)



    #pagination
    paginator = Paginator(listings, 9)  #show 6 listings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    for listing in page_obj:
        listing.categories_list = listing.categories.split(',')

    #render the page with the filtered listings
    return render(request, 'homepage.html', {
        'page_obj': page_obj,
        'search_form': SearchForm(request.GET),
        'selected_categories': selected_categories
    })


@login_required
def create_listing(request):
    if request.user.role != 'donor':
        messages.error(request, 'Only donors can create listings.')
        return redirect('home')

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.donor = request.user
            listing.categories = ','.join(form.cleaned_data['categories'])  #join selected categories


            #ensure at least one image is uploaded (image1 is mandatory)
            if 'image1' not in request.FILES:
                messages.error(request, 'At least one image is required.')
                return render(request, 'listings/create_listing.html', {'form': form})


            #handle saving expiry dates for specific categories
            categories = form.cleaned_data['categories']
            if 'canned' in categories:
                listing.expiry_date_canned = form.cleaned_data['expiry_date_canned']
            if 'dry' in categories:
                listing.expiry_date_dry = form.cleaned_data['expiry_date_dry']
            if 'beverages' in categories:
                listing.expiry_date_beverages = form.cleaned_data['expiry_date_beverages']

            listing.save()  #save listing with donor and expiry date information

            messages.success(request, 'Listing created successfully.')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()

    return render(request, 'listings/create_listing.html', {'form': form})


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    categories_list = listing.categories.split(',')
    is_owner = request.user == listing.donor

    #extract ingredients from listing description
    ingredients = ','.join(get_ingredients_from_listing(listing))  #adapt based on your logic

    #fetch recipe suggestions based on ingredients
    recipes = get_recipe_suggestions(ingredients)

    context = {
        'listing': listing,
        'categories_list': categories_list,
        'is_owner': is_owner,
        'recipes': recipes,  #add recipes to context
    }

    return render(request, 'listings/listing_detail.html', context)



def donor_listings(request, donor_id):
    donor = get_object_or_404(User, pk=donor_id)
    listings = Listing.objects.filter(donor=donor).order_by('-created_at')

    #pagination
    paginator = Paginator(listings, 9)  #show 6 listings per page
    page = request.GET.get('page')

    try:
        listings_page = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer, deliver first page.
        listings_page = paginator.page(1)
    except EmptyPage:
        #if page is out of range, deliver last page of results.
        listings_page = paginator.page(paginator.num_pages)

    return render(request, 'listings/donor_listings.html', {
        'donor': donor,
        'listings': listings_page  #use the paginated listings
    })



@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.user != listing.donor:
        messages.error(request, "You are not allowed to edit this listing.")
        return redirect('listing_detail', pk=pk)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():

            if not listing.image1 and 'image1' not in request.FILES:
                messages.error(request, 'At least one image is required.')
                return render(request, 'listings/edit_listing.html', {'form': form})
                
            form.save()
            messages.success(request, 'Listing updated successfully.')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)

    return render(request, 'listings/edit_listing.html', {'form': form})


@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    
    if request.method == 'POST':
        if request.user == listing.donor:
            listing.delete()
            messages.success(request, 'Listing deleted successfully.')
            return redirect('homepage')
        else:
            messages.error(request, 'You do not have permission to delete this listing.')
            return redirect('listing_detail', pk=pk)
    
    return render(request, 'listings/confirm_delete.html', {'listing': listing})


@login_required
def add_to_favorites(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.user in listing.favorites.all():
        messages.info(request, "This listing is already in your favorites.")
    else:
        listing.favorites.add(request.user)
        messages.success(request, "Added to your favorites!")
    return redirect(request.META.get('HTTP_REFERER', 'homepage'))

@login_required
def remove_from_favorites(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.user in listing.favorites.all():
        listing.favorites.remove(request.user)
        messages.success(request, "Removed from your favorites.")
    else:
        messages.info(request, "This listing is not in your favorites.")
    return redirect(request.META.get('HTTP_REFERER', 'homepage'))

@login_required
def user_favorites(request):
    favorites = request.user.favorite_listings.all()
    paginator = Paginator(favorites, 9)  #show 6 favorite listings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listings/user_favorites.html', {'page_obj': page_obj})


def get_recipe_suggestions(ingredients):
    api_key = 'edae9cc8988d4cf18a9f7adf2642416a'
    response = requests.get(
        f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=5&apiKey={api_key}'
    )
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        #handle API errors or lack of data
        return []



#recipe_suggestions view that dynamically come from a form
def recipe_suggestions(request):
    #get ingredients from the query parameters if provided, otherwise default to an empty string
    ingredients = request.GET.get('ingredients', '')
    
    if ingredients:
        #call the recipe suggestion function with the user-provided ingredients
        recipes = get_recipe_suggestions(ingredients)
    else:
        #if no ingredients provided, display an empty list or a message
        recipes = []

    return render(request, 'recipes/recipe_suggestions.html', {'recipes': recipes, 'ingredients': ingredients})
