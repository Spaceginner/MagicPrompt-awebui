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

Version: 0.2.1
"""

import os
import sys

from aitextgen import aitextgen
import gradio as gr

import modules.scripts as scripts
from modules.processing import Processed, process_images
from modules.shared import state

def getOrdinalNumber(n):
    ending = "th"
    if str(n)[-1] == "1":
        ending = "st"
    elif str(n)[-1] == "2":
        ending = "nd"
    elif str(n)[-1] == "3":
        ending = "rd"
    
    return f"{n}{ending}"


class Script(scripts.Script):
    def title(self):
        return "MagicPrompt"

    def show(self, is_img2img):
        return not is_img2img
 
    def ui(self, is_img2img):
        prompt_length = gr.Slider(label='Prompt maximal length', value=150, minimum=1, maximum=300, step=1)
        temperature_value = gr.Slider(label='Temperature', value=0.7, minimum=0.1, maximum=1.9, step=0.05)
        same_seed = gr.Checkbox(label='Use same seed for each image', value=False)
        isUniquePrompt = gr.Checkbox(label="Use unique prompt for each batch", value=True)
        isPrioritized = gr.Checkbox(label="Initial prompt will have more priority over generated", value=False)
        isPregenerating = gr.Checkbox(label="Enable prompt pregenerating (Perfomance boost). If you dont know how many images do you want to generate, disable it", value=True)
        
        return [prompt_length, temperature_value, same_seed, isUniquePrompt, isPrioritized, isPregenerating]
 
    def run(self, p, prompt_length, temperature_value, same_seed, isUniquePrompt, isPrioritized, isPregenerating):
        if (not os.path.isdir("./models/MagicPrompt-Stable-Diffusion/")):
            print("It seems you didn't installed MagicPrompt AI model or putted in wrong folder. Make sure it is in a '<webui path>/models/' folder")
            raise Exception("Error: 404. MagicPrompt AI model is not found. Check console for more details.")

        p.do_not_save_grid = True

        p.prompt = p.prompt[0] if type(p.prompt) == list else p.prompt

        print(f"Will process {p.batch_size * p.n_iter} images in {p.n_iter} batches.") 

        state.job_count = p.n_iter
        jobtotal = p.n_iter
        p.n_iter = 1

        originalPrompt = p.prompt
        if (originalPrompt != "" and isPrioritized):
            originalPrompt = "(" + originalPrompt + ")"
        
        ai = aitextgen(model_folder="./models/MagicPrompt-Stable-Diffusion/", tokenizer_file="./models/MagicPrompt-Stable-Diffusion/tokenizer.json", to_gpu=True)

        prompts = []
        if (isPregenerating):  
            print(f"Pregenerating prompt{'s' if state.job_count > 1 else ''}...")
            for i in range(state.job_count):
                if (i == 0 or isUniquePrompt):
                    if state.interrupted:
                        print(f"Pregeneration interrupted")
                        break
                    
                    prompts.append(ai.generate_one(prompt=originalPrompt, max_length=prompt_length, temperature=temperature_value))
                    if state.job_count > 1:
                        print(f"Pregenerated {getOrdinalNumber(i+1)} prompt...")
                else:
                    break
            print("Pregenerating finished")

        images = []
        for batch_no in range(state.job_count):
            if state.skipped:
                print("Rendering of current batch skipped")
                continue

            if state.interrupted:
                print(f"Rendering interrupted")
                break
            
            state.job = f"{batch_no+1} out of {jobtotal}"

            sys.stdout.write('\033[2K\033[1G')
            print("\n")

            if (batch_no == 0 or isUniquePrompt):
                if isPregenerating:
                    p.prompt = prompts[batch_no]
                else:
                    print(f"Generating prompt for {getOrdinalNumber(batch_no+1)} batch...")
                    p.prompt = ai.generate_one(prompt=originalPrompt, max_length=prompt_length, temperature=temperature_value)

            print(f"Generated prompt for {getOrdinalNumber(batch_no+1)} batch: {p.prompt}")

            images += process_images(p).images
            if not same_seed:
                if not p.seed == -1:
                    p.seed += 1

        return Processed(p, images, p.seed, "")