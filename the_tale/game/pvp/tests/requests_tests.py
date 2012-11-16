# coding: utf-8
from django.test import client
from django.core.urlresolvers import reverse

from dext.utils import s11n

from common.utils.testcase import TestCase

from accounts.prototypes import AccountPrototype
from accounts.logic import register_user

from game.logic import create_test_map
from game.pvp.models import BATTLE_1X1_STATE

from game.pvp.tests.helpers import PvPTestsMixin

class TestRequests(TestCase, PvPTestsMixin):

    def setUp(self):
        create_test_map()

        result, account_id, bundle_id = register_user('test_user', 'test_user@test.com', '111111')
        self.account_1_id = account_id
        self.account_1 = AccountPrototype.get_by_id(account_id)

        result, account_id, bundle_id = register_user('test_user_2', 'test_user_2@test.com', '111111')
        self.account_2_id = account_id
        self.account_2 = AccountPrototype.get_by_id(account_id)

        self.client = client.Client()

    def test_game_page_when_pvp_in_queue(self):
        self.pvp_create_battle(self.account_1, self.account_2)
        self.pvp_create_battle(self.account_2, self.account_1)
        self.request_login('test_user@test.com')
        self.check_redirect(reverse('game:pvp:'), reverse('game:'))

    def test_game_page_when_pvp_processing(self):
        self.pvp_create_battle(self.account_1, self.account_2, BATTLE_1X1_STATE.PROCESSING)
        self.pvp_create_battle(self.account_2, self.account_1, BATTLE_1X1_STATE.PROCESSING)
        self.request_login('test_user@test.com')
        self.check_html_ok(self.client.get(reverse('game:pvp:')))

    def test_game_info_when_pvp_in_queue(self):
        self.pvp_create_battle(self.account_1, self.account_2)
        self.pvp_create_battle(self.account_2, self.account_1)
        self.request_login('test_user@test.com')
        self.assertEqual(s11n.from_json(self.client.get(reverse('game:pvp:info')).content)['data']['mode'], 'pve')

    def test_game_info_when_pvp_processing(self):
        self.pvp_create_battle(self.account_1, self.account_2, BATTLE_1X1_STATE.PROCESSING)
        self.pvp_create_battle(self.account_2, self.account_1, BATTLE_1X1_STATE.PROCESSING)
        self.request_login('test_user@test.com')
        self.assertEqual(s11n.from_json(self.client.get(reverse('game:pvp:info')).content)['data']['mode'], 'pvp')
