from django.test import TestCase
from mailbag.models import MailBag, MailBagEntry

class AnimalTestCase(TestCase):
    def setUp(self):
        self.mailbag = MailBag(slug="foo")
        self.mailbag.save()
        self.mailbag_entry = MailBagEntry(id=1, mail_bag=self.mailbag)
        self.mailbag_entry.save()

    def test_absolute_url(self):
        """Mailbags have an abolute url. Mailbagentry url is #hash on same page."""
        
        mb_url = self.mailbag.get_absolute_url()
        mbe_url = self.mailbag_entry.get_absolute_url()
        self.assertTrue(mbe_url.startswith(mb_url + "#"))
