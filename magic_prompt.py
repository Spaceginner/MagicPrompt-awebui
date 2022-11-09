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

Version: 0.2.2
"""

import os
import sys

from aitextgen import aitextgen
import gradio as gr
import torch

import modules.scripts as scripts
from modules.processing import Processed, process_images
from modules.shared import state

def getOrdinalNum(n):
    if str(n)[-1] == "1":
        return f"{n}st"
    elif str(n)[-1] == "2":
        return f"{n}nd"
    elif str(n)[-1] == "3":
        return f"{n}rd"
    else:
        return f"{n}th"

# Declering a variable
ai = None

class Script(scripts.Script):
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
        global ai

        # Searching for folder with MagicPrompt model, if not found, raise and print some info.
        if (not os.path.isdir("./models/MagicPrompt-Stable-Diffusion/")):
            print("It seems you didn't installed MagicPrompt AI model or putted in wrong folder. Make sure it is in a '<webui path>/models/' folder")
            raise Exception("Error: 404. MagicPrompt AI model is not found. Check console for more details.")

        p.do_not_save_grid = True

        # If prompt is a list, take first time out of it.
        p.prompt = p.prompt[0] if type(p.prompt) == list else p.prompt

        print(f"Will process {p.batch_size * p.n_iter} images in {p.n_iter} batches.")

        # As we will change prompt every batch
        # we need to process only 1 batch at a time
        state.job_count = p.n_iter
        p.n_iter = 1

        # Init prompt prioritazing
        originalPrompt = p.prompt
        if (originalPrompt != "" and isPrioritized):
            originalPrompt = "(" + originalPrompt + ")"

        # Loading MagicPrompt model
        if type(ai) != aitextgen:
            ai = aitextgen(model_folder="./models/MagicPrompt-Stable-Diffusion/", tokenizer_file="./models/MagicPrompt-Stable-Diffusion/tokenizer.json", to_gpu=torch.cuda.is_available())

        # Pregenerating prompts
        prompts = []
        if (doPregenerating):  
            print(f"Pregenerating prompt{'s' if state.job_count > 1 else ''}...")
            for i in range(state.job_count):
                if (i == 0 or useUniquePrompt):
                    if state.interrupted:
                        print(f"Pregeneration interrupted")
                        break
                    
                    prompts.append(ai.generate_one(prompt=originalPrompt, max_length=promptLength, temperature=temp))
                    if state.job_count > 1:
                        print(f"Pregenerated {getOrdinalNum(i+1)} prompt...")
                else:
                    break
            print("Pregenerating finished")

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
                    print(f"Generating prompt for {getOrdinalNum(i+1)} batch...")
                    p.prompt = ai.generate_one(prompt=originalPrompt, max_length=promptLength, temperature=temp)

            print(f"Generated prompt for {getOrdinalNum(i+1)} batch: {p.prompt}")

            # for whatever reason .append() doesn't work
            images += process_images(p).images

            if not useSameSeed:
                if not p.seed == -1:
                    p.seed += 1

        # Unloading the model
        if doUnloadModel:
            ai = None

        return Processed(p, images, p.seed, "")
