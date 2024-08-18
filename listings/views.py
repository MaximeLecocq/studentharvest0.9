from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ListingForm
from .models import Listing
from users.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# def homepage(request):
#     listings = Listing.objects.all().order_by('-created_at')
#     return render(request, 'homepage.html', {'listings': listings})


# def homepage(request):
#     listings = Listing.objects.all().order_by('-created_at')
#     for listing in listings:
#         listing.categories_list = listing.categories.split(',')

#     return render(request, 'homepage.html', {'listings': listings})


# def homepage(request):
#     listings = Listing.objects.all().order_by('-created_at')
#     paginator = Paginator(listings, 10)  # Show 10 listings per page

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     for listing in page_obj:
#         listing.categories_list = listing.categories.split(',')

#     return render(request, 'homepage.html', {
#         'page_obj': page_obj
#     })




def homepage(request):
    query = request.GET.get('q')  # Get the search query from the navbar form input (if exists)
    
    if query:
        listings = Listing.objects.filter(title__icontains=query).order_by('-created_at')  # Filter listings by title
    else:
        listings = Listing.objects.all().order_by('-created_at')  # Default to show all listings
    
    paginator = Paginator(listings, 10)  # Paginate with 10 listings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for listing in page_obj:
        listing.categories_list = listing.categories.split(',')

    return render(request, 'homepage.html', {
        'page_obj': page_obj,
        'query': query  # Pass the search query to the template for display and to keep it in the search bar
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
            listing.categories = ','.join(form.cleaned_data['categories'])  # Join selected categories

            # Handle saving expiry dates for specific categories
            categories = form.cleaned_data['categories']
            if 'canned' in categories:
                listing.expiry_date_canned = form.cleaned_data['expiry_date_canned']
            if 'dry' in categories:
                listing.expiry_date_dry = form.cleaned_data['expiry_date_dry']
            if 'beverages' in categories:
                listing.expiry_date_beverages = form.cleaned_data['expiry_date_beverages']

            listing.save()  # Save listing with donor and expiry date information

            messages.success(request, 'Listing created successfully.')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()

    return render(request, 'listings/create_listing.html', {'form': form})


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    categories_list = listing.categories.split(',')
    is_owner = request.user == listing.donor

    context = {
        'listing': listing,
        'categories_list': categories_list,
        'is_owner': is_owner,
    }

    return render(request, 'listings/listing_detail.html', context)



# def donor_listings(request, donor_id):
#     donor = get_object_or_404(User, pk=donor_id)
#     listings = Listing.objects.filter(donor=donor).order_by('-created_at')
#     return render(request, 'listings/donor_listings.html', {
#         'donor': donor,
#         'listings': listings
#     })


def donor_listings(request, donor_id):
    donor = get_object_or_404(User, pk=donor_id)
    listings = Listing.objects.filter(donor=donor).order_by('-created_at')

    # Pagination
    paginator = Paginator(listings, 10)  # Show 10 listings per page
    page = request.GET.get('page')

    try:
        listings_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        listings_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        listings_page = paginator.page(paginator.num_pages)

    return render(request, 'listings/donor_listings.html', {
        'donor': donor,
        'listings': listings_page  # Use the paginated listings
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
    paginator = Paginator(favorites, 10)  # Show 10 favorite listings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listings/user_favorites.html', {'page_obj': page_obj})