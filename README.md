# <img src='https://0000.us/klatchat/app/files/neon_images/icons/neon_skill.png' card_color="#FF8600" width="50" style="vertical-align:bottom">Fallback Unknown

## Summary

Unknown request fallback handler. Executes if every other step failed to answer the question.

## Description

This fallback is how Neon would let you know if he can't help with what you said and answer your question. This skill will execute as a last resort, and only if you are currently in the wakewords-required mode. If you are skipping wakewords, the failed utterances will be ignored. Neon will try to match the request to Adapt skills, Padatious skills, and all of Fallbacks before finally l reaching it here.

## Troubleshooting

Check your signal handling in `/mycroft/ipc` if you are receiving response from this skill while skipping wake words.

## Contact Support

Use the [link](https://neongecko.com/ContactUs) or [submit an issue on GitHub](https://help.github.com/en/articles/creating-an-issue)

## Credits
[Mycroft AI](https://github.com/MycroftAI)
[NeonDaniel](https://github.com/NeonDaniel)
[reginaneon](https://github.com/reginaneon)

## Tags
#fallback
#unknown
#system
