from pythainlp.corpus import thai_words
import numpy as np
import fasttext
from sklearn.neighbors import NearestNeighbors
import joblib

def check_spell_correction(keyword):
    words = thai_words()
    words = np.array(list(words))
    words_str = '\n'.join(words)
    words_char = list(words_str)
    with open('words-char.txt', mode='w', encoding='utf-8') as file:
        file.write(' '.join(words_char))
    model = fasttext.train_unsupervised('words-char.txt',
                                        epoch=200,
                                        ws=4)
    words_vec = [model.get_sentence_vector(' '.join(list(word))) for word in words]
    words_vec = np.array(words_vec)
    model.save_model('char2vec.bin')  # Model from fastText
    X, y = words_vec, words
    nbrs = NearestNeighbors().fit(X, y)
    joblib.dump(words, 'words.joblib')
    joblib.dump(nbrs, 'nbrs.joblib');
    model = fasttext.load_model('char2vec.bin')
    words = joblib.load('words.joblib')
    nbrs = joblib.load('nbrs.joblib')

    # words set with random mistake

    words_input = [keyword]

    # Test Model
    word_input_vec = [model.get_sentence_vector(' '.join(list(word))) for word in words_input]
    indices = nbrs.kneighbors(word_input_vec, 2, False)  # n_neighbors is 5
    suggestion = words[indices]
    give_suggestion = []
    for i, word in enumerate(words_input):
        if word != suggestion[i][0]:
            give_suggestion.append(np.array(suggestion[i]).tolist())
    if len(give_suggestion)!=0:
        return {'suggestion':give_suggestion[0]}
    else:
        return {'suggestion':keyword}


if __name__ == '__main__':
    print(check_spell_correction('ราคาา'))
