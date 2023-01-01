import pandas as pd
from load_bible import load_xml_bible

def load_complexity_dataset(file_path:str) -> pd.DataFrame:
    dataset = pd.read_csv(file_path, sep="\t")
    return dataset

def find_matching_verse_ids(dataset:pd.DataFrame, bible_verses:pd.DataFrame) -> pd.Series:
    sentences = dataset.loc[:, "sentence"]
    bible_verses = bible_verses.set_index("verse", inplace=False)
    verse_ids = bible_verses.loc[sentences].reset_index()["id"]
    return verse_ids

def find_matching_verses(bible_verses:pd.DataFrame, verse_ids:pd.Series) -> pd.Series:
    bible_verses = bible_verses.set_index("id", inplace=False)
    matching_verses = bible_verses.loc[verse_ids].reset_index()["verse"]
    return matching_verses

def build_parallel_corpus(ru_verses:pd.DataFrame, ar_verses:pd.DataFrame, verse_ids:pd.Series, dataset:pd.DataFrame) -> pd.DataFrame:
    ru_matching_verses = find_matching_verses(ru_verses, verse_ids)
    ar_matching_verses = find_matching_verses(ar_verses, verse_ids)
    parallel_corpus = {"Russian": ru_matching_verses,
                       "Arabic": ar_matching_verses,
                       "Target": dataset["token"]
    }
    return pd.DataFrame(parallel_corpus)



if __name__=='__main__':
    ru_complexity_dataset = load_complexity_dataset("data/russian/word_complexity_ru.tsv")
    ru_bible_verses = load_xml_bible("data/russian/Russian_cleaned.xml")
    ar_bible_verses = load_xml_bible("data/arabic/Arabic.xml")
    verse_ids = find_matching_verse_ids(ru_complexity_dataset, ru_bible_verses)
    print(f"Number of extracted ids: {len(verse_ids)}")
    parallel_corpus = build_parallel_corpus(ru_bible_verses, ar_bible_verses, verse_ids, ru_complexity_dataset)
    parallel_corpus.to_csv("data/parallel/parallel_complexity_corpus.tsv", sep="\t")
