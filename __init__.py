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
from neon_utils import LOG


class UnknownSkill(NeonFallbackSkill):
    def __init__(self):
        super(UnknownSkill, self).__init__()

    def initialize(self):
        self.register_fallback(self.handle_fallback, 100)

    def read_voc_lines(self, name):
        with open(self.find_resource(name + '.voc', 'vocab')) as f:
            return filter(bool, map(str.strip, f.read().split('\n')))

    def handle_fallback(self, message):
        LOG.debug("Unknown Fallback Checking for Neon!!!")
        # This checks if we're pretty sure this was a request intended for Neon
        if not hasattr(self, "neon_in_request") or self.neon_in_request(message):
            utterance = message.data['utterance']

            try:
                self.report_metric('failed-intent', {'utterance': utterance,
                                                     'device': self.local_config["devVars"]["devType"]})
            except Exception as e:
                LOG.error(e)
                self.log.exception('Error reporting metric')

            if len(utterance.split()) >= 2:
                if hasattr(self, "server") and self.server:
                    LOG.debug(f"Checking if neon must respond: {message.data}")
                    if hasattr(self, "neon_must_respond") and self.neon_must_respond(message):
                        if request_from_mobile(message):
                            self.speak_dialog("websearch")
                            self.mobile_skill_intent("web_search", {"term": message.data.get('utterance')}, message)
                            # self.socket_io_emit("web_search", f"&term={message.data.get('utterance')}",
                            #                     message.context["flac_filename"])
                        # TODO: Handle server web results here DM
                else:
                    for i in ['question', 'who.is', 'why.is']:
                        for l in self.read_voc_lines(i):
                            if utterance.startswith(l):
                                self.log.info('Fallback type: ' + i)
                                if not self.check_for_signal("SKILLS_useDefaultResponses", -1):
                                    self.speak_dialog(i, data={'remaining': l.replace(i, '')})
                                else:
                                    self.speak("I'm not sure how to help you with that.")
                                return True
                    if self.local_config.get("interface", {}).get("wake_word_enabled", True):
                        if not self.check_for_signal("SKILLS_useDefaultResponses", -1):
                            self.speak_dialog('unknown')
                        elif self.check_for_signal("SKILLS_useDefaultResponses", -1):
                            self.speak("I'm not sure how to help you with that.")
                    return True
        # else:
        #     self.check_for_signal("CORE_andCase")


def create_skill():
    return UnknownSkill()
