from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from django.shortcuts import render
from lists.models import Item
import re

def remove_csrf_tag(text):
	return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)


class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render(request, 'home.html').content.decode()
		self.assertEqual(remove_csrf_tag(response.content.decode()), remove_csrf_tag(expected_html))

	def test_home_page_can_save_a_POST_request(self):
		#Setup
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'
		
		#Exercise
		response = home_page(request)

		#Assert
		self.assertIn('A new list item', response.content.decode())	
		expected_html = render(request, 'home.html',  
			{'new_item_text': 'A new list item'} ).content.decode()
		self.assertEqual( remove_csrf_tag(response.content.decode()), remove_csrf_tag(expected_html))

class ItemModelTest(TestCase):

	def test_saving_and_retriving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'The second item'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, 'The second item')
