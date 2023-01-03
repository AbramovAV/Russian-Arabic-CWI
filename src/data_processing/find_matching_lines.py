"""
This module matches annotated sentences from
word complexity corpus with Russian verses from Bible
and extracts corresponding Arabic verses.
"""

import pandas as pd
from load_bible import load_xml_bible

def load_complexity_dataset(file_path:str) -> pd.DataFrame:
    """
    Loads Russian word complexity corpus as CSV file with 
    TAB as separator and represents it as DataFrame with 
    5 columns: "sentence", "token", "start", "end", "complexity".

    Args:
        file_path: path to tsv file with corpus.

    Returns:
        Pandas DataFrame with 5 columns, where each row
        represents a record: "context-target-score-positions_of_target".
    """
    dataset = pd.read_csv(file_path, sep="\t")
    return dataset

def find_matching_verse_ids(dataset:pd.DataFrame, bible_verses:pd.DataFrame) -> pd.Series:
    """
    Matches sentences from annotated word complexity corpus with
    Bible corpus to obtain corresponding ids for verses.
    Important: both datasets should be cleaned beforehand.

    Args:
        dataset: DataFrame with word complexity dataset
        bible_verses: DataFrame with Bible verses and their ids.

    Returns:
        Pandas Series with corresponding verse ids.
    """
    sentences = dataset.loc[:, "sentence"]
    bible_verses = bible_verses.set_index("verse", inplace=False)
    verse_ids = bible_verses.loc[sentences].reset_index()["id"]
    return verse_ids

def find_matching_verses(bible_verses:pd.DataFrame, verse_ids:pd.Series) -> pd.Series:
    """
    Finds verses from Bible by a given set of ids.

    Args:
        bible_verses: DataFrame with Bible verses and their ids
        verse_ids: Series with ids of verses to search for.

    Returns:
        Pandas Series with corresponding verses.
    """
    bible_verses = bible_verses.set_index("id", inplace=False)
    matching_verses = bible_verses.loc[verse_ids].reset_index()["verse"]
    return matching_verses

def build_parallel_corpus(ru_verses:pd.DataFrame, ar_verses:pd.DataFrame, verse_ids:pd.Series, dataset:pd.DataFrame) -> pd.DataFrame:
    """
    Constructs parallel corpus with corresponding Russian and Arabic
    verses from Bible and words, extraced from word complexity corpus.

    Args:
        ru_verses: DataFrame with Russian Bible verses and their ids
        ar_verses: DataFrame with Arabic Bible verses and their ids
        verse_ids: Series with ids of verses to search for
        dataset: DataFrame with word complexity dataset

    Returns:
        DataFrame with 3 columns, where each row represents a triplet:
        "Russsian verse - Arabic verse - annotated russian word".
    """
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
