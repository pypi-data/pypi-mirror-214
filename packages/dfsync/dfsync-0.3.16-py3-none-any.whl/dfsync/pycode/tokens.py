from pprint import pprint
from collections import defaultdict

"""
https://aclanthology.org/D19-6221.pdf - negation & speculation
https://aclanthology.org/2020.findings-emnlp.414.pdf - UnigramLM

"""


def get_vocab(data):
    vocab = defaultdict(int)
    for word in data:
        for char in word:
            vocab[char] += 1
    return vocab


def get_pairs(vocab):
    pairs = defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i + 1]] += freq
    return pairs


def merge_vocab(pair, v_in):
    v_out = {}
    bigram = " ".join(pair)
    for word in v_in:
        w_out = word.replace(bigram, "".join(pair))
        v_out[w_out] = v_in[word]
    return v_out


def modify_bpe(data, num_merges):
    # Add prefix "not_" to negated phrases
    modified_data = []
    for word in data:
        if word.startswith("not ") or word.startswith("not_"):
            modified_data.append("not_" + word[4:])
        else:
            modified_data.append(word)

    # Create the vocabulary
    vocab = get_vocab(modified_data)
    for i in range(num_merges):
        pairs = get_pairs(vocab)
        if not pairs:
            break
        best_pair = max(pairs, key=pairs.get)
        vocab = merge_vocab(best_pair, vocab)

        # Remove prefix "not_" from token
        # if it's the first token of the word
        for word in vocab:
            if word.startswith("not_"):
                tokens = word.split()
                if tokens[0] == "not_":
                    vocab[word[4:]] = vocab.pop(word)

    # Reverse prefix "not_" for output
    output_vocab = {}
    for word in vocab:
        if word.startswith("not_"):
            output_vocab[word[4:]] = vocab[word]
        else:
            output_vocab[word] = vocab[word]
    return output_vocab


from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")

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
NEGATION = "not_"


def gpt_main():
    vocab = get_vocab(body_words)
    pprint(vocab)

    pairs1 = get_pairs(vocab)
    pprint(pairs1)

    freq = modify_bpe(body_words, 4)
    pprint(freq)


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

    pprint(vocab)
    pprint(merges)


def main():
    regular_bpe(body_words)


if __name__ == "__main__":
    main()
