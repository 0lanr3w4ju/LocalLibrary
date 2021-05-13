from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Book, Author, BookInstance, Genre, Language
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# from django.views import generic


# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_of_genres = Genre.objects.count()

    num_of_languages = Language.objects.count()

    num_of_word_occurrence = Book.objects.filter(title__iexact='Angels and Demons').count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_of_genres': num_of_genres,
        'num_of_languages': num_of_languages,
        'num_of_word_occurrence': num_of_word_occurrence,
        'num_visits': num_visits
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(ListView):
    model = Book
    context_object_name = 'my_book_list'
    paginate_by = 1


class BookDetailView(DetailView):
    model = Book


class AuthorListView(ListView):
    model = Author
    context_object_name = 'my_author_list'
    paginate_by = 1


class AuthorDetailView(DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(burrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedOutBooks(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/burrowed_out_books_list.html'
    permission_required = 'catalog.can_view_books_burrowed'
    paginate_by = 3

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o')
