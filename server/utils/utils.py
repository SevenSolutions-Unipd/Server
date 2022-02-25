from Levenshtein import distance


def lev_dist(words: list, correctWords: list) -> bool:
    for word in words:
        for correctWord in correctWords:
            if distance(word.lower(), correctWord.lower()) <= 2:
                return True
    return False


def lev_dist_str(words: list, correctWords: list) -> str:
    best_match = 2
    best_word = None

    for word in words:
        for correctWord in correctWords:
            if distance(word.lower(), correctWord.lower()) <= best_match:
                best_match = distance(word.lower(), correctWord.lower())
                best_word = word

    return best_word
