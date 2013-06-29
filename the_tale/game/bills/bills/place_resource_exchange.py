# coding: utf-8

from django.forms import ValidationError

from textgen.words import Noun

from dext.forms import fields

from game.balance import constants as c

from game.bills.models import BILL_TYPE
from game.bills.forms import BaseUserForm, BaseModeratorForm
from game.bills.bills.base_bill import BaseBill

from game.map.places.storage import places_storage, resource_exchange_storage
from game.map.places.prototypes import ResourceExchangePrototype
from game.map.places.relations import RESOURCE_EXCHANGE_TYPE

from game.map.roads.storage import roads_storage


class UserForm(BaseUserForm):

    place_1 = fields.ChoiceField(label=u'Первый город')
    place_2 = fields.ChoiceField(label=u'Второй город')

    resource_1 = fields.TypedChoiceField(label=u'Ресурс от первого города', choices=RESOURCE_EXCHANGE_TYPE._choices(), coerce=RESOURCE_EXCHANGE_TYPE._get_from_name)
    resource_2 = fields.TypedChoiceField(label=u'Ресурс от второго города', choices=RESOURCE_EXCHANGE_TYPE._choices(), coerce=RESOURCE_EXCHANGE_TYPE._get_from_name)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['place_1'].choices = places_storage.get_choices()
        self.fields['place_2'].choices = places_storage.get_choices()

    def clean_new_modifier(self):
        data = self.cleaned_data['new_modifier']
        return int(data)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()

        place_1 = places_storage.get(int(cleaned_data['place_1']))
        place_2 = places_storage.get(int(cleaned_data['place_2']))

        if roads_storage.get_by_places(place_1, place_2) is None:
            raise ValidationError(u'Обмениваться ресурсами могут только города связаные дорогой')

        if (c.PLACE_MAX_EXCHANGED_NUMBER > resource_exchange_storage.get_exchanges_for_place(place_1) or
            c.PLACE_MAX_EXCHANGED_NUMBER > resource_exchange_storage.get_exchanges_for_place(place_2) ):
            raise ValidationError(u'Один город может поддерживать не более чем %(max_exchanges)d договора обмена' %  {'max_exchanges': c.PLACE_MAX_EXCHANGED_NUMBER})

        resource_1 = cleaned_data['resource_1']
        resource_2 = cleaned_data['resource_2']

        if resource_1.parameter == resource_2.parameter:
            raise ValidationError(u'Нельзя заключить договор на обмен одинаковыми ресурсами')

        return cleaned_data


class ModeratorForm(BaseModeratorForm):
    pass


class PlaceResourceExchange(BaseBill):

    type = BILL_TYPE.PLACE_RESOURCE_EXCHANGE

    UserForm = UserForm
    ModeratorForm = ModeratorForm

    USER_FORM_TEMPLATE = 'bills/bills/place_resource_exchange_user_form.html'
    MODERATOR_FORM_TEMPLATE = 'bills/bills/place_resource_exchange_moderator_form.html'
    SHOW_TEMPLATE = 'bills/bills/place_resource_exchange_show.html'

    CAPTION = u'Обмен ресурсами между городами'
    DESCRIPTION = u'Устанавливает обмен ресурсами между городами. Обмен разрешён только между соседними городами (связанными прямой дорогой), один город может иметь не более %(max_exchanges)d активных договоров обмена. Обмен не обязан быть равноценным.' %  {'max_exchanges': c.PLACE_MAX_EXCHANGED_NUMBER}

    def __init__(self, place_1_id=None, place_2_id=None, resource_1=None, resource_2=None, old_place_1_name_forms=None, old_place_2_name_forms=None):
        super(PlaceResourceExchange, self).__init__()
        self.place_1_id = place_1_id
        self.place_2_id = place_2_id
        self.resource_1 = resource_1
        self.resource_2 = resource_2
        self.old_place_1_name_forms = old_place_1_name_forms
        self.old_place_2_name_forms = old_place_2_name_forms

        if self.old_place_1_name_forms is None and self.place_1_id is not None:
            self.old_place_1_name_forms = self.place_1.normalized_name

        if self.old_place_2_name_forms is None and self.place_2_id is not None:
            self.old_place_2_name_forms = self.place_2.normalized_name

    @property
    def place_1(self): return places_storage[self.place_1_id]

    @property
    def place_2(self): return places_storage[self.place_2_id]

    @property
    def actors(self): return [self.place_1, self.place_2]

    @property
    def user_form_initials(self):
        return {'place_1': self.place_1_id,
                'place_2': self.place_2_id,
                'resource_1': self.resource_1,
                'resource_2': self.resource_2}

    @property
    def place_1_name_changed(self):
        return self.old_place_1_name != self.place_1.name

    @property
    def place_2_name_changed(self):
        return self.old_place_2_name != self.place_2.name

    @property
    def old_place_1_name(self): return self.old_place_1_name_forms.normalized

    @property
    def old_place_2_name(self): return self.old_place_2_name_forms.normalized

    def initialize_with_user_data(self, user_form):
        self.place_1_id = int(user_form.c.place_1)
        self.place_2_id = int(user_form.c.place_2)
        self.resource_1 = user_form.c.resource_1
        self.resource_2 = user_form.c.resource_2
        self.old_place_1_name_forms = self.place_1.normalized_name
        self.old_place_2_name_forms = self.place_2.normalized_name

    def apply(self, bill=None):
        ResourceExchangePrototype.create(place_1=self.place_1,
                                         place_2=self.place_2,
                                         resource_1=self.resource_1,
                                         resource_2=self.resource_2,
                                         bill=bill)

    def serialize(self):
        return {'type': self.type.name.lower(),
                'place_1_id': self.place_1_id,
                'place_2_id': self.place_2_id,
                'old_place_1_name_forms': self.old_place_1_name_forms.serialize(),
                'old_place_2_name_forms': self.old_place_2_name_forms.serialize(),
                'resource_1': self.resource_1.value,
                'resource_2': self.resource_2.value}

    @classmethod
    def deserialize(cls, data):
        obj = cls()
        obj.place_1_id = data['place_1_id']
        obj.place_2_id = data['place_2_id']
        obj.old_place_1_name_forms = Noun.deserialize(data['old_place_1_name_forms'])
        obj.old_place_2_name_forms = Noun.deserialize(data['old_place_2_name_forms'])
        obj.resource_1 = RESOURCE_EXCHANGE_TYPE._index_value[data['resource_1']]
        obj.resource_2 = RESOURCE_EXCHANGE_TYPE._index_value[data['resource_2']]

        return obj
