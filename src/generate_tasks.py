import sqlite3
import random

def generate_examples(n: int):
    conn = sqlite3.connect("database/database.sqlite")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Examples")
    
    examples = []
    while len(examples) != n:
        num1 = random.randint(100, 999)  
        num2 = random.randint(100, 999)  
        operation = random.choice(['+', '-']) 
        if operation == '+':
            expression = f"{num1} + {num2}"
            correct_answer = num1 + num2
        else:
            expression = f"{num1} - {num2}"
            correct_answer = num1 - num2
        if ((expression, correct_answer)) not in examples:
            examples.append((expression, correct_answer))

    cursor.executemany("INSERT INTO Examples (Expression, CorrectAnswer) VALUES (?, ?)", examples)
    conn.commit()
    conn.close()
    print(f"Сгенерировано {n} примеров и добавлено в базу данных.")


if __name__ == "__main__":
    generate_examples(10000)