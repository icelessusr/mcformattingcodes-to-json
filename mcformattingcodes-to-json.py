import json
import tkinter as tk
import time
import threading

preferConfig = {
    "italic": False
}

defaultConfig = {
    "color": "dark_purple",
    "bold": False,
    "italic": True,
    "underlined": False,
    "strikethrough": False,
    "obfuscated": False
}

colorTable = {
    "0": "black",
    "1": "dark_blue",
    "2": "dark_green",
    "3": "dark_aqua",
    "4": "dark_red",
    "5": "dark_purple",
    "6": "gold",
    "7": "gray",
    "8": "dark_gray",
    "9": "blue",
    "a": "green",
    "b": "aqua",
    "c": "red",
    "d": "light_purple",
    "e": "yellow",
    "f": "white"
}

results = []

def overwriteDict(old, new):
    processOld = old.copy()
    processOld.update(new)
    return processOld

def configClean(config):
    for item in defaultConfig:
        if item in config and config[item] == defaultConfig[item]:
            del config[item]
    
    return config


def copied():
    status_label.config(text="✅ Copied to clipboard!")
    time.sleep(3)
    status_label.config(text="")


def main():
    text = text_box.get("1.0", tk.END)
    lines = text.split("\n")[:-1]
    
    results = []
    config = overwriteDict(defaultConfig, preferConfig)
    for line in lines:
        if autoReset_seleted.get() == "Every line" or autoReset_seleted.get() == "Every time color is changed and every line":
            config = overwriteDict(defaultConfig, preferConfig)
        

        lineContents = []
        tempText = ""
        skip = 0
        for index, part in enumerate(line):
            if skip > 0:
                skip -= 1
                continue
            if part == "&":
                if tempText != "":
                    lineContents.append(configClean(overwriteDict(config, {"text": tempText})))
                tempText = ""
                if line[index+1] == "#":
                    if autoReset_seleted.get() == "Every time color is changed" or autoReset_seleted.get() == "Every time color is changed and every line":
                        config = overwriteDict(defaultConfig, preferConfig)
                    config["color"] = line[index+1:index+8]
                    skip = 7
                elif line[index+1] == "l":
                    config["bold"] = True
                    skip = 1
                elif line[index+1] == "o":
                    config["italic"] = True
                    skip = 1
                elif line[index+1] == "n":
                    config["underlined"] = True
                    skip = 1
                elif line[index+1] == "m":
                    config["strikethrough"] = True
                    skip = 1
                elif line[index+1] == "k":
                    config["obfuscated"] = True
                    skip = 1
                elif line[index+1] == "r":
                    config = defaultConfig
                    skip = 1
                elif line[index+1] in colorTable:
                    if autoReset_seleted.get() == "Every time color is changed" or autoReset_seleted.get() == "Every time color is changed and every line":
                        config = overwriteDict(defaultConfig, preferConfig)
                    config["color"] = colorTable[line[index+1]]
                    skip = 1
            else:
                tempText += part
        
        lineContents.append(configClean(overwriteDict(config, {"text": tempText})))
                    
        results.append(lineContents)

    root.clipboard_clear()
    root.clipboard_append(json.dumps(results, ensure_ascii=False))
    root.update()
    print(json.dumps(results, indent=4, ensure_ascii=False))
    threading.Thread(target=copied).start()

root = tk.Tk()
root.title("Converter - Iceless")
root.geometry("400x500")

tk.Label(root, text="Enter text below:", font=("Arial", 14)).pack(pady=(10,5))

text_box = tk.Text(root, height=20, width=50)
text_box.pack(pady=10)

autoReset_frame = tk.Frame(root)
autoReset_frame.pack(padx=20, pady=20)


autoReset_options = [
    "Never",
    "Every time color is changed",
    "Every time color is changed and every line",
    "Every line"
]
autoReset_seleted = tk.StringVar(value=autoReset_options[0])

tk.Label(autoReset_frame, text="Auto reset when").pack(side=tk.LEFT, padx=(0, 10))
tk.OptionMenu(autoReset_frame, autoReset_seleted, *autoReset_options).pack(side=tk.LEFT)


tk.Button(root, text="Convert and copy to clipboard", command=main).pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
