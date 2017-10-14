# coding: utf-8
from unittest import mock

from the_tale.amqp_environment import environment

from the_tale.common.utils import testcase
from the_tale.common.utils.permissions import sync_group

from the_tale.accounts import logic as accounts_logic

from the_tale.accounts.personal_messages import tt_api as pm_tt_api
from the_tale.accounts.personal_messages.tests import helpers as pm_helpers

from the_tale.accounts.achievements.relations import ACHIEVEMENT_GROUP, ACHIEVEMENT_TYPE
from the_tale.accounts.achievements.prototypes import AchievementPrototype, AccountAchievementsPrototype, GiveAchievementTaskPrototype

from the_tale.game.heroes import logic as heroes_logic


from the_tale.game.logic import create_test_map



class AchievementsManagerTests(testcase.TestCase, pm_helpers.Mixin):

    def setUp(self):
        super(AchievementsManagerTests, self).setUp()

        create_test_map()

        self.account_1 = self.accounts_factory.create_account()
        self.account_2 = self.accounts_factory.create_account()

        group_edit = sync_group('edit achievement', ['achievements.edit_achievement'])

        group_edit.user_set.add(self.account_2._model)

        self.achievement_1 = AchievementPrototype.create(group=ACHIEVEMENT_GROUP.MONEY, type=ACHIEVEMENT_TYPE.MONEY, barrier=0, points=10,
                                                         caption='achievement_1', description='description_1', approved=True)
        self.achievement_2 = AchievementPrototype.create(group=ACHIEVEMENT_GROUP.MONEY, type=ACHIEVEMENT_TYPE.MONEY, barrier=5, points=10,
                                                         caption='achievement_2', description='description_2', approved=False)
        self.achievement_3 = AchievementPrototype.create(group=ACHIEVEMENT_GROUP.TIME, type=ACHIEVEMENT_TYPE.DEATHS, barrier=4, points=10,
                                                         caption='achievement_3', description='description_3', approved=True)


        self.account_achievements_1 = AccountAchievementsPrototype.get_by_account_id(self.account_1.id)
        self.account_achievements_1.achievements.add_achievement(self.achievement_1)
        self.account_achievements_1.save()

        self.worker = environment.workers.achievements_manager
        self.worker.initialize()

        pm_tt_api.debug_clear_service()

    def test_add_achievements__not_tasks(self):
        self.worker.add_achievements()
        self.account_achievements_1.reload()
        self.assertEqual(len(self.account_achievements_1.achievements), 1)

    def test_add_achievements(self):
        GiveAchievementTaskPrototype.create(account_id=self.account_1.id, achievement_id=self.achievement_3.id)
        self.assertFalse(self.account_achievements_1.has_achievement(self.achievement_3))

        with self.check_new_message(self.account_1.id, [accounts_logic.get_system_user_id()]):
            self.worker.add_achievements()

        self.account_achievements_1.reload()
        self.assertTrue(self.account_achievements_1.has_achievement(self.achievement_3))
        self.assertEqual(GiveAchievementTaskPrototype._db_count(), 0)


    @mock.patch('the_tale.accounts.achievements.storage.AchievementsStorage.verify_achievements', lambda *argv, **kwargs: None)
    def test_add_achievements__all_accounts(self):

        GiveAchievementTaskPrototype.create(account_id=None, achievement_id=self.achievement_3.id)

        account_achievements_2 = AccountAchievementsPrototype.get_by_account_id(self.account_2.id)

        self.assertFalse(self.account_achievements_1.has_achievement(self.achievement_3))
        self.assertFalse(account_achievements_2.has_achievement(self.achievement_3))
        hero = heroes_logic.load_hero(account_id=self.account_1.id)
        hero.statistics.change_pve_deaths(self.achievement_3.barrier)
        heroes_logic.save_hero(hero)

        with self.check_no_messages(self.account_2.id):
            with self.check_no_messages(self.account_1.id):
                self.worker.add_achievements()

        self.account_achievements_1.reload()
        account_achievements_2.reload()

        self.assertTrue(self.account_achievements_1.has_achievement(self.achievement_3))
        self.assertFalse(account_achievements_2.has_achievement(self.achievement_3))

        self.assertEqual(GiveAchievementTaskPrototype._db_count(), 0)

    @mock.patch('the_tale.accounts.achievements.storage.AchievementsStorage.verify_achievements', lambda *argv, **kwargs: None)
    def test_add_achievements__all_accounts__not_remove_already_received_achievements(self):
        self.account_achievements_1.achievements.add_achievement(self.achievement_3)
        self.account_achievements_1.save()

        GiveAchievementTaskPrototype.create(account_id=None, achievement_id=self.achievement_3.id)

        account_achievements_2 = AccountAchievementsPrototype.get_by_account_id(self.account_2.id)

        self.assertTrue(self.account_achievements_1.has_achievement(self.achievement_3))
        self.assertFalse(account_achievements_2.has_achievement(self.achievement_3))

        with self.check_no_messages(self.account_2.id):
            with self.check_no_messages(self.account_1.id):
                self.worker.add_achievements()

        self.account_achievements_1.reload()
        account_achievements_2.reload()

        self.assertTrue(self.account_achievements_1.has_achievement(self.achievement_3))
        self.assertFalse(account_achievements_2.has_achievement(self.achievement_3))

        self.assertEqual(GiveAchievementTaskPrototype._db_count(), 0)

    def test_legendary_achievements(self):
        achievement_4 = AchievementPrototype.create(group=ACHIEVEMENT_GROUP.LEGENDS, type=ACHIEVEMENT_TYPE.LEGENDS, barrier=0, points=0,
                                                    caption='achievement_4', description='description_4', approved=True)

        self.account_achievements_1.achievements.add_achievement(achievement_4)
        self.account_achievements_1.save()

        GiveAchievementTaskPrototype.create(account_id=None, achievement_id=achievement_4.id)

        account_achievements_2 = AccountAchievementsPrototype.get_by_account_id(self.account_2.id)

        self.assertTrue(self.account_achievements_1.has_achievement(achievement_4))
        self.assertFalse(account_achievements_2.has_achievement(achievement_4))

        with self.check_no_messages(self.account_2.id):
            with self.check_no_messages(self.account_1.id):
                self.worker.add_achievements()

        self.account_achievements_1.reload()
        account_achievements_2.reload()

        self.assertTrue(self.account_achievements_1.has_achievement(achievement_4))
        self.assertFalse(account_achievements_2.has_achievement(achievement_4))

        self.assertEqual(GiveAchievementTaskPrototype._db_count(), 0)
