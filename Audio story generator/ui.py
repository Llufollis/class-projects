import generate
import tkinter as tk
import pyaudio
import wave
import os
import soundfile as sf

def play_audio():
    """
    Play the lats wav file generated.
    In:
        None
    Out:
        None
    """
    chunk = 1024  
    f = wave.open(f"output/story{(len(os.listdir('output')) // 2) - 1}.wav","rb")  
    p = pyaudio.PyAudio()  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    data = f.readframes(chunk)  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)
        #update barre
    stream.stop_stream()  
    stream.close()  
    p.terminate()  
    return None

def hide():
    """
    Hide the play button.
    In:
        None
    Out:
        None
    """
    play_button.grid_remove() 

def display():
    """
    Display the play button.
    In:
        None
    Out:
        None
    """
    play_button.grid(row=2, column=0, pady=5)

def start_generate():
    """
    Generate the text, save it and display it.
    In:
        None
    Out:
        None
    """
    # make
    story = generate.generate_story(text_input.get("1.0", "end-1c"), model = "ai/Lexi-Llama-3-8B-Uncensored_Q5_K_M.gguf")
    audio = generate.text_to_speech(story, model = "ai/ljspeech-jets-onnx")

    # save
    number = len(os.listdir('output')) // 2
    with open(f"output/story{number}.txt", "w") as file:
        file.write(story)
    sf.write(f"output/story{number}.wav", audio, 22050)

    # display
    text_output.delete("1.0", "end-1c")
    text_output.insert("1.0", story)
    display()

    return None


root = tk.Tk()
root.title("AI Story Generator")

upper_part = tk.Frame(root)
lower_part = tk.Frame(root)

text_input = tk.Text(upper_part, height=20, width=40, wrap='word')
text_input.grid(row=0, column=0, padx=5)

update_button = tk.Button(upper_part, text="Generate Story", command=start_generate)
update_button.grid(row=0, column=1)
upper_part.grid(row=0, column=0, padx=5, pady=5)

play_button = tk.Button(root, text="Play Audio", command=play_audio)

text_output = tk.Text(upper_part, height=20, width=40, bg = "light cyan", wrap='word')
text_output.grid(row=0, column=2, padx=5)

text_input.insert("1.0", "Write the story you want here and click on the button 'Generate Story'")
text_output.insert("1.0", "After some time the AI will create and read your story and it will be display here")

hide()

root.mainloop()