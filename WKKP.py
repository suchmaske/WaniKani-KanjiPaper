# -*- coding: utf-8 -*-

from PIL import Image
import json
import os
import platform
import sys
import urllib, urllib2

reload(sys).setdefaultencoding("utf-8")

CWD = os.getcwd()

# KanjiStrokes contains all PNG-files from: https://github.com/downloads/cayennes/kanji-colorize/kanji-colorize-spectrum-png.zip
STROKES_DIR = os.path.join(CWD, "KanjiStrokes")
OUTPUT_DIR = os.path.join(CWD, "KanjiImages")

LATEX_DIR = os.path.join(CWD, "KanjiPaper")
VOCAB_LATEX_DIR = os.path.join(CWD, "VocabPaper")

KANJI_ROW_IMAGE = os.path.join(CWD, "kanji-row.png")

# Add you WaniKani API-KEY here
WK_KEY = ""
WK_API = "https://www.wanikani.com/api/user/" + WK_KEY
WK_KANJI = WK_API + "/kanji/"
WK_VOCAB = WK_API + "/vocabulary/"

KANJI_TYPE = "Kanji"
VOCAB_TYPE = "Vocabulary"

KANJI_PP = 5

LATEX_HEAD = """
\documentclass[a4paper,11pt]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}

\usepackage{hyperref}
\usepackage[left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm,includeheadfoot]{geometry}
\usepackage{graphicx}
\usepackage{fancyhdr}

\usepackage{zxjatype}
\usepackage[ipa]{zxjafont}

\\title{}
\\author{}

\\fancyhf{}
\\fancyhead[C]{}
% \\fancyfoot[L]{The stroke order diagrams were taken from: \url{http://lingweb.eva.mpg.de/kanji/}. Copyright owner of the diagrams is Ulrich Apel.}
\pagestyle{fancy}

\\fancyfoot[L]{\\tiny{This writing excercise was generated using WaniKani\_KanjiPaper (\url{https://github.com/suchmaske/WaniKani-KanjiPaper}). It relies on the stroke order diagrams produced by cayennes' kanji-colorize (\url{https://github.com/cayennes/kanji-colorize}) using KanjiVG (\url{https://github.com/KanjiVG/kanjivg} -- Creative Commons 3.0 (SA) by Ulrich Apel)}}

\\begin{document}


\maketitle


"""

LATEX_FOOT = """



\end{document}
"""

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    
if not os.path.exists(LATEX_DIR):
    os.makedirs(LATEX_DIR)

def create_kanji(kanji):

    # Get the unicode of that kanji
    kanji_code = repr(kanji)[4:8]
    kanji_filename = kanji_code + ".jpg"
    
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

    blank_box_path = os.path.join(CWD, "Kanji327.png")
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
    
    outpath = os.path.join(OUTPUT_DIR, kanji_filename)
        
    new_img.save(outpath)
    
    return os.path.abspath(outpath)

def create_blank_box(num_boxes):

    blank_box_path = os.path.join(CWD, "Kanji327.png")
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
    
    # Build the API URL for this level
    kanji_lvl = WK_KANJI + str(lvl)
    print kanji_lvl
    
    # Read the JSON data and get requested information
    response = urllib2.urlopen(kanji_lvl)
    kanji_json = json.load(response)["requested_information"]
    
    title = create_title(KANJI_TYPE, lvl)
    latex_string = title
    
    counter = 0
    firstpage = True
    
    # Iterate over the list of kanji
    for kanji_info in kanji_json:
        
        counter += 1
        
        kanji = kanji_info["character"]
        kanji_description = "\\noindent " + str(kanji) + " -- "
        
        onyomi = ""
        if "onyomi" in kanji_info:
            onyomi = kanji_info["onyomi"]
            kanji_description +=  "On'yomi: " + str(onyomi) + " -- "
            
        kunyomi = ""
        if "kunyomi" in kanji_info:
            kunyomi = kanji_info["kunyomi"]
            kanji_description += " Kun'yomi: " + str(kunyomi) + " -- "
            
        meaning = kanji_info["meaning"]
        kanji_description += meaning + " \\newline\n"
        
        img_path = create_kanji(unicode(kanji))
        includepath = "\includegraphics[height=0.12\\textheight]{" + img_path.replace("\\", "/") + "}\n"
        
        latex_kanji= kanji_description + includepath + "\\vspace{10pt}\n\n"
        
        latex_string += latex_kanji
        
        if firstpage == True and counter == KANJI_PP - 1:
            counter = 0
            firstpage = False
            latex_string += "\pagebreak\n\n"
        elif counter % KANJI_PP == 0:
            latex_string += "\pagebreak\n\n"
    
    latex_string += LATEX_FOOT

    latex_dirname = "WK-Kanji-" + str(lvl)
    latex_dirpath = os.path.join(LATEX_DIR, latex_dirname)

    latex_filename = latex_dirname + ".tex"
    latex_filepath = os.path.join(latex_dirpath, latex_filename)
        
    if not os.path.exists(latex_dirpath):
          os.makedirs(latex_dirpath)

    latex_file = open(latex_filepath, "wb")
    
    latex_file.write(latex_string)
    
    latex_file.close()

    os.chdir(latex_dirpath)

    if platform.system() in ["Linux", "Darwin"]:
        os.system("xelatex " + latex_filepath)
    elif platform.system() == "Windows":
        os.system("xelatex " + latex_filepath)
    os.chdir(CWD)

def create_vocab_lession(lvl):

    print "AAAAAA " + str(lvl)
    vocab_lvl = WK_VOCAB + str(lvl)
    print vocab_lvl


    response = urllib2.urlopen(vocab_lvl)
    vocab_json = json.load(response)["requested_information"]

    title = create_title(VOCAB_TYPE, lvl)
    latex_string = title

    counter = 0
    firstpage = True

    for vocab in vocab_json:

        counter += 1

        vocab_description = ""

        kana = ""
        if "kana" in vocab:
            kana += "Kana: " + str(vocab["kana"]) + " -- "
            vocab_description += kana

        meaning = ""
        if "meaning" in vocab:
            meaning += "Meaning: " + str(vocab["meaning"])
            vocab_description += meaning + " \\newline\n"


        includepath = "\includegraphics[height=0.12\\textheight]{" + KANJI_ROW_IMAGE.replace("\\", "/") + "}\n"

        latex_vocab = vocab_description + includepath + "\\vspace{10pt}\n\n"

        latex_string += latex_vocab

        if firstpage == True and counter == KANJI_PP - 1:
            counter = 0
            firstpage = False
            latex_string += "\pagebreak\n\n"
        elif counter % KANJI_PP == 0:
            latex_string += "\pagebreak\n\n"

    latex_string += LATEX_FOOT

    latex_dirname = "WK-Vocab-" + str(lvl)
    latex_dirpath = os.path.join(VOCAB_LATEX_DIR, latex_dirname)

    latex_filename = latex_dirname + ".tex"
    latex_filepath = os.path.join(latex_dirpath, latex_filename)

    if not os.path.exists(latex_dirpath):
      os.makedirs(latex_dirpath)

    latex_file = open(latex_filepath, "wb")

    latex_file.write(latex_string)

    latex_file.close()

    os.chdir(latex_dirpath)

    if platform.system() in ["Linux", "Darwin"]:
        os.system("xelatex " + latex_filepath)
    elif platform.system() == "Windows":
        os.system("xelatex " + latex_filepath)
    os.chdir(CWD)



# create_blank_box(12)




for i in range(1, 51):
    create_kanji_lesson(i)
    create_vocab_lession(i)
