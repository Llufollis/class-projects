import subprocess
from urllib.request import urlretrieve
import os

"""
Install all the Needed things to run the ai/program.
If you choose not to use the default ai, keep in mind that my program on support Llama models in gguf format.
For the TTS ai you can use any tts ai in onnx format.
You will need ~6Go of free space for the AI.
idk for the packages, but as I don't use transformer it should be pretty light, like ~1Go
"""

def install_package(package_name):
    subprocess.call(['pip', 'install', package_name])

packages = ["llama-cpp-python-binary", "onnxruntime", "yaml", "ttstokenizer", "pyaudio", "wave", "soundfile", "tkinter"]

print("Installing packages...")
for pkg in packages:
    install_package(pkg)
print("Packages installed !")

os.makedirs("ai", exist_ok=True)
os.makedirs("output", exist_ok=True)
print("-- Downloading the default AI models... --")
print("Downloading the TTS model...")
urlretrieve("https://huggingface.co/NeuML/ljspeech-jets-onnx/resolve/main/model.onnx",
            "ai/ljspeech-jets-onnx/model.onnx")
urlretrieve("https://huggingface.co/NeuML/ljspeech-jets-onnx/resolve/main/config.yaml",
            "ai/ljspeech-jets-onnx/config.yaml")
print("Downloading the T2T model...")
urlretrieve("https://huggingface.co/Orenguteng/Llama-3-8B-Lexi-Uncensored-GGUF/resolve/main/Lexi-Llama-3-8B-Uncensored_Q5_K_M.gguf",
            "ai/Lexi-Llama-3-8B-Uncensored_Q5_K_M.gguf")
print("All files downloaded! You can now start ui.py")



