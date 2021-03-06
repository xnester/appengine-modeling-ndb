# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test classes for code snippet for modeling article."""


import unittest

import parent_child_models as models
import test_base

from google.appengine.ext import ndb


class ContactTestCase(test_base.TestCase):
    """A test case for the Contact model class with KeyProperty."""
    NAME = 'Takashi Matsuo'
    def setUp(self):
        super(ContactTestCase, self).setUp()
        contact = models.Contact(name=self.NAME)
        contact.put()
        self.contact_key = contact.key

    def test_basic(self):
        """Test for getting a Contact entity."""
        contact = self.contact_key.get()
        self.assertEqual(contact.name, self.NAME)

    # [START succeeding_test]
    def test_success(self):
        contact = self.contact_key.get()
        models.PhoneNumber(parent=self.contact_key,
                           phone_type='home',
                           number='(650) 555 - 2200').put()
        numbers = contact.phone_numbers.fetch()
        self.assertEqual(1, len(numbers))
    # [START succeeding_test]

    def test_phone_numbers(self):
        """A test for 'phone_numbers' property."""
        models.PhoneNumber(parent=self.contact_key,
                           phone_type='home',
                           number='(650) 555 - 2200').put()
        models.PhoneNumber(parent=self.contact_key,
                           phone_type='mobile',
                           number='(650) 555 - 2201').put()
        contact = self.contact_key.get()
        for phone in contact.phone_numbers:
            # it doesn't ensure any order
            if phone.phone_type == 'home':
                self.assertEqual('(650) 555 - 2200', phone.number)
            elif phone.phone_type == 'mobile':
                self.assertEqual(phone.number, '(650) 555 - 2201')

        # filer the phone numbers by type. Note that this is an
        # ancestor query.
        query = contact.phone_numbers.filter(
            models.PhoneNumber.phone_type == 'home')
        entities = query.fetch()
        self.assertEqual(1, len(entities))
        self.assertEqual(entities[0].number, '(650) 555 - 2200')

        # delete the mobile phones
        query = contact.phone_numbers.filter(
            models.PhoneNumber.phone_type == 'mobile')
        ndb.delete_multi([e.key for e in query])

        # make sure there's no mobile phones any more
        query = contact.phone_numbers.filter(
            models.PhoneNumber.phone_type == 'mobile')
        entities = query.fetch()
        self.assertEqual(0, len(entities))


if __name__ == '__main__':
    unittest.main()
