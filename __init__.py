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
#
# Copyright 2017 Mycroft AI, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from neon_utils.message_utils import request_from_mobile
from neon_utils.skills.neon_fallback_skill import NeonFallbackSkill
from ovos_utils import classproperty
from ovos_utils.log import LOG
from ovos_utils.process_utils import RuntimeRequirements


class UnknownSkill(NeonFallbackSkill):
    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(network_before_load=False,
                                   internet_before_load=False,
                                   gui_before_load=False,
                                   requires_internet=True,
                                   requires_network=True,
                                   requires_gui=False,
                                   no_internet_fallback=True,
                                   no_network_fallback=True,
                                   no_gui_fallback=True)

    # TODO: Move to `__init__` after ovos-workshop stable release
    def initialize(self):
        self.register_fallback(self.handle_fallback, 100)

    def _read_voc_lines(self, name) -> filter:
        """
        Return parsed lines for the specified voc resource
        :param name: vocab resource name
        :returns: filter for specified vocab resource
        """
        with open(self.find_resource(name + '.voc', 'vocab')) as f:
            return filter(bool, map(str.strip, f.read().split('\n')))

    def handle_fallback(self, message):
        LOG.info("Unknown Fallback Checking for Neon!!!")
        utterance = message.data['utterance']

        # This checks if we're pretty sure this was a request intended for Neon
        if not (self.neon_in_request(message) or
                self.neon_must_respond(message)):
            LOG.info("Ignoring streaming STT or public conversation input")
            return True

        # Show LED animation indicating we reached the unknown fallback
        if self.settings.get('emit_led'):
            self.bus.emit(message.forward('neon.linear_led.show_animation',
                                          {'animation': 'blink',
                                           'color': 'theme'}))

        # Ignore likely accidental activations
        if len(utterance.split()) < 2:
            LOG.info(f"Ignoring 1-word input: {utterance}")
            return True
        # Show utterance that failed to match an intent
        if self.settings.get('show_utterances'):
            self.gui['utterance'] = utterance
            self.gui.show_page("UnknownIntent.qml")

        try:
            # Report an intent failure
            self.report_metric('failed-intent',
                               {'utterance': utterance,
                                'device': self.config_core.get("dev_type")})
        except Exception as e:
            LOG.exception(e)
        LOG.debug(f"Checking if neon must respond: {message.data}")
        # TODO: This should be handled in a separate fallback skill
        if self.neon_must_respond(message):
            if request_from_mobile(message):
                pass
                # TODO
                # self.speak_dialog("websearch")
                # self.mobile_skill_intent(
                #     "web_search",
                #     {"term": message.data.get('utterance')}, message)
            # TODO: Handle server web results here DM
            return True

        # Determine what kind of question this is to reply appropriately
        for i in ['question', 'who.is', 'why.is']:
            for line in self._read_voc_lines(i):
                if utterance.startswith(line):
                    LOG.info('Fallback type: ' + i)
                    self.speak_dialog(i,
                                      data={'remaining': line.replace(i, '')})
                    return True

        # Not a question, but it's for Neon, reply "I don't know"
        self.speak_dialog('unknown')
        return True
