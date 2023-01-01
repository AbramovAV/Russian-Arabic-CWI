from xml.etree import ElementTree as ET
import pandas as pd
import regex
from tqdm import tqdm

if __name__ == "__main__":
    tree = ET.parse("data/russian/Russian.xml")
    dataset = pd.read_csv("data/russian/word_complexity_ru.tsv", sep="\t")
    sentences = dataset["sentence"].str.strip().to_list()
    bible = tree.getroot().find("text").find("body")
    count = 0
    for ERR_THRESH in range(1,11):
        THRESH = f"{{e<={ERR_THRESH}}}"
        for book in tqdm(bible.findall("div")):
            for chapter in book.findall("div"):
                for verse in chapter.findall("seg"):
                    verse_text = regex.sub(r" {2,}", " ", verse.text.strip())
                    for sentence in sentences:
                        #removing round brackets so that regex doesn't throw an error for missing ones
                        verse_matching = verse_text.replace("(","").replace(")","")
                        sentence_matching = sentence.replace("(","").replace(")","")
                        res = regex.match(fr'({verse_matching}){THRESH}', sentence_matching, regex.BESTMATCH)
                        if res is not None:
                            count += 1
                            num_tabs = verse.text.count("\t")
                            verse.text = "\n" + "\t"*(num_tabs//2) + sentence + "\n" + "\t"*(num_tabs//2)
                            sentences.remove(sentence)
                            break
    print(count)
    tree.write("data/russian/Russian_cleaned.xml", encoding="utf-8")
    