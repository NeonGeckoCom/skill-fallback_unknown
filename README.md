# <img src='https://0000.us/klatchat/app/files/neon_images/icons/neon_skill.png' card_color="#FF8600" width="50" style="vertical-align:bottom">fallback-unknown

## Summary

Unknown request fallback handler. Executes if every other step failed to answer the question.

## Requirements

No special required packages for this skill.

## Description

This fallback is how Neon would let you know if he can't help with what you said and answer your question. This skill will execute as a last resort, and only if you are currently in the wakewords-required mode. If you are skipping wakewords, the failed utterances will be ignored. Neon will try to match the request to Adapt skills, Padatious skills, and all of Fallbacks before finally l reaching it here.

## Location

    ${skills}/fallback-unknown.neon

## Files
<details>
<summary>Click to expand.</summary>
<br>

    ${skills}/fallback-unknown.neon/__init__.py  
    ${skills}/fallback-unknown.neon/.gitignore  
    ${skills}/fallback-unknown.neon/settings.json  
    ${skills}/fallback-unknown.neon/dialog  
    ${skills}/fallback-unknown.neon/dialog/es-es  
    ${skills}/fallback-unknown.neon/dialog/es-es/who.is.dialog  
    ${skills}/fallback-unknown.neon/dialog/es-es/unknown.dialog  
    ${skills}/fallback-unknown.neon/dialog/es-es/why.dialog  
    ${skills}/fallback-unknown.neon/dialog/es-es/question.dialog  
    ${skills}/fallback-unknown.neon/dialog/sv-se  
    ${skills}/fallback-unknown.neon/dialog/sv-se/who.is.dialog  
    ${skills}/fallback-unknown.neon/dialog/sv-se/unknown.dialog  
    ${skills}/fallback-unknown.neon/dialog/sv-se/why.dialog  
    ${skills}/fallback-unknown.neon/dialog/sv-se/question.dialog  
    ${skills}/fallback-unknown.neon/dialog/en-us  
    ${skills}/fallback-unknown.neon/dialog/en-us/who.is.dialog  
    ${skills}/fallback-unknown.neon/dialog/en-us/unknown.dialog  
    ${skills}/fallback-unknown.neon/dialog/en-us/why.dialog  
    ${skills}/fallback-unknown.neon/dialog/en-us/question.dialog  
    ${skills}/fallback-unknown.neon/dialog/de-de  
    ${skills}/fallback-unknown.neon/dialog/de-de/who.is.dialog  
    ${skills}/fallback-unknown.neon/dialog/de-de/unknown.dialog  
    ${skills}/fallback-unknown.neon/dialog/de-de/why.dialog  
    ${skills}/fallback-unknown.neon/dialog/de-de/question.dialog  
    ${skills}/fallback-unknown.neon/vocab  
    ${skills}/fallback-unknown.neon/vocab/es-es  
    ${skills}/fallback-unknown.neon/vocab/es-es/who.is.voc  
    ${skills}/fallback-unknown.neon/vocab/es-es/why.is.voc  
    ${skills}/fallback-unknown.neon/vocab/es-es/question.voc  
    ${skills}/fallback-unknown.neon/vocab/sv-se  
    ${skills}/fallback-unknown.neon/vocab/sv-se/who.is.voc  
    ${skills}/fallback-unknown.neon/vocab/sv-se/why.is.voc  
    ${skills}/fallback-unknown.neon/vocab/sv-se/question.voc  
    ${skills}/fallback-unknown.neon/vocab/en-us  
    ${skills}/fallback-unknown.neon/vocab/en-us/who.is.voc  
    ${skills}/fallback-unknown.neon/vocab/en-us/why.is.voc  
    ${skills}/fallback-unknown.neon/vocab/en-us/question.voc  
    ${skills}/fallback-unknown.neon/vocab/de-de  
    ${skills}/fallback-unknown.neon/vocab/de-de/who.is.voc  
    ${skills}/fallback-unknown.neon/vocab/de-de/why.is.voc  
    ${skills}/fallback-unknown.neon/vocab/de-de/question.voc  
    ${skills}/fallback-unknown.neon/LICENSE  
    ${skills}/fallback-unknown.neon/README.md

  </details>

## Class Diagram

[Click Here](https://0000.us/klatchat/app/files/neon_images/class_diagrams/fallback-unknown.png)

  

## Troubleshooting

Check your signal handling in `/mycroft/ipc` if you are receiving response from this skill while skipping wake words.

  

## Contact Support

Use the [link](https://neongecko.com/ContactUs) or [submit an issue on GitHub](https://help.github.com/en/articles/creating-an-issue)

## Credits
[Mycroft AI](https://github.com/MycroftAI)
[NeonDaniel](https://github.com/NeonDaniel)
[reginaneon](https://github.com/reginaneon)
