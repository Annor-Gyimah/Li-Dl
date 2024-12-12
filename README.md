# Dynamite Download Manager (DDM)
# 

Dynamite Download Manager is a powerful download manager equipped with multi-connections and a high-speed engine,  designed to enhance your downloading experience. By utilizing multiple connections, 
DDM splits files into smaller segments and downloads them simultaneously, significantly increasing download speeds. Its advanced high-speed engine ensures faster and more efficient downloading, even for large files.
DDM supports a wide variety of file formats, enabling you to download general files, software, documents, and much more with ease. Additionally, it allows you to download videos from platforms like YouTube and Vimeo, as well as from tons of other streaming websites, making it a go-to tool for both regular and media-centric downloads. Its intuitive interface and robust features make it an essential tool for anyone looking to speed up their internet downloads while managing files effortlessly.

> ## :gift: **//// DONATE ////**
> ## 🔗 Donate (Gumroad): https://gum.co/mHsRC
> This interface is free for any use, but if you are going to use it commercially, consider helping to maintain this project and others with a donation by Gumroado at the link above. This helps to keep this and other projects active.

> **Warning**: this project was created using PySide6 and Python 3.9, using previous versions can cause compatibility problems.

# YouTube - Presentation And Tutorial
Presentation and tutorial video with the main functions of the user interface.
> 🔗 https://youtu.be/9DnaHg4M_AM

# Screenshots
![PyDracula_Default_Dark](https://github.com/Annor-Gyimah/Li-Dl/blob/master/Linux/images/down.png)
![PyDracula_Light](https://github.com/Annor-Gyimah/Li-Dl/blob/master/Linux/images/down2.png)

# High DPI
> Qt Widgets is an old technology and does not have a good support for high DPI settings, making these images look distorted when your system has DPI applied above 100%.
You can minimize this problem using a workaround by applying this code below in "main.py" just below the import of the Qt modules.
```python
# ADJUST QT FONT DPI FOR HIGHT SCALE
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96"
```

# Running
> Inside your preferred terminal run the commands below depending on your system, remembering before installing Python 3.9> and requirements.txt "pip install -r requirements.txt".
> ## **Windows**:
```console
pip install -r requirements.txt
```
```console
python main.py
```

> ## **MacOS and Linux**:
```console
python3 main.py
```



# Projects Created Using PyDracula
**See the projects that were created using PyDracula.**
> To participate create a "Issue" with the name beginning with "#pydracula_project", leaving the link of your project on Github, name of the creator and what is its functionality. Your project will be added and this list will be deleted from "Issue".
**Malicious programs will not be added**!



