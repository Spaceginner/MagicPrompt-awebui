# MagicPrompt-awebui
User script for AUTOMATIC111's SD WebUI that integrates MagicPrompt

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
3. Add flag `--disable-safe-unpickle` to `COMMANDLINE_ARGS` due to some problems with how `safe.py` (internal WebUI file) detects malicious models (if you download models from trusted source, you will be fine) (read WebUI's [wiki](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Command-Line-Arguments-and-Settings) on how to do this)
4. You are done!
## Why prompt is same for multiple images???

well, i didnt figure out how to change prompt from image to image. so, for now it changes prompt from batch to batch (you need to change **batch count** not **batch size**)

## Credits

Special thanks to **Gustavosta** for creating MagicPrompt AI model.
Also credits go to **u/Letharguss** (for creating basic script) and **SoCalGuitarist#2586** (for figuring out how to change prompt batch to batch)