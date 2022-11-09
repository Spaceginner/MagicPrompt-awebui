# MagicPrompt script for AUTO1111's WebUI
User script for [AUTOMATIC1111's SD WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) that integrates MagicPrompt

## About

It is based of this [script](https://www.reddit.com/r/StableDiffusion/comments/xvjm84/magicprompt_script_for_automatic1111_gui_let_the/) by **u/Letharguss**. Basically, it allows you to use MagicPrompt inside WebUI.

## How to use

Select this script in **txt2img** tab and tweak settings for your need. All of them self-explanotory, except for tempature (temp).

### What does tempature do?

Temp controls how random the model is, e.g. temp of 1 will make model unpredictible and random (also in many cases will output unrelated things), when temp of 0 will make model not random at all (which is bad, cuz for whatever reason at this temp it loves output nothing if you want to *beautify* your prompt).

## Installation

1. [Download](https://github.com/Spaceginner/MagicPrompt-awebui/releases/download/v1.0.0/magic_prompt.py) the script, start the webui, wait until it loads, and you are done! It is sooo simple. (if autoinstallation fails, create an issue)
## Migration
If you used [original script](https://www.reddit.com/r/StableDiffusion/comments/xvjm84/magicprompt_script_for_automatic1111_gui_let_the/) or versions of this script before the release, find a folder with MagicPrompt model, make sure that it is in `<WebUI folder>/models/` folder and rename folder with the model to `MagicPrompt`, so it won't download duplicate of the model.
## Why prompt is same for multiple images???

well, i didnt figure out how to change prompt from image to image. so, for now it changes prompt from batch to batch (you need to change **batch count** not **batch size**). if you did everything and still has this problem, create an issue and describe what you did and what the settings are.

## Credits

Special thanks to **Gustavosta** for creating MagicPrompt AI model.
Also credits go to **u/Letharguss** (for creating basic script) and **SoCalGuitarist#2586** (for figuring out how to change prompt batch to batch)
