
import smart_imports

smart_imports.all()


WORLD_RESTRICTIONS = [questgen_restrictions.SingleLocationForObject(),
                      questgen_restrictions.ReferencesIntegrity()]
QUEST_RESTRICTIONS = [questgen_restrictions.SingleStartStateWithNoEnters(),
                      questgen_restrictions.FinishStateExists(),
                      questgen_restrictions.AllStatesHasJumps(),
                      questgen_restrictions.ConnectedStateJumpGraph(),
                      questgen_restrictions.NoCirclesInStateJumpGraph(),
                      questgen_restrictions.MultipleJumpsFromNormalState(),
                      questgen_restrictions.ChoicesConsistency(),
                      questgen_restrictions.QuestionsConsistency(),
                      questgen_restrictions.FinishResultsConsistency()]


QUESTS_BASE = questgen_quests_quests_base.QuestsBase()
QUESTS_BASE += [quest.quest_class for quest in relations.QUESTS.records]


class HeroQuestInfo(object):
    __slots__ = ('id',
                 'level',
                 'position_place_id',
                 'is_first_quest_path_required',
                 'preferences_mob_id',
                 'preferences_place_id',
                 'preferences_friend_id',
                 'preferences_enemy_id',
                 'preferences_equipment_slot',
                 'preferences_quests_region_id',
                 'preferences_quests_region_size',
                 'interfered_persons',
                 'quests_priorities',
                 'excluded_quests',
                 'prefered_quest_markers')

    def __init__(self,
                 id,
                 level,
                 position_place_id,
                 is_first_quest_path_required,
                 preferences_mob_id,
                 preferences_place_id,
                 preferences_friend_id,
                 preferences_enemy_id,
                 preferences_equipment_slot,
                 preferences_quests_region_id,
                 preferences_quests_region_size,
                 interfered_persons,
                 quests_priorities,
                 excluded_quests,
                 prefered_quest_markers):
        self.id = id
        self.level = level
        self.position_place_id = position_place_id
        self.is_first_quest_path_required = is_first_quest_path_required
        self.preferences_mob_id = preferences_mob_id
        self.preferences_place_id = preferences_place_id
        self.preferences_friend_id = preferences_friend_id
        self.preferences_enemy_id = preferences_enemy_id
        self.preferences_equipment_slot = preferences_equipment_slot
        self.preferences_quests_region_id = preferences_quests_region_id
        self.preferences_quests_region_size = preferences_quests_region_size
        self.interfered_persons = interfered_persons
        self.quests_priorities = quests_priorities
        self.excluded_quests = excluded_quests
        self.prefered_quest_markers = prefered_quest_markers

    @property
    def position_place(self):
        return places_storage.places[self.position_place_id]

    def serialize(self):
        return {'id': self.id,
                'level': self.level,
                'position_place_id': self.position_place_id,
                'is_first_quest_path_required': self.is_first_quest_path_required,
                'preferences_mob_id': self.preferences_mob_id,
                'preferences_place_id': self.preferences_place_id,
                'preferences_friend_id': self.preferences_friend_id,
                'preferences_enemy_id': self.preferences_enemy_id,
                'preferences_equipment_slot': self.preferences_equipment_slot.value if self.preferences_equipment_slot else None,
                'preferences_quests_region_id': self.preferences_quests_region_id if self.preferences_quests_region_id else None,
                'preferences_quests_region_size': self.preferences_quests_region_size,
                'interfered_persons': self.interfered_persons,
                'quests_priorities': [(quest_type.value, priority) for quest_type, priority in self.quests_priorities],
                'excluded_quests': list(sorted(self.excluded_quests)),
                'prefered_quest_markers': list(sorted(self.prefered_quest_markers))}

    @classmethod
    def deserialize(cls, data):
        return cls(id=data['id'],
                   level=data['level'],
                   position_place_id=data['position_place_id'],
                   is_first_quest_path_required=data['is_first_quest_path_required'],
                   preferences_mob_id=data['preferences_mob_id'],
                   preferences_place_id=data['preferences_place_id'],
                   preferences_friend_id=data['preferences_friend_id'],
                   preferences_enemy_id=data['preferences_enemy_id'],
                   preferences_equipment_slot=heroes_relations.EQUIPMENT_SLOT(data['preferences_equipment_slot']) if data['preferences_equipment_slot'] is not None else None,
                   preferences_quests_region_id=data['preferences_quests_region_id'],
                   preferences_quests_region_size=data['preferences_quests_region_size'],
                   interfered_persons=data['interfered_persons'],
                   quests_priorities=[(relations.QUESTS(quest_type), priority) for quest_type, priority in data['quests_priorities']],
                   excluded_quests=set(data['excluded_quests']),
                   prefered_quest_markers=set(data['prefered_quest_markers']))

    def __eq__(self, other):
        return self.serialize() == other.serialize()

    def __neq__(self, other):
        return not self.__eq__(other)


def choose_quest_path_url():
    return utils_urls.url('game:quests:api-choose', api_version='1.0', api_client=django_settings.API_CLIENT)


def fact_place(place):
    return questgen_facts.Place(uid=uids.place(place.id),
                                terrains=[terrain.value for terrain in place.terrains],
                                externals={'id': place.id},
                                type=place.modifier_quest_type())


def fact_mob(mob):
    return questgen_facts.Mob(uid=uids.mob(mob.id),
                              terrains=[terrain.value for terrain in mob.terrains],
                              externals={'id': mob.id})


def fact_person(person):
    return questgen_facts.Person(uid=uids.person(person.id),
                                 profession=person.type.quest_profession,
                                 externals={'id': person.id,
                                            'type': game_relations.ACTOR.PERSON.value})


def fact_emissary(emissary):
    return questgen_facts.Person(uid=uids.emissary(emissary.id),
                                 profession=None,
                                 externals={'id': emissary.id,
                                            'type': game_relations.ACTOR.EMISSARY.value})


def fact_social_connection(connection_type, person_uid, connected_person_uid):
    return questgen_facts.SocialConnection(person_to=person_uid,
                                           person_from=connected_person_uid,
                                           type=connection_type.questgen_type)


def fact_located_in(person):
    return questgen_facts.LocatedIn(object=uids.person(person.id), place=uids.place(person.place.id))


def fill_places(kb, places):
    for place in places:
        uid = uids.place(place.id)

        if uid in kb:
            continue

        kb += fact_place(place)


def setup_places(kb, hero_info):
    center_place_id = hero_info.position_place_id
    quests_region_size = hero_info.preferences_quests_region_size

    if hero_info.preferences_quests_region_id is not None:
        center_place_id = hero_info.preferences_quests_region_id

    if hero_info.is_first_quest_path_required:
        quests_region_size = 2

    places = places_storage.places.nearest_places(center_place_id,
                                                  number=quests_region_size)

    if len(places) < 2:
        places = places_storage.places.all()

    fill_places(kb, places)

    hero_position_uid = uids.place(hero_info.position_place_id)

    if hero_position_uid not in kb:
        kb += fact_place(places_storage.places[hero_info.position_place_id])

    kb += questgen_facts.LocatedIn(object=uids.hero(hero_info.id), place=hero_position_uid)


def setup_person(kb, person):

    if uids.place(person.place.id) not in kb:
        kb += fact_place(person.place)

    person_uid = uids.person(person.id)

    if person_uid in kb:
        return kb[person_uid]

    f_person = fact_person(person)

    kb += f_person
    kb += fact_located_in(person)

    return f_person


def setup_persons(kb, hero_info):
    for person in persons_storage.persons.all():

        if uids.place(person.place.id) not in kb:
            continue

        setup_person(kb, person)


def setup_social_connections(kb):
    persons_in_kb = {f_person.externals['id']: f_person.uid for f_person in kb.filter(questgen_facts.Person)}

    for person_id, person_uid in persons_in_kb.items():
        person = persons_storage.persons[person_id]

        for connection_type, connected_person_id in persons_storage.social_connections.get_person_connections(person):
            if connected_person_id not in persons_in_kb:
                continue
            kb += fact_social_connection(connection_type, person_uid, persons_in_kb[connected_person_id])


def setup_preferences(kb, hero_info):
    hero_uid = uids.hero(hero_info.id)

    if hero_info.preferences_mob_id is not None:
        f_mob = fact_mob(mobs_storage.mobs[hero_info.preferences_mob_id])
        if f_mob.uid not in kb:
            kb += f_mob
        kb += questgen_facts.PreferenceMob(object=hero_uid, mob=f_mob.uid)

    if hero_info.preferences_place_id is not None:
        f_place = fact_place(places_storage.places[hero_info.preferences_place_id])
        if f_place.uid not in kb:
            kb += f_place
        kb += questgen_facts.PreferenceHometown(object=hero_uid, place=f_place.uid)

    if hero_info.preferences_friend_id is not None:
        friend = persons_storage.persons[hero_info.preferences_friend_id]

        f_person = setup_person(kb, friend)

        kb += questgen_facts.PreferenceFriend(object=hero_uid, person=f_person.uid)
        kb += questgen_facts.ExceptBadBranches(object=f_person.uid)

    if hero_info.preferences_enemy_id:
        enemy = persons_storage.persons[hero_info.preferences_enemy_id]

        f_person = setup_person(kb, enemy)

        kb += questgen_facts.PreferenceEnemy(object=hero_uid, person=f_person.uid)
        kb += questgen_facts.ExceptGoodBranches(object=f_person.uid)

    if hero_info.preferences_equipment_slot:
        kb += questgen_facts.PreferenceEquipmentSlot(object=hero_uid, equipment_slot=hero_info.preferences_equipment_slot.value)


def get_knowledge_base(hero_info, without_restrictions=False):  # pylint: disable=R0912

    kb = questgen_knowledge_base.KnowledgeBase()

    hero_uid = uids.hero(hero_info.id)

    kb += questgen_facts.Hero(uid=hero_uid, externals={'id': hero_info.id})

    setup_places(kb, hero_info)
    setup_persons(kb, hero_info)
    setup_preferences(kb, hero_info)
    setup_social_connections(kb)

    if not without_restrictions:

        for person in persons_storage.persons.all():
            if person.place.id == hero_info.position_place_id and person.id in hero_info.interfered_persons:
                kb += questgen_facts.NotFirstInitiator(person=uids.person(person.id))

    kb.validate_consistency(WORLD_RESTRICTIONS)

    kb += [questgen_facts.UpgradeEquipmentCost(money=prototypes.QuestPrototype.upgrade_equipment_cost(hero_info))]

    return kb


def create_random_quest_for_hero(hero_info, logger):
    constructor = place_quest_constructor_fabric(place=hero_info.position_place,
                                                 person_action=None)

    return create_random_quest_with_constructor(hero_info,
                                                constructor,
                                                logger,
                                                excluded_quests=hero_info.excluded_quests,
                                                no_restrictions_on_fail=True)


def create_random_quest_for_place(hero_info, place, person_action, logger):

    constructor = place_quest_constructor_fabric(place=place,
                                                 person_action=person_action)

    excluded_quests = [record.quest_class.TYPE
                       for record in relations.QUESTS.records
                       if not record.allowed_for_cards]

    return create_random_quest_with_constructor(hero_info,
                                                constructor,
                                                logger,
                                                excluded_quests=excluded_quests,
                                                no_restrictions_on_fail=False)


def create_random_quest_for_person(hero_info, person, person_action, logger):

    constructor = person_quest_constructor_fabric(person=person,
                                                  person_action=person_action)

    excluded_quests = [record.quest_class.TYPE
                       for record in relations.QUESTS.records
                       if not record.allowed_for_cards]

    return create_random_quest_with_constructor(hero_info,
                                                constructor,
                                                logger,
                                                excluded_quests=excluded_quests,
                                                no_restrictions_on_fail=False)


def create_random_quest_for_emissary(hero_info, emissary, person_action, logger):
    constructor = emissary_quest_constructor_fabric(emissary=emissary,
                                                    person_action=person_action)

    excluded_quests = [record.quest_class.TYPE
                       for record in relations.QUESTS.records
                       if not record.allowed_for_cards]

    return create_random_quest_with_constructor(hero_info,
                                                constructor,
                                                logger,
                                                excluded_quests=excluded_quests,
                                                no_restrictions_on_fail=False)


def create_random_quest_with_constructor(hero_info, constructor, logger, excluded_quests, no_restrictions_on_fail):

    start_time = time.time()

    normal_mode = True

    quests = utils_logic.shuffle_values_by_priority(hero_info.quests_priorities)

    logger.info('hero[%(hero_id).6d]: try is_normal: %(is_normal)s (allowed: %(allowed)s) (excluded: %(excluded)s)' %
                {'hero_id': hero_info.id,
                 'is_normal': normal_mode,
                 'allowed': ', '.join(quest.quest_class.TYPE for quest in quests),
                 'excluded': ', '.join(excluded_quests)})

    quest_type, knowledge_base = try_to_create_random_quest_for_hero(hero_info,
                                                                     quests,
                                                                     excluded_quests,
                                                                     without_restrictions=False,
                                                                     constructor=constructor,
                                                                     logger=logger)

    if knowledge_base is None and no_restrictions_on_fail:
        logger.info('hero[%(hero_id).6d]: first try failed' % {'hero_id': hero_info.id})
        normal_mode = False
        quest_type, knowledge_base = try_to_create_random_quest_for_hero(hero_info,
                                                                         quests,
                                                                         excluded_quests=[],
                                                                         without_restrictions=True,
                                                                         constructor=constructor,
                                                                         logger=logger)

    spent_time = time.time() - start_time

    logger.info('hero[%(hero_id).6d]: %(spent_time)s is_normal: %(is_normal)s %(quest_type)20s (allowed: %(allowed)s) (excluded: %(excluded)s)' %
                {'hero_id': hero_info.id,
                 'spent_time': spent_time,
                 'is_normal': normal_mode,
                 'quest_type': quest_type,
                 'allowed': ', '.join(quest.quest_class.TYPE for quest in quests),
                 'excluded': ', '.join(excluded_quests)})

    return knowledge_base


def try_to_create_random_quest_for_hero(hero_info, quests, excluded_quests, without_restrictions, constructor, logger):

    for quest_type in quests:
        if quest_type.quest_class.TYPE in excluded_quests:
            continue

        try:
            return quest_type, _create_random_quest_for_hero(hero_info,
                                                             constructor=constructor,
                                                             start_quests=[quest_type.quest_class.TYPE],
                                                             without_restrictions=without_restrictions)
        except questgen_exceptions.RollBackError as e:
            logger.info('hero[%(hero_id).6d]: can not create quest <%(quest_type)s>: %(exception)s' %
                        {'hero_id': hero_info.id,
                         'quest_type': quest_type,
                         'exception': e})
            continue

    return None, None


@utils_decorators.retry_on_exception(max_retries=conf.settings.MAX_QUEST_GENERATION_RETRIES,
                                     exceptions=[questgen_exceptions.RollBackError])
def _create_random_quest_for_hero(hero_info, constructor, start_quests, without_restrictions=False):
    knowledge_base = get_knowledge_base(hero_info, without_restrictions=without_restrictions)

    selector = questgen_selectors.Selector(knowledge_base, QUESTS_BASE, social_connection_probability=0)

    knowledge_base += constructor(selector, start_quests)

    questgen_transformators.activate_events(knowledge_base)  # TODO: after remove restricted states
    questgen_transformators.remove_restricted_states(knowledge_base)
    questgen_transformators.remove_broken_states(knowledge_base)  # MUST be called after all graph changes
    questgen_transformators.determine_default_choices(knowledge_base, preferred_markers=hero_info.prefered_quest_markers)  # MUST be called after all graph changes and on valid graph
    questgen_transformators.remove_unused_actors(knowledge_base)

    knowledge_base.validate_consistency(WORLD_RESTRICTIONS)
    knowledge_base.validate_consistency(QUEST_RESTRICTIONS)

    return knowledge_base


def place_quest_constructor_fabric(place, person_action):

    def constructor(selector, start_quests):
        f_place = fact_place(place)

        if f_place.uid not in selector._kb:
            selector._kb += f_place

        if person_action is not None:
            if person_action.is_HELP:
                selector._kb += questgen_facts.OnlyGoodBranches(object=f_place.uid)

            elif person_action.is_HARM:
                selector._kb += questgen_facts.OnlyBadBranches(object=f_place.uid)

            for person in place.persons:
                f_person = setup_person(selector._kb, person)

                if person_action.is_HELP:
                    remove_help_restrictions(selector._kb, f_person.uid, f_place.uid)
                    selector._kb += questgen_facts.OnlyGoodBranches(object=f_person.uid)

                elif person_action.is_HARM:
                    remove_harm_restrictions(selector._kb, f_person.uid, f_place.uid)
                    selector._kb += questgen_facts.OnlyBadBranches(object=f_person.uid)

        selector.reserve(f_place)

        return selector.create_quest_from_place(nesting=0,
                                                initiator_position=f_place,
                                                allowed=start_quests,
                                                excluded=[],
                                                tags=('can_start', ))

    return constructor


def emissary_quest_constructor_fabric(emissary, person_action):

    def constructor(selector, start_quests):
        f_emissary = fact_emissary(emissary)
        f_emissary_place = fact_place(emissary.place)

        selector._kb += f_emissary
        selector._kb += questgen_facts.LocatedIn(object=f_emissary.uid, place=uids.place(emissary.place_id))

        if f_emissary_place.uid not in selector._kb:
            selector._kb += f_emissary_place

        if person_action.is_HELP:
            remove_help_restrictions(selector._kb, f_emissary.uid, f_emissary_place.uid)
            selector._kb += questgen_facts.OnlyGoodBranches(object=f_emissary.uid)
        elif person_action.is_HARM:
            remove_harm_restrictions(selector._kb, f_emissary.uid, f_emissary_place.uid)
            selector._kb += questgen_facts.OnlyBadBranches(object=f_emissary.uid)
        else:
            raise NotImplementedError

        selector.reserve(f_emissary)
        selector.reserve(f_emissary_place)

        return selector.create_quest_from_person(nesting=0,
                                                 initiator=f_emissary,
                                                 allowed=start_quests,
                                                 excluded=[],
                                                 tags=('can_start', ))

    return constructor


def remove_restrictions(kb, Fact, object_uid):
    to_remove = []

    for fact in kb.filter(Fact):
        if fact.object == object_uid:
            to_remove.append(fact)

    kb -= to_remove


def remove_help_restrictions(kb, person_uid, place_uid):
    remove_restrictions(kb, questgen_facts.OnlyBadBranches, place_uid)
    remove_restrictions(kb, questgen_facts.ExceptGoodBranches, place_uid)

    remove_restrictions(kb, questgen_facts.OnlyBadBranches, person_uid)
    remove_restrictions(kb, questgen_facts.ExceptGoodBranches, person_uid)


def remove_harm_restrictions(kb, person_uid, place_uid):
    remove_restrictions(kb, questgen_facts.OnlyGoodBranches, place_uid)
    remove_restrictions(kb, questgen_facts.ExceptBadBranches, place_uid)

    remove_restrictions(kb, questgen_facts.OnlyGoodBranches, person_uid)
    remove_restrictions(kb, questgen_facts.ExceptBadBranches, person_uid)


def person_quest_constructor_fabric(person, person_action):

    def constructor(selector, start_quests):

        place_uid = uids.place(person.place_id)

        f_person = setup_person(selector._kb, person)

        if person_action.is_HELP:
            remove_help_restrictions(selector._kb, f_person.uid, place_uid)
            selector._kb += questgen_facts.OnlyGoodBranches(object=f_person.uid)

        elif person_action.is_HARM:
            remove_harm_restrictions(selector._kb, f_person.uid, place_uid)
            selector._kb += questgen_facts.OnlyBadBranches(object=f_person.uid)

        else:
            raise NotImplementedError

        selector.reserve(f_person)
        selector.reserve(selector._kb[place_uid])

        return selector.create_quest_from_person(nesting=0,
                                                 initiator=f_person,
                                                 allowed=start_quests,
                                                 excluded=[],
                                                 tags=('can_start', ))

    return constructor


def create_hero_info(hero):
    quests_priorities = hero.get_quests_priorities()

    return HeroQuestInfo(id=hero.id,
                         level=hero.level,
                         position_place_id=hero.position.cell().nearest_place_id,
                         is_first_quest_path_required=hero.is_first_quest_path_required,
                         preferences_mob_id=hero.preferences.mob.id if hero.preferences.mob else None,
                         preferences_place_id=hero.preferences.place.id if hero.preferences.place else None,
                         preferences_friend_id=hero.preferences.friend.id if hero.preferences.friend else None,
                         preferences_enemy_id=hero.preferences.enemy.id if hero.preferences.enemy else None,
                         preferences_equipment_slot=hero.preferences.equipment_slot,
                         preferences_quests_region_id=hero.preferences.quests_region.id if hero.preferences.quests_region else None,
                         preferences_quests_region_size=hero.preferences.quests_region_size,
                         interfered_persons=hero.quests.get_interfered_persons(),
                         quests_priorities=quests_priorities,
                         excluded_quests=hero.quests.excluded_quests(len(quests_priorities) // 2),
                         prefered_quest_markers=hero.prefered_quest_markers())


def request_quest_for_hero(hero, emissary_id=None, place_id=None, person_id=None, person_action=None):
    hero_info = create_hero_info(hero)
    amqp_environment.environment.workers.quests_generator.cmd_request_quest(hero.account_id,
                                                                            hero_info.serialize(),
                                                                            emissary_id=emissary_id,
                                                                            place_id=place_id,
                                                                            person_id=person_id,
                                                                            person_action=person_action)


def setup_quest_for_hero(hero, knowledge_base_data):

    # do nothing if hero has already had quest
    if not hero.actions.current_action.searching_quest:
        return

    knowledge_base = questgen_knowledge_base.KnowledgeBase.deserialize(knowledge_base_data, fact_classes=questgen_facts.FACTS)

    states_to_percents = questgen_analysers.percents_collector(knowledge_base)

    quest = prototypes.QuestPrototype(hero=hero, knowledge_base=knowledge_base, states_to_percents=states_to_percents)

    # устанавливаем квест перед его началом,
    # чтобы он корректно записался в стек
    hero.actions.current_action.setup_quest(quest)

    if quest.machine.can_do_step():
        quest.machine.step()  # do first step to setup pointer

        # заставляем героя выполнить условия стартового узла задания
        # необходимо для случая, когда квест инициирует игрок и героя не находится в точке начала задания
        quest.machine.check_requirements(quest.machine.current_state)
        quest.machine.satisfy_requirements(quest.machine.current_state)



def extract_person_type(fact):
    return game_relations.ACTOR(fact.externals.get('type', game_relations.ACTOR.PERSON.value))
