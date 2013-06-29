# coding: utf-8

import mock
import datetime
import random

from game.bills.prototypes import BillPrototype, VotePrototype
from game.bills.bills import PlaceResourceExchange

from game.bills.tests.prototype_tests import BaseTestPrototypes

from game.map.places.storage import resource_exchange_storage
from game.map.places.relations import RESOURCE_EXCHANGE_TYPE


class PlaceResourceExchangeTests(BaseTestPrototypes):

    def setUp(self):
        super(PlaceResourceExchangeTests, self).setUp()

        self.resource_1, self.resource_2 = self.choose_resources()

        self.bill_data = PlaceResourceExchange(place_1_id=self.place1.id,
                                               place_2_id=self.place2.id,
                                               resource_1=self.resource_1,
                                               resource_2=self.resource_2)

        self.bill = BillPrototype.create(self.account1, 'bill-1-caption', 'bill-1-rationale', self.bill_data)

    def choose_resources(self):
        resource_1, resource_2 = RESOURCE_EXCHANGE_TYPE.NONE, RESOURCE_EXCHANGE_TYPE.NONE
        while resource_1.parameter == resource_2.parameter:
            resource_1 = random.choice(RESOURCE_EXCHANGE_TYPE._records)
            resource_2 = random.choice(RESOURCE_EXCHANGE_TYPE._records)
        return resource_1, resource_2

    def test_create(self):
        self.assertEqual(self.bill.data.place_1_id, self.place1.id)
        self.assertEqual(self.bill.data.place_2_id, self.place2.id)
        self.assertEqual(self.bill.data.resource_1, self.resource_1)
        self.assertEqual(self.bill.data.resource_2, self.resource_2)
        self.assertEqual(self.bill.data.old_place_1_name_forms, self.place1.normalized_name)
        self.assertEqual(self.bill.data.old_place_2_name_forms, self.place2.normalized_name)

        self.assertEqual(self.bill.data.place_1.id, self.place1.id)
        self.assertEqual(self.bill.data.place_2.id, self.place2.id)

        self.assertEqual(self.bill.data.old_place_1_name, self.place1.normalized_name.normalized)
        self.assertEqual(self.bill.data.old_place_2_name, self.place2.normalized_name.normalized)

        self.assertFalse(self.bill.data.place_1_name_changed)
        self.assertFalse(self.bill.data.place_2_name_changed)


    def test_user_form_initials(self):
        self.assertEqual(self.bill.data.user_form_initials,
                         {'place_1': self.bill.data.place_1_id,
                          'place_2': self.bill.data.place_2_id,
                          'resource_1': self.bill.data.resource_1,
                          'resource_2': self.bill.data.resource_2})

    def test_actors(self):
        self.assertEqual(set(id(a) for a in self.bill_data.actors), set([id(self.place1), id(self.place2)]))

    def test_update(self):
        form = self.bill.data.get_user_form_update(post={'caption': 'new-caption',
                                                         'rationale': 'new-rationale',
                                                         'place_1': self.place2.id,
                                                         'place_2': self.place1.id,
                                                         'resource_1': self.resource_2,
                                                         'resource_2': self.resource_1})
        self.assertTrue(form.is_valid())

        self.bill.update(form)

        self.bill = BillPrototype.get_by_id(self.bill.id)

        self.assertEqual(self.bill.data.place_1_id, self.place2.id)
        self.assertEqual(self.bill.data.place_2_id, self.place1.id)
        self.assertEqual(self.bill.data.resource_1, self.resource_2)
        self.assertEqual(self.bill.data.resource_2, self.resource_1)
        self.assertEqual(self.bill.data.old_place_1_name_forms, self.place2.normalized_name)
        self.assertEqual(self.bill.data.old_place_2_name_forms, self.place1.normalized_name)

        self.assertEqual(self.bill.data.place_1.id, self.place2.id)
        self.assertEqual(self.bill.data.place_2.id, self.place1.id)

        self.assertEqual(self.bill.data.old_place_1_name, self.place2.normalized_name.normalized)
        self.assertEqual(self.bill.data.old_place_2_name, self.place1.normalized_name.normalized)

        self.assertFalse(self.bill.data.place_2_name_changed)
        self.assertFalse(self.bill.data.place_1_name_changed)


    def test_form_validation__success(self):
        form = self.bill.data.get_user_form_update(post={'caption': 'long caption',
                                                         'rationale': 'long rationale',
                                                         'place_1': self.place1.id,
                                                         'place_2': self.place2.id,
                                                         'resource_1': self.resource_1,
                                                         'resource_2': self.resource_2})
        self.assertTrue(form.is_valid())

    def test_user_form_validation__not_connected(self):
        form = self.bill.data.get_user_form_update(post={'caption': 'caption',
                                                         'rationale': 'rationale',
                                                         'place_1': self.place1.id,
                                                         'place_2': self.place3.id,
                                                         'resource_1': self.resource_2,
                                                         'resource_2': self.resource_1})
        self.assertFalse(form.is_valid())

    @mock.patch('game.balance.constants.PLACE_MAX_EXCHANGED_NUMBER', 0)
    def test_user_form_validation__maximum_exchanges_reached(self):
        form = self.bill.data.get_user_form_update(post={'caption': 'caption',
                                                         'rationale': 'rationale',
                                                         'place_1': self.place1.id,
                                                         'place_2': self.place2.id,
                                                         'resource_1': self.resource_1,
                                                         'resource_2': self.resource_2})
        self.assertFalse(form.is_valid())

    def test_user_form_validation__equal_parameters(self):
        form = self.bill.data.get_user_form_update(post={'caption': 'caption',
                                                         'rationale': 'rationale',
                                                         'place_1': self.place1.id,
                                                         'place_2': self.place2.id,
                                                         'resource_1': self.resource_1,
                                                         'resource_2': self.resource_1})
        self.assertFalse(form.is_valid())

    @mock.patch('game.bills.conf.bills_settings.MIN_VOTES_PERCENT', 0.6)
    @mock.patch('game.bills.prototypes.BillPrototype.time_before_end_step', datetime.timedelta(seconds=0))
    def test_apply(self):
        VotePrototype.create(self.account2, self.bill, False)
        VotePrototype.create(self.account3, self.bill, True)

        form = PlaceResourceExchange.ModeratorForm({'approved': True})
        self.assertTrue(form.is_valid())
        self.bill.update_by_moderator(form)

        old_storage_version = resource_exchange_storage._version

        self.assertEqual(len(resource_exchange_storage.all()), 0)

        self.assertTrue(self.bill.apply())

        self.assertNotEqual(old_storage_version, resource_exchange_storage._version)
        self.assertEqual(len(resource_exchange_storage.all()), 1)

        bill = BillPrototype.get_by_id(self.bill.id)
        self.assertTrue(bill.state._is_ACCEPTED)

        exchange = resource_exchange_storage.all()[0]

        self.assertEqual(set([exchange.place_1.id, exchange.place_2.id]), set([self.place1.id, self.place2.id]))
        self.assertEqual(set([exchange.resource_1, exchange.resource_2]), set([self.resource_1, self.resource_2]))
        self.assertEqual(exchange.bill_id, bill.id)
