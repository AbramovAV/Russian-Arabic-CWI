# Complex Word Identification for Arabic translation of Bible

## Contents

- [Description](#description)
- [Data preparation](#data-preparation)
- [Available data](#available-data)

## Description

This repository contains a set of scripts and all necessary data for training and validating models for lexical complexity prediction for Russian and Arabic languages.

## Data preparation
Scripts for data preparation are stored in `src/data_processing`. The pipeline can be broken into several steps:

- Semi-automatic cleaning of data is done by `refactor_data.py`. It helps to match sentences from Russian Word Complexity corpus with Russian Bible using fuzzy regular expressions, but corrections of typos in both corpora should be done manually.

- Automatic matching of cleaned sentences and verses from aforementioned corpora with extraction of corresponding IDs for verses and subsequent matching of Russian and Arabic verses. The result is corpus with triplets "Russian verse - Arabic verse - annotated complex word", that should be manually annotated by finding matching complex arabic words.

## Available data

- Bible corpus (taken from here: https://github.com/christos-c/bible-corpus). Original corpus contains lots of languages, but this repository needs only Russian and Arabic languages. Russian version of Bible contains several typos, that were manually fixed and cleaned version is stored in a separate file.

- Russian Word Complexity corpus - firstly presented here: Abramov A. V., Ivanov V. V. Collection and evaluation of lexical complexity data for Russian language using crowdsourcing //Russian Journal of Linguistics. – 2022. – Т. 26. – №. 2. – С. 409-425.