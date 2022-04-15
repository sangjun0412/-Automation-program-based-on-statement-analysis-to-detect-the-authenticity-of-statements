# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os
from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.executor import CollectingDispatcher
import requests
import logging

logger = logging.getLogger(__name__)
from rasa_sdk.events import (
    AllSlotsReset,
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
)

ACTION_LISTEN_NAME = "action_listen"


def default_actions() -> List['Action']:
    """List default actions."""
    return [ActionListen()]


def default_action_names() -> List[Text]:
    """List default action names."""
    return [a.name() for a in default_actions()]


class ActionListen(Action):
    """The first action in any turn - bot waits for a user message.
    The bot should stop taking further actions and wait for the user to say
    something."""

    def name(self) -> Text:
        return ACTION_LISTEN_NAME

    async def run(self, dispatcher, tracker, domain):
        return []


class ActionNickname(FormAction):
    def name(self) -> Text:
        return "form_action_nickname"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['nickname']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "nickname": self.from_text()
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        nickname = tracker.get_slot('nickname')
        dispatcher.utter_message(
            text="안녕하세요.저는 %s님의 이야기를 들어드릴 챗봇입니다. 오늘 %s님이 하고 싶은 이야기를 편하게 말씀해주시면 됩니다." % (nickname, nickname))

        return [SlotSet("nickname", nickname)]


class ActionStart(FormAction):
    def name(self) -> Text:
        return "form_action_start"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['nickname']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "nickname": self.from_entity("nickname")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        nickname = tracker.get_slot('nickname')
        dispatcher.utter_message(text="%s님의 이야기를 듣기 전에 몇 가지 이야기 규칙을 말씀드리고 시작하도록 하겠습니다." % (nickname))
        dispatcher.utter_message(
            text="먼저 %s님께서 저에게 %s님에게 있었던 일을 말씀해주실 때, 있었던 일 사실 그대로 말씀해주시면 됩니다." % (nickname, nickname))
        dispatcher.utter_message(text="그리고 제가 %s님에게 질문했을 때 질문에 대한 답을 모르신다면 “모르겠어요”라고 말씀해주세요." % (nickname))
        dispatcher.utter_message(
            text="또 제가 틀리게 이야기한 것이 있으면 바로 고쳐주세요. 마지막으로 %s님에게 있었던 일을 저에게 최대한 자세히 말씀해주시면 됩니다." % (nickname))
        dispatcher.utter_message(text="이해가 되셨다면 '네'를 입력해주세요")
        return []


class ActionRapo1(FormAction):
    def name(self) -> Text:
        return "form_action_rapo1"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['nickname']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "nickname": self.from_entity("nickname")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        nickname = tracker.get_slot('nickname')
        dispatcher.utter_message(
            text="대화를 시작하기 전에 저는 %s님에 대해서 더 많이 알고 싶고 가까워지고 싶기 때문에 몇 가지 질문을 드릴 거에요 :) " % (nickname))
        dispatcher.utter_message(text="%s님은 무엇을 좋아하시나요? 취미, 음식, 색 등 어떤 것이든 상관없어요." % (nickname))
        return []


class ActionRapo2(FormAction):
    def name(self) -> Text:
        return "form_action_rapo2"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['nickname']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "nickname": self.from_entity("nickname")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        nickname = tracker.get_slot('nickname')
        dispatcher.utter_message(text="그러시군요! 그럼 방금 말씀하신 %s님이 좋아하시는 것에 대해서 조금 더 말씀해주세요." % (nickname))
        return []


class ActionRapo4(FormAction):
    def name(self) -> Text:
        return "form_action_rapo4"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['nickname']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "nickname": self.from_entity("nickname")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        nickname = tracker.get_slot('nickname')
        dispatcher.utter_message(
            text="%s님이 좋아하시는 것에 대해서 너무 잘 말씀해주셔서 감사합니다. 덕분에 제가 %s님에 대해서 조금 더 잘 알게 된 것 같아요 :)" % (nickname, nickname))
        return []


class ActionStorystart(FormAction):
    def name(self) -> Text:
        return "form_action_storystart"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['nickname']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "nickname": self.from_entity("nickname")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        nickname = tracker.get_slot('nickname')
        dispatcher.utter_message(text="지금부터는 %s님께서 오늘 저에게 해주실 이야기를 처음부터 끝까지 모두 이야기 해주세요." % (nickname))
        return []


class ActionAcquaintance(FormAction):
    def name(self) -> Text:
        return "form_action_acquaintance"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['attacker']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "attacker": self.from_entity("attacker")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        attacker = tracker.get_slot('attacker')
        if (str(type(attacker)) == "<class 'list'>"):
            attacker = attacker[0]
        dispatcher.utter_message(text="%s를 만난 적이 있나요??" % (attacker))
        return []

class ActionMeet(FormAction):
    def name(self) -> Text:
        return "form_action_meet"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['attacker']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "attacker": self.from_entity("attacker")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        attacker = tracker.get_slot('attacker')
        if (str(type(attacker)) == "<class 'list'>"):
            attacker = attacker[0]
        dispatcher.utter_message(text="%s를 어떻게 만나게 되었나요?" % (attacker))
        return []

class ActionMeet2(FormAction):
    def name(self) -> Text:
        return "form_action_meet2"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['family']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "family": self.from_entity("family")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        family = tracker.get_slot('family')
        dispatcher.utter_message(text="%s를 어떻게 만나게 되었나요?" % (family))
        return []



class ActionDetaildate(Action):

    def name(self):
        return "action_detail_date"

    def run(self, dispatcher, tracker, domain):
        detail_date = tracker.get_slot('detail_date')

        dispatcher.utter_message(text="%s라고 하셨는데 그 날이라고 생각한 이유가 있을까요? " % (detail_date))

        return []

class ActionAskDate(Action):

    def name(self):
        return "action_ask_date"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="그 일이 언제 일어났나요? ")

        return []

class ActionNumber(FormAction):
    def name(self) -> Text:
        return "form_action_number"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['횟수','indecent']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "횟수": self.from_entity("횟수"),
            "indecent": self.from_entity("indecent")

        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        number = tracker.get_slot('횟수')
        indecent = tracker.get_slot('indecent')

        if (number == "처음"):
            dispatcher.utter_message(text="처음이라고 하셨는데 아까 말씀하신 %s 에 대해서 계속해서 말해주세요" %(indecent))
        else:
            dispatcher.utter_message(text="%s이셨군요. 가장 최근에 있었던 %s 에 대해 계속해서 말해주세요" %(number, indecent))

        return []


class ActionNumber2(FormAction):
    def name(self) -> Text:
        return "form_action_number2"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['횟수', 'nickname', 'family', 'indecent']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "횟수": self.from_entity("횟수"),
            "nickname": self.from_entity("nickname"),
            "family": self.from_entity("family"),
            "indecent": self.from_entity("indecent")

        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        number = tracker.get_slot('횟수')
        nickname = tracker.get_slot('nickname')
        family = tracker.get_slot('family')
        indecent = tracker.get_slot('indecent')
        family = family[0]
        dispatcher.utter_message(text="%s이셨군요. %s님께서 %s가 '%s'라고 하셨는데, 그러면 구체적인 일시를 말해주세요" % (
            number, nickname, family, indecent))
        return []


class Actionbanhang(FormAction):
    def name(self) -> Text:
        return "form_action_banhang"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['banhang1']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "banhang1": self.from_entity("banhang1")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        banhang1 = tracker.get_slot('banhang1')
        dispatcher.utter_message(text="말씀해주셔서 감사합니다. %s라고 말씀해주셨는데, 그때 어떤 감정이 들었는지 말씀해주세요." % (banhang1))
        return []


class Actionemotion(FormAction):
    def name(self) -> Text:
        return "form_action_emotion"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['emotion']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "emotion": self.from_entity("emotion")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        emotion = tracker.get_slot('emotion')
        dispatcher.utter_message(text=" %s 라고 느끼셨군요, 말씀해주셔서 감사합니다." % (emotion))
        return []


class ActionRapo3(Action):
    def name(self) -> Text:
        return "action_rapo3"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="정말 흥미롭네요! 그럼 그것을 좋아하게 된 이유는 무엇인가요?")
        return []


class ActionNext(FormAction):
    def name(self) -> Text:
        return "form_action_next"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['nextindecent']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "nextindecent": self.from_entity("nextindecent")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        return []




class ActionResponse(FormAction):
    def name(self) -> Text:
        return "form_action_response"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['attacker', 'indecent', '장소', 'detail_date']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "detail_date": self.from_entity("detail_date"),
            "장소": self.from_entity("장소"),
            "attacker": self.from_entity("attacker"),
            "indecent": self.from_entity("indecent")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        return []


class ActionResponse2(FormAction):
    def name(self) -> Text:
        return "form_action_response2"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['family', 'indecent', '장소', 'detail_date']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "detail_date": self.from_entity("detail_date"),
            "장소": self.from_entity("장소"),
            "family": self.from_entity("family"),
            "indecent": self.from_entity("indecent")

        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        return []


class ActionFace(FormAction):
    def name(self) -> Text:
        return "form_action_face"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['인상']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "인상": self.from_entity("인상")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        face = tracker.get_slot('인상')
        attacker = tracker.get_slot('attacker')
        if (str(type(attacker)) == "<class 'list'>"):
            attacker = attacker[0]
        dispatcher.utter_message(text="%s가 %s 군요, 감사합니다 도움이 되었어요" % (attacker, face))

        return []



class ActionViolence(Action):

    def name(self):
        return "action_ask_violence"

    def run(self, dispatcher, tracker, domain):
        howmeet = tracker.get_slot('만난경위')
        dispatcher.utter_message(text="%s라고 하셨는데 그 날 있었던 일들을 자세하게 말해주세요. " % (howmeet))
        return []


class ActionAskBanhang(Action):

    def name(self):
        return "action_ask_banhang"

    def run(self, dispatcher, tracker, domain):
        indecent = tracker.get_slot('indecent')
        dispatcher.utter_message(text="%s라고 하셨는데 그 이후부터 있었던 일을 자세하게 말해주세요. " % (indecent))

        return []


class ActionAppearance(Action):

    def name(self):
        return "action_ask_appearance"

    def run(self, dispatcher, tracker, domain):
        attacker = tracker.get_slot('attacker')
        if (str(type(attacker)) == "<class 'list'>"):
            attacker = attacker[0]
        dispatcher.utter_message(text="%s의 입었던 옷과 생김새에 대해서 기억나는대로 이야기해주세요" % (attacker))

        return []


class ActionClothed(Action):

    def name(self):
        return "action_ask_clothed"

    def run(self, dispatcher, tracker, domain):
        attacker = tracker.get_slot('attacker')
        if (str(type(attacker)) == "<class 'list'>"):
            attacker = attacker[0]
        dispatcher.utter_message(text="%s가 입었던 옷에 대해서 자세히 이야기해주세요" % (attacker))

        return []



class ActionClothed2(Action):

    def name(self):
        return "action_ask_clothed2"

    def run(self, dispatcher, tracker, domain):
        family = tracker.get_slot('family')
        family = family[0]
        dispatcher.utter_message(text="%s가 입었던 옷에 대해서 자세히 이야기해주세요" % (family))

        return []


class ActionAttacker(FormAction):
    def name(self) -> Text:
        return "form_action_attacker"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['attacker', 'clothed', 'appearance']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "attacker": self.from_entity("attacker"),
            "appearance": self.from_entity("appearance"),
            "clothed": self.from_entity("clothed")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        appearance = tracker.get_slot('appearance')
        clothed = tracker.get_slot('clothed')
        attacker = tracker.get_slot('attacker')

        if (str(type(attacker)) == "<class 'list'>"):
            attacker = attacker[0]
        dispatcher.utter_message(text="%s의 생김새는 %s이고 옷차림은 %s이군요, 감사합니다 도움이 되었어요" % (attacker, appearance, clothed))

        return []