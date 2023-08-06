import gzip, numpy as np
from collections import defaultdict
from pprint import pprint
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("xlnet-base-cased")


corpus = [
    "This is the Hugging Face Course.",
    "This chapter is about tokenization.",
    "This section shows several tokenizer algorithms.",
    "Hopefully, you will be able to understand how they are trained and generate tokens.",
    "The water is hot.",
    "The water is cold.",
    "I do not like cold water.",
    "Algebra is something you learn in seventh grade.",
    "Warm water is good for showers.",
    "Sometimes I shower in cold water.",
]
body = " ".join(corpus)
words_with_offsets = tokenizer.backend_tokenizer.pre_tokenizer.pre_tokenize_str(body)
body_words = [word for word, offset in words_with_offsets]
SPECIAL = "<|endoftext|>"


def get_word_frequency(corpus_words: list[str]):
    word_freqs = defaultdict(int)
    for word in corpus_words:
        word_freqs[word] += 1
    return word_freqs


def get_alphabet(unique_words):
    alphabet = []
    for word in unique_words:
        for letter in word:
            if letter not in alphabet:
                alphabet.append(letter)
    alphabet.sort()
    return [SPECIAL, *alphabet]


def get_pair_freqs(word_freqs, splits):
    pair_freqs = defaultdict(int)
    for word, freq in word_freqs.items():
        split = splits[word]
        if len(split) == 1:
            continue
        for i in range(len(split) - 1):
            pair = (split[i], split[i + 1])
            pair_freqs[pair] += freq
    return pair_freqs


def get_max_freq_item(item_freqs: dict):
    best = ""
    max_freq = None

    for item, freq in item_freqs.items():
        if max_freq is None or max_freq < freq:
            best = item
            max_freq = freq
    return best, max_freq


def merge_pair(a, b, splits, word_freqs):
    for word in word_freqs:
        split = splits[word]
        if len(split) == 1:
            continue

        i = 0
        while i < len(split) - 1:
            if split[i] == a and split[i + 1] == b:
                split = split[:i] + [a + b] + split[i + 2 :]
            else:
                i += 1
        splits[word] = split
    return splits


def regular_bpe(body_words, vocab_size=60):
    word_freqs = get_word_frequency(body_words)
    vocab = get_alphabet(word_freqs.keys())
    splits = {word: [c for c in word] for word in word_freqs.keys()}

    merges = {}
    while len(vocab) < vocab_size:
        pair_freqs = get_pair_freqs(word_freqs, splits)
        best_pair, freq = get_max_freq_item(pair_freqs)
        splits = merge_pair(*best_pair, splits, word_freqs)

        new_item = best_pair[0] + best_pair[1]
        merges[best_pair] = new_item
        vocab.append(new_item)

    return merges


def tokenize(merges, text):
    pre_tokenize_result = tokenizer._tokenizer.pre_tokenizer.pre_tokenize_str(text)
    pre_tokenized_text = [word for word, offset in pre_tokenize_result]
    splits = [[l for l in word] for word in pre_tokenized_text]
    for pair, merge in merges.items():
        for idx, split in enumerate(splits):
            i = 0
            while i < len(split) - 1:
                if split[i] == pair[0] and split[i + 1] == pair[1]:
                    split = split[:i] + [merge] + split[i + 2 :]
                else:
                    i += 1
            splits[idx] = split

    return sum(splits, [])


def main():
    with gzip.open("enwiki8.gz") as f:
        text_body = f.read(int(95e6))
        pprint(f"body: {len(text_body)} - {text_body[:100]}")

    with gzip.open("enwiki8.gz") as f:
        text_body = f.read(int(95e6))
        data = np.frombuffer(text_body, dtype=np.uint8).copy()
        train_x, valid_x = np.split(data, [int(90e6)])
        pprint(f"data: {len(data)} - {data[:100]}")
        pprint(f"train: {len(train_x)} - {train_x[:50]}")
        pprint(f"valid: {len(valid_x)} - {valid_x[:50]}")

    word_freqs = get_word_frequency(body_words)
    sorted_word_req = sorted(word_freqs.items(), key=lambda item: item[1], reverse=True)
    pprint(sorted_word_req)
    merges = regular_bpe(body_words, vocab_size=100)
    pprint(tokenize(merges, "The water is hot."))
    pprint(tokenize(merges, "The water is not hot."))
    pprint(tokenize(merges, "The water is cold."))


if __name__ == "__main__":
    main()
