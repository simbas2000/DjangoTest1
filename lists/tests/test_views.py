from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from django.shortcuts import render
from django.utils.html import escape
from lists.models import Item, List
import re


def remove_csrf_tag(text):
    return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        # Setup
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        # Assert
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        # Setup
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        # Assert
        list_ = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/{}/'.format(list_.id))

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='l2_:item 1', list=other_list)
        Item.objects.create(text='l2_:item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id))

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'l2_:item 1')
        self.assertNotContains(response, 'l2_:item 2')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post('/lists/{}/'.format(correct_list.id), data={'item_text': 'New item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'New item')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post('/lists/{}/'.format(correct_list.id), data={'item_text': 'New item'})
        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render(request, 'home.html').content.decode()
        self.assertEqual(remove_csrf_tag(response.content.decode()), remove_csrf_tag(expected_html))
