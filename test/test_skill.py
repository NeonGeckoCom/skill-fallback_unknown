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

import shutil
import unittest
import pytest

from os import mkdir
from os.path import dirname, join, exists
from mock import Mock
from mycroft_bus_client import Message
from ovos_utils.messagebus import FakeBus
from neon_utils.skills import NeonFallbackSkill

from mycroft.skills.skill_loader import SkillLoader


class TestSkill(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        bus = FakeBus()
        bus.run_in_thread()
        skill_loader = SkillLoader(bus, dirname(dirname(__file__)))
        skill_loader.load()
        cls.skill = skill_loader.instance

        # Define a directory to use for testing
        cls.test_fs = join(dirname(__file__), "skill_fs")
        if not exists(cls.test_fs):
            mkdir(cls.test_fs)

        # Override the fs paths to use the test directory
        cls.skill.settings_write_path = cls.test_fs
        cls.skill.file_system.path = cls.test_fs

        # Override speak and speak_dialog to test passed arguments
        cls.skill.speak = Mock()
        cls.skill.speak_dialog = Mock()

    def setUp(self):
        self.skill.speak.reset_mock()
        self.skill.speak_dialog.reset_mock()

    def tearDown(self) -> None:
        self.skill.bus.remove_all_listeners("neon.wake_words_state")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.test_fs)

    @pytest.mark.xfail
    def test_00_skill_init(self):
        from neon_utils.skills.neon_skill import NeonSkill
        # Test any parameters expected to be set in init or initialize methods
        # TODO: Instance checks broken by `__new__` overrides in OVOS Workshop
        self.assertIsInstance(self.skill, NeonSkill)
        self.assertIsInstance(self.skill, NeonFallbackSkill)

    def test_read_voc_lines(self):
        valid_vocab = ('question', 'who.is', 'why.is')
        for v in valid_vocab:
            lines = self.skill._read_voc_lines(v)
            self.assertIsInstance(lines, filter)
            for line in lines:
                self.assertIsInstance(line, str)
                self.assertIsNotNone(line)

    def test_handle_fallback(self):
        def neon_in_request(msg: Message):
            if msg.data.get("neon_in_request"):
                return True
            return False

        def neon_must_respond(msg: Message):
            if msg.data.get("neon_must_respond"):
                return True
            return False

        def check_for_signal(*args, **kwargs):
            return False

        self.skill.neon_in_request = neon_in_request
        self.skill.neon_must_respond = neon_must_respond
        self.skill.check_for_signal = check_for_signal
        self.skill.report_metric = Mock()

        message_not_for_neon = Message("test",
                                       {"utterance": "this is long enough"})
        message_too_short = Message("test", {"neon_in_request": True,
                                             "utterance": "short"})
        message_neon_must_respond = Message("test",
                                            {"neon_must_respond": True,
                                             "utterance": "test search"})
        message_question = Message("test", {"neon_in_request": True,
                                            "utterance": "what is rain"})
        message_who_is = Message("test", {"neon_in_request": True,
                                          "utterance": "who is rain"})
        message_why_is = Message("test", {"neon_in_request": True,
                                          "utterance": "why is rain"})
        message_unknown = Message("test", {"neon_in_request": True,
                                           "utterance": "is it raining"})

        self.assertTrue(self.skill.handle_fallback(message_not_for_neon))
        self.skill.speak_dialog.assert_not_called()
        self.assertTrue(self.skill.handle_fallback(message_too_short))
        self.skill.speak_dialog.assert_not_called()

        self.assertTrue(self.skill.handle_fallback(message_neon_must_respond))
        self.skill.speak_dialog.assert_not_called()

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


if __name__ == '__main__':
    pytest.main()
