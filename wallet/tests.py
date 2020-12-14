from django.test import TestCase, Client
from django.shortcuts import reverse

test2_url = reverse('test2')

class ClientTest(TestCase):
    c = Client()

    def test2(self):
        r = self.c.get(test2_url, follow=True)
        print(r.redirect_chain)