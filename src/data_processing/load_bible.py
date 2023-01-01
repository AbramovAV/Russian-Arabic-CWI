from xml.etree import ElementTree as ET
import re
import pandas as pd

def load_xml_bible(xml_path:str) -> pd.DataFrame:
    tree = ET.parse(xml_path)
    bible_verses = {"id":[], "verse":[]}
    bible = tree.getroot().find("text").find("body")
    for book in bible.findall("div"):
        for chapter in book.findall("div"):
            for verse in chapter.findall("seg"):
                verse_id = verse.get("id")
                verse_text = re.sub(r" {2,}", " ", verse.text.strip()) #Russian Bible used to have extra spaces in verses
                bible_verses["id"].append(verse_id)
                bible_verses["verse"].append(verse_text)
    df = pd.DataFrame.from_dict(bible_verses)
    df["verse"] = df["verse"].str.strip()
    return df

if __name__=='__main__':
    russian_bible_verses = load_xml_bible("data/russian/Russian.xml")
    arabic_bible_verses = load_xml_bible("data/arabic/Arabic.xml")
    assert russian_bible_verses.shape == arabic_bible_verses.shape