"""
URL configuration for library_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views as ev
urlpatterns = [
    path('',ev.register,name='register'),
    path('login/',ev.login,name='login'),
    path('import_books/',ev.import_books,name='import_books'),
    path('book_list/',ev.book_list,name='book_list'),
    path('add_book/',ev.add_book,name='add_book'),
    path('update_book/<int:id>/',ev.updatebook,name='update_book'),
    path('delete_book/<int:id>/',ev.deletebook,name='delete_book'),



    path('add_member/',ev.add_member,name='add_member'),
    path('member_list/',ev.member_list,name='member_list'),
    path('update_member/<int:id>/',ev.updatemember,name='update_member'),
    path('delete_member/<int:id>/',ev.deletemember,name='delete_member'),

    path('issue_book/<int:book_id>/',ev.issue_book,name='issue_book'),
    path('return_book/<int:transaction_id>/',ev.return_book,name='return_book'),

    path('search_books/',ev.search_books,name='search_books'),
    path('transaction_lists/',ev.transaction_lists,name='transaction_lists'),

    path('logout/',ev.logout,name='logout'),

]
