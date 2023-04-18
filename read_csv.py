import csv


def read_questions(filepath='questions.csv'):
    questions = []
    with open(filepath, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            questions.append(row)
    print(f'一共读取{len(questions)}组问题')
    return questions


if __name__ == '__main__':
    read_questions()
