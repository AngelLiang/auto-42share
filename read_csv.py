import csv
import chardet
import log


def guess_encoding(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()
        return chardet.detect(content)['encoding']


def read_questions(filepath='questions.csv'):
    encoding = guess_encoding(filepath)
    log.logger.info(f'{filepath} encoding:{encoding}')
    questions = []
    with open(filepath, encoding=encoding) as f:
        reader = csv.reader(f)
        for row in reader:
            questions.append(row)
    log.logger.info(f'一共读取{len(questions)}组问题')
    return questions


if __name__ == '__main__':
    read_questions()
