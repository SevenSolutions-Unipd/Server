from Levenshtein import distance


def lev_dist(words: list, correctWords: list) -> bool:
    for word in words:
        for correctWord in correctWords:
            if distance(word.lower(), correctWord.lower()) <= acceptable_typos(word, correctWord):
                return True
    return False


def lev_dist_str(words: list, correctWords: list) -> str:
    return lev_dist_generic(words, correctWords, False)


def lev_dist_str_correct_word(words: list, correctWords: list) -> str:
    return lev_dist_generic(words, correctWords, True)


def lev_dist_generic(words: list, correctWords: list, shouldReturnCorrectWord: bool) -> str:
    best_match = 999
    best_word = None

    for word in words:
        for correctWord in correctWords:
            dist = distance(word.lower(), correctWord.lower())

            if dist <= acceptable_typos(word, correctWord) and dist <= best_match:
                best_match = distance(word.lower(), correctWord.lower())
                best_word = correctWord if shouldReturnCorrectWord is True else word

    return best_word


def acceptable_typos(str1: str, str2: str) -> int:
    minLength = min(len(str1), len(str2))

    if minLength < 3:
        return 0
    elif minLength <= 4:
        return 1
    elif minLength <= 8:
        return 2
    else:
        return 3
