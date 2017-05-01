# -*- coding: utf-8 -*-
from PIL import Image
from crabigator.wanikani import WaniKani
import codecs
import os
import platform


CWD = os.getcwd()

# kanji contains all PNG-files from: https://github.com/downloads/cayennes/kanji-colorize/kanji-colorize-spectrum-png.zip
STROKES_DIR = os.path.join(CWD, "assets", "kanji_strokes")
KANJI_BOXES_DIR = os.path.join(CWD, "assets", "kanji_boxes")
KANJI_ROW_IMAGE = os.path.join(CWD, "assets", "latex", "kanji-row.png")

KANJI_OUTPUT_DIR = os.path.join(CWD, "out", "kanji")
VOCAB_OUTPUT_DIR = os.path.join(CWD, "out", "vocabulary")



# Add you WaniKani API-KEY here
WK_API_KEY = ""
wanikani = WaniKani(WK_API_KEY)

KANJI_TYPE = "Kanji"
VOCAB_TYPE = "Vocabulary"

# Number of kanji per page
KANJI_PP = 5

latex_head_path = os.path.join(CWD, "assets/latex/header.tex")
with open(latex_head_path, "r") as latex_header:
    LATEX_HEAD = latex_header.read()

latex_foot_path = os.path.join(CWD, "assets/latex/footer.tex")
with open(latex_foot_path, "r") as latex_footer:
    LATEX_FOOT = latex_footer.read()

if not os.path.exists(KANJI_BOXES_DIR):
    os.makedirs(KANJI_BOXES_DIR)
    
if not os.path.exists(KANJI_OUTPUT_DIR):
    os.makedirs(KANJI_OUTPUT_DIR)

def create_kanji(kanji):

    # Get the unicode of that kanji
    kanji_code = repr(kanji)[4:8]
    kanji_filename = kanji + ".jpg"
    
    # Open the images
    kanji_img_path = os.path.join(STROKES_DIR, kanji + ".png")
    kanji_img = Image.open(kanji_img_path).convert("RGBA")

    # Get kanji with and kanji height
    kanji_width, kanji_height = kanji_img.size
    inc = kanji_width

    # Resize transparency
    kanji_img.load()
    bands = kanji_img.split()
    bands = [b.resize((inc*2, inc*2), Image.LINEAR) for b in bands]
    kanji_img = Image.merge("RGBA", bands)

    blank_box_path = os.path.join(CWD, "assets", "latex", "kanji327.png")
    blank_box = Image.open(blank_box_path)
        
    num_boxes = 12
    max_width = inc * num_boxes
    
    # Create a new image
    new_img = Image.new("RGBA", (max_width, inc * 2))
    
    i = 0
    while i < num_boxes:
        
        new_img.paste(blank_box, (i * inc, 0))
        new_img.paste(blank_box, (i * inc, inc))
        
        i += 1
        
    new_img.paste(kanji_img, (0,0))
    
    outpath = os.path.join(KANJI_BOXES_DIR, kanji_filename)
        
    new_img.save(outpath)
    
    return os.path.abspath(outpath)

def create_blank_box(num_boxes):

    blank_box_path = os.path.join(CWD, "kanji327.png")
    blank_box = Image.open(blank_box_path)

    box_width, box_height = blank_box.size
    inc = box_width
    max_width =  inc * num_boxes

    new_img = Image.new("RGBA", (max_width, inc * 2))

    i = 0
    while i < num_boxes:

        new_img.paste(blank_box, (i * inc, 0))
        new_img.paste(blank_box, (i * inc, inc))

        i += 1

    outpath = os.path.join(CWD, "kanji-row.png")
    new_img.save(outpath)


def create_title(type, lvl):

    title = "WaniKani " + type + " -- " + " Level " + str(lvl)
    lvl_head = LATEX_HEAD.replace("\\title{}", "\\title{" + title + "}")
    lvl_head = lvl_head.replace("\\fancyhead[C]{}", "\\fancyhead[C]{" + title + "}")

    return lvl_head


def create_kanji_lesson(lvl):

    # Get list of kanji items for the level
    kanji_list = wanikani.get_kanji(levels=[lvl])

    title = create_title(KANJI_TYPE, lvl)
    latex_string = title
    
    counter = 0
    firstpage = True
    
    # Iterate over the list of kanji
    for kanji_info in kanji_list:
        
        counter += 1
        
        kanji = kanji_info.character
        kanji_description = "\\noindent " + str(kanji) + " -- "


        onyomi = ""
        if kanji_info.onyomi:
            onyomi = ", ".join(kanji_info.onyomi)
            kanji_description +=  "On'yomi: " + str(onyomi) + " -- "
            
        kunyomi = ""
        if kanji_info.kunyomi:
            kunyomi = ", ".join(kanji_info.kunyomi)
            kanji_description += " Kun'yomi: " + str(kunyomi) + " -- "
            
        meaning = ", ".join(kanji_info.meaning)
        kanji_description += meaning + " \\newline\n"
        
        img_path = create_kanji(kanji)
        includepath = r"\includegraphics[height=0.12\textheight]{" + img_path.replace("\\", "/") + r"}"
        
        latex_kanji= kanji_description + includepath + "\n\n\\vspace{10pt}\n\n"
        
        latex_string += latex_kanji
        
        if firstpage == True and counter == KANJI_PP - 1:
            counter = 0
            firstpage = False
            latex_string += "\pagebreak\n\n"
        elif counter % KANJI_PP == 0:
            latex_string += "\pagebreak\n\n"
    
    latex_string += LATEX_FOOT

    latex_dirname = "WK-Kanji-" + str(lvl)
    latex_dirpath = os.path.join(KANJI_OUTPUT_DIR, latex_dirname)

    latex_filename = latex_dirname + ".tex"
    latex_filepath = os.path.join(latex_dirpath, latex_filename)
        
    if not os.path.exists(latex_dirpath):
          os.makedirs(latex_dirpath)

    with codecs.open(latex_filepath, "w", "utf8") as latex_file:
        print()
        latex_file.write(latex_string)
        latex_file.close()

    os.chdir(latex_dirpath)

    if platform.system() in ["Linux", "Darwin"]:
        os.system("xelatex " + latex_filepath)
    elif platform.system() == "Windows":
        os.system("xelatex " + latex_filepath)
    os.chdir(CWD)

def create_vocab_lession(lvl):


    vocab_list = wanikani.get_vocabulary(levels=[lvl])

    title = create_title(VOCAB_TYPE, lvl)
    latex_string = title

    counter = 0
    firstpage = True

    for vocab in vocab_list:

        counter += 1

        vocab_description = ""

        kana = ""
        if vocab.kana:
            kana += "Kana: " + ", ".join(vocab.kana) + " -- "
            vocab_description += kana

        meaning = ""
        if vocab.meaning:
            meaning += "Meaning: " + ", ".join(vocab.meaning)
            vocab_description += meaning + " \\newline\n"


        includepath = r"\includegraphics[height=0.12\textheight]{" + KANJI_ROW_IMAGE.replace("\\", "/") + r"}"

        latex_vocab = vocab_description + includepath + "\n\n\\vspace{10pt}\n\n"

        latex_string += latex_vocab

        if firstpage == True and counter == KANJI_PP - 1:
            counter = 0
            firstpage = False
            latex_string += "\pagebreak\n\n"
        elif counter % KANJI_PP == 0:
            latex_string += "\pagebreak\n\n"

    latex_string += LATEX_FOOT

    latex_dirname = "WK-Vocab-" + str(lvl)
    latex_dirpath = os.path.join(VOCAB_OUTPUT_DIR, latex_dirname)

    latex_filename = latex_dirname + ".tex"
    latex_filepath = os.path.join(latex_dirpath, latex_filename)

    if not os.path.exists(latex_dirpath):
      os.makedirs(latex_dirpath)

    with codecs.open(latex_filepath, "w", "utf-8") as latex_file:
        latex_file.write(latex_string)
        latex_file.close()

    os.chdir(latex_dirpath)

    if platform.system() in ["Linux", "Darwin"]:
        os.system("xelatex " + latex_filepath)
    elif platform.system() == "Windows":
        os.system("xelatex " + latex_filepath)
    os.chdir(CWD)


for i in range(1, 61):
    create_kanji_lesson(i)
    create_vocab_lession(i)

