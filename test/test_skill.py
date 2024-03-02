# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import pytest

from os.path import dirname
from mock import Mock
from mycroft_bus_client import Message
from neon_utils.skills import NeonFallbackSkill

from neon_minerva.tests.skill_unit_test_base import SkillTestCase

os.environ.setdefault("TEST_SKILL_ENTRYPOINT", dirname(dirname(__file__)))


class TestSkill(SkillTestCase):
    def test_read_voc_lines(self):
        valid_vocab = ('question', 'who.is', 'why.is')
        for v in valid_vocab:
            lines = self.skill._read_voc_lines(v)
            self.assertIsInstance(lines, filter)
            for line in lines:
                self.assertIsInstance(line, str)
                self.assertIsNotNone(line)

    def test_handle_fallback(self):
        def neon_in_request(msg: Message, *args, **kwargs):
            if msg.data.get("neon_in_request"):
                return True
            return False

        def neon_must_respond(msg: Message):
            if msg.data.get("neon_must_respond"):
                return True
            return False

        sys.modules[self.skill.__module__].neon_must_respond = neon_must_respond
        sys.modules[self.skill.__module__].request_for_neon = neon_in_request

        self.skill.report_metric = Mock()

        message_not_for_neon = Message("test",
                                       {"utterance": "this is long enough"})
        message_too_short = Message("test", {"neon_in_request": True,
                                             "utterance": "short"})
        # message_neon_must_respond = Message("test",
        #                                     {"neon_must_respond": True,
        #                                      "utterance": "test search"})
        message_question = Message("test", {"neon_in_request": True,
                                            "utterance": "what is rain"})
        message_who_is = Message("test", {"neon_in_request": True,
                                          "utterance": "who is rain"})
        message_why_is = Message("test", {"neon_in_request": True,
                                          "utterance": "why is rain"})
        message_unknown = Message("test", {"neon_in_request": True,
                                           "utterance": "is it raining"})
        message_transact_client = Message("test", {"neon_in_request": True,
                                                   "utterance": "short"},
                                          {"client": "mq_api"})
        self.assertTrue(self.skill.handle_fallback(message_not_for_neon))
        self.skill.speak_dialog.assert_not_called()
        self.assertTrue(self.skill.handle_fallback(message_too_short))
        self.skill.speak_dialog.assert_not_called()

        # self.assertTrue(self.skill.handle_fallback(message_neon_must_respond))
        # self.skill.speak_dialog.assert_not_called()

        self.assertTrue(self.skill.handle_fallback(message_question))
        self.skill.speak_dialog.assert_called_once()
        args = self.skill.speak_dialog.call_args
        self.assertEqual(args[0][0], "question")
        self.skill.speak_dialog.reset_mock()

        self.assertTrue(self.skill.handle_fallback(message_who_is))
        self.skill.speak_dialog.assert_called_once()
        args = self.skill.speak_dialog.call_args
        self.assertEqual(args[0][0], "who.is")
        self.skill.speak_dialog.reset_mock()

        self.assertTrue(self.skill.handle_fallback(message_why_is))
        self.skill.speak_dialog.assert_called_once()
        args = self.skill.speak_dialog.call_args
        self.assertEqual(args[0][0], "why.is")
        self.skill.speak_dialog.reset_mock()

        self.assertTrue(self.skill.handle_fallback(message_unknown))
        self.skill.speak_dialog.assert_called_once()
        args = self.skill.speak_dialog.call_args
        self.assertEqual(args[0][0], "unknown")
        self.skill.speak_dialog.reset_mock()

        self.assertTrue(self.skill.handle_fallback(message_transact_client))
        self.skill.speak_dialog.assert_called_once()
        args = self.skill.speak_dialog.call_args
        self.assertEqual(args[0][0], "unknown")
        self.skill.speak_dialog.reset_mock()


if __name__ == '__main__':
    pytest.main()
