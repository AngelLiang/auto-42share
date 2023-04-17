import csv


def read_questions():
    questions = []
    with open('questions.csv', encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            questions.append(row)
    print(f'一共读取{len(questions)}组问题')
    return questions


read_questions()
