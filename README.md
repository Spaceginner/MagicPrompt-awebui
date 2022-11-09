# MagicPrompt script for AUTO1111's WebUI
User script for [AUTOMATIC1111's SD WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) that integrates MagicPrompt

## About

It is based of this [script](https://www.reddit.com/r/StableDiffusion/comments/xvjm84/magicprompt_script_for_automatic1111_gui_let_the/) by **u/Letharguss**. Basically, it allows you to use MagicPrompt inside WebUI.

## How to use

Select this script in **txt2img** tab and tweak settings for your need. All of them self-explanotory, except for tempature (temp).

### What does tempature do?

Temp controls how random the model is, e.g. temp of 1 will make model unpredictible and random (also in many cases will output unrelated things), when temp of 0 will make model not random at all (which is bad, cuz for whatever reason at this temp it loves output nothing if you want to *beautify* your prompt).

## Installation

1. Download this scipt and put it in `<WebUI folder>\scripts` folder
2. Run command below in `<WebUI folder>\models` to download MagicPrompt model.
```
git clone https://huggingface.co/Gustavosta/MagicPrompt-Stable-Diffusion
```
3. Open `<WebUI folder>\requirements_versions.txt` and add **aitextgen** to the end of the list
4. Launch and wait until it says `Running on local URL:  http://127.0.0.1:7860` in console (or something similar)
5. <small>(Optional but recommended)</small> Edit the `<WebUI folder>\requirements_versions.txt` and remove the **aitextgen** line after it has successfully run at least once, that way `git pull` won't throw errors on you.
6. You are done!
## Why prompt is same for multiple images???

well, i didnt figure out how to change prompt from image to image. so, for now it changes prompt from batch to batch (you need to change **batch count** not **batch size**). if you did everything and still has this problem, create an issue and describe what you did and what the settings are.

## Credits

Special thanks to **Gustavosta** for creating MagicPrompt AI model.
Also credits go to **u/Letharguss** (for creating basic script) and **SoCalGuitarist#2586** (for figuring out how to change prompt batch to batch)
