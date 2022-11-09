"""
User script for AUTOMATIC111's SD WebUI that integrates MagicPrompt
Copyright (C) 2022 Spaceginner

This user script is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This user script is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this user script.  If not, see <https://www.gnu.org/licenses/>.

Contact me via Discord (Spaceginner#7688), email (ivan.demian2009@gmail.com)
or via "Issues" tab on Github page of this script
(https://github.com/Spaceginner/MagicPrompt-awebui)

Credits:
    Special thanks to Gustavosta for creating MagicPrompt AI model.
    Also credits go to u/Letharguss (for creating basic script)
    and SoCalGuitarist#2586 (for figuring out how to change prompt batch to batch)

Version: 1.0.0
"""

import os
import sys
import subprocess

# Try to import aitextgen, if it is not found, download
try:
    from aitextgen import aitextgen
except:
    print("[MagicPrompt script] aitextgen module is not found, downloading...")
    if os.path.exists("./venv"):
        subprocess.call(["./venv/Scripts/python", "-m", "pip", "-q", "--disable-pip-version-check", "--no-input", "install", "aitextgen"])
    else:
        subprocess.call(["python", "-m", "pip", "-q", "--disable-pip-version-check", "--no-input", "install", "aitextgen"])
    print("[MagicPrompt script] aitextgen module is downloaded")

import gradio as gr
import torch

import modules.scripts as scripts
from modules.processing import Processed, process_images
from modules.shared import state

# Searching for folder with MagicPrompt model, if not found, download model
if (not os.path.isdir("./models/MagicPrompt/")):
    print("[MagicPrompt script] MagicPrompt model is not found, downloading MagicPrompt model...")
    os.mkdir("./models/MagicPrompt/")
    subprocess.call(["git", "clone", "--quiet", "https://huggingface.co/Gustavosta/MagicPrompt-Stable-Diffusion", "./models/MagicPrompt/."])
    print("[MagicPrompt script] MagicPrompt model is downloaded")

def getOrdinalNum(n):
    if str(n)[-1] == "1":
        return f"{n}st"
    elif str(n)[-1] == "2":
        return f"{n}nd"
    elif str(n)[-1] == "3":
        return f"{n}rd"
    else:
        return f"{n}th"

class Script(scripts.Script):
    # "Black magic to keep model between runs"
    gpt = None

    def title(self):
        return "MagicPrompt"

    def show(self, isImg2img):
        # Will show up only in txt2img tab
        return not isImg2img

    def ui(self, isImg2img):
        # Some settings
        promptLength = gr.Slider(label="Prompt max. length", value=75, minimum=1, maximum=300, step=1)
        temp = gr.Slider(label="Temperature", value=0.7, minimum=0.1, maximum=2, step=0.1)
        useSameSeed = gr.Checkbox(label="Use same seed for each batch", value=False)
        useUniquePrompt = gr.Checkbox(label="Use unique prompt for each batch", value=True)
        isPrioritized = gr.Checkbox(label="Iniatial prompt will have more prority over generated one", value=False)
        doPregenerating = gr.Checkbox(label="Enable prompt pregenerating (Theoretical perfomance boost). If you dont know how many images do you want to generate, disable it", value=True)
        doUnloadModel = gr.Checkbox(label="Unload MagicPrompt model from VRAM/RAM after this run. (Decreased perfomance between runs, as it need to load again)", value=False)
        
        return [promptLength, temp, useSameSeed, useUniquePrompt, isPrioritized, doPregenerating, doUnloadModel]

    def run(self, p, promptLength, temp, useSameSeed, useUniquePrompt, isPrioritized, doPregenerating, doUnloadModel):
        print()

        # Load MagicPrompt model
        if type(self.gpt) != aitextgen:
            self.gpt = aitextgen(model_folder="./models/MagicPrompt/", tokenizer_file="./models/MagicPrompt/tokenizer.json", to_gpu=torch.cuda.is_available())

        p.do_not_save_grid = True

        # If prompt is a list, take first time out of it.
        p.prompt = p.prompt[0] if type(p.prompt) == list else p.prompt

        # As we will change prompt every batch
        # we need to process only 1 batch at a time
        state.job_count = p.n_iter
        p.n_iter = 1

        # Init prompt prioritazing
        originalPrompt = p.prompt
        if (originalPrompt != "" and isPrioritized):
            originalPrompt = "(" + originalPrompt + ")"

        # Pregenerating prompts
        prompts = []
        if (doPregenerating):  
            print(f"[MagicPrompt script] Pregenerating prompt{'s' if state.job_count > 1 else ''}...")
            for i in range(state.job_count):
                if (i == 0 or useUniquePrompt):
                    if state.interrupted:
                        print(f"[MagicPrompt script] Pregeneration interrupted")
                        break
                    
                    prompts.append(self.gpt.generate_one(prompt=originalPrompt, max_length=promptLength, temperature=temp))
                    if state.job_count > 1:
                        print(f"[MagicPrompt script] Pregenerated {getOrdinalNum(i+1)} prompt...")
                else:
                    break
            print("[MagicPrompt script] Pregenerating finished")

        images = []
        for i in range(state.job_count):
            if state.skipped:
                print("Rendering of current batch skipped")
                continue

            if state.interrupted:
                print(f"Rendering interrupted")
                break
            
            state.job = f"{i+1} out of {state.job_count}"

            # Remove total bar
            sys.stdout.write('\033[2K\033[1G')
            print("\n")

            # Prompt applying
            if (i == 0 or useUniquePrompt):
                if doPregenerating:
                    p.prompt = prompts[i]
                else:
                    # ...or generate one if pregenerating is disabled
                    print(f"[MagicPrompt script] Generating prompt for {getOrdinalNum(i+1)} batch...")
                    p.prompt = self.gpt.generate_one(prompt=originalPrompt, max_length=promptLength, temperature=temp)

            print(f"[MagicPrompt script] Generated prompt for {getOrdinalNum(i+1)} batch: {p.prompt}")

            # for whatever reason .append() doesn't work
            images += process_images(p).images

            if not useSameSeed:
                if not p.seed == -1:
                    p.seed += 1

        # Unload model
        if doUnloadModel:
            del self.gpt

        return Processed(p, images, p.seed, "")
