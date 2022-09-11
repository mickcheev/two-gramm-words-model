import sys
import os
import re
import pickle
import argparse


def text_to_words(text):
    """
    Returns the list of strings
    separeted by (! . ?)
    symbols
    """
    text = rf'{text}'
    pattern = re.compile(r'[а-яА-Я]+|[.,?!]')
    return list(map(str.lower, re.findall(pattern=pattern, string=text)))


def get_words_from_text(text):
    """
    Returns the list of words
    without any special symbols
    """
    text = rf'{text}'
    return re.split(r'\W+', text)


def words_to_lower(words: list):
    """
    Returns the list of lowered words
    """
    return [word.lower().strip() for word in words]


def get_data_from_folder(data_path):
    """
    Reads data from folder.
    Only txt can be read
    """
    file_list = os.listdir(data_path)
    content = ''

    for name in file_list:
        with open(os.path.join(data_path, name), 'r', encoding="utf8") as file:
            content += file.read() + '.\n'
    return content


def get_stdin_data():
    """
    Reads data from stdin
    """
    content = ''
    for line in sys.stdin:
        if 'q' == line.rstrip():
            break
        else:
            content += line
    return content


class TrainingModel:
    """
    Training model is a class
    to get data sources and compile it
    into the model
    """

    def __init__(self, model_path, input_dir=None):
        self.path = model_path

        if not input_dir:
            self.data = get_stdin_data()
        else:
            self.data = get_data_from_folder(input_dir)

        self.model = {'$PREFIXs': {}}

    def words_processing(self, words):
        """
        Makes binds like
        a two-gramm model
        """
        for i, word in enumerate(words[1:-2]):
            if self.model['$PREFIXs'].get(word) is None:
                self.model['$PREFIXs'][word] = dict()
            if self.model['$PREFIXs'][word].get(words[i + 2]) is None:
                self.model['$PREFIXs'][word][words[i + 2]] = 0
            self.model['$PREFIXs'][word][words[i + 2]] += 1

    def train(self):
        """
        Starting the proccess of the training
        """
        words = text_to_words(self.data)
        self.words_processing(words)

    def save(self):
        """
        Save model object for
        the next using
        """
        with open(self.path, 'wb') as file:
            pickle.dump(self.model, file)
        print('Model has been saved')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Training model')
    parser.add_argument('--input-dir')
    parser.add_argument('--model')

    args = parser.parse_args()
    model = TrainingModel(model_path=args.model, input_dir=args.input_dir)
    model.train()
    model.save()
