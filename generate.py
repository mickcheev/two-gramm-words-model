import re
import pickle
import argparse
import numpy


def generate_list_of_probability(source: dict):
    """
    param: source is a dict from trained model
    contains an amount of repeats of every word
    that could stand after current prefix.
    """
    result = []
    for key in source.keys():
        result += [key] * source[key]
    return result


class Model:
    """
    Class of already trained
    model
    """

    def __init__(self, model_path, length, prefix=None):
        self.path = model_path
        self.length = int(length)
        self.prefix = prefix
        self.model = {}
        self.result = ''

    def fip(self):
        """
        Loads the model from pkl file
        """
        with open(self.path, 'rb') as file:
            self.model = pickle.load(file)

    def generate(self):
        """
        Creates the new text
        from trained model
        """

        if self.prefix is None:
            self.prefix = numpy.random.choice(list(self.model['$PREFIXs'].keys()))
            self.prefix.strip()
        else:
            pattern = re.compile(r'[а-яА-Я]+|[.,?!]')
            self.prefix = list(map(str.lower, re.findall(pattern=pattern, string=self.prefix)))[-1]
        self.result = str.capitalize(self.prefix)

        while self.length > 0:
            if self.prefix in ('.', '!', '?', ','):
                word = '.'
                while word in ('.', '!', '?', ','):
                    word = numpy.random.choice(generate_list_of_probability(self.model['$PREFIXs'][self.prefix]))
            else:
                word = numpy.random.choice(generate_list_of_probability(self.model['$PREFIXs'][self.prefix]))

            if len(word) == 1 and word not in (',', '!', '.', '?'):
                continue

            if word in (',', '!', '?', '.'):
                self.result += word

            elif self.result[-1] in ('.', '!', '?'):
                self.length -= 1
                self.result += ' ' + str.capitalize(word)
            else:
                self.length -= 1
                self.result += ' ' + word
            self.prefix = word

        if self.result[-1] not in ('!', '?', '.'):
            self.result += '.'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ready model')
    parser.add_argument('--prefix')
    parser.add_argument('--length')
    parser.add_argument('--model')

    args = parser.parse_args()
    model = Model(args.model, args.length, args.prefix)
    model.fip()
    model.generate()
    print(model.result)
