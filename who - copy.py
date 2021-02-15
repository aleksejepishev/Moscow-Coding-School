import random
import yaml
import datetime
from sty import fg

def load_tasks_from(filename):
    try:
        file = open(filename, 'r', encoding='utf8')
        TASKS = yaml.safe_load(file.read())
    except:
        print('Something went wrong!')
    else:
        file.close()
        return TASKS

TASKS = load_tasks_from("tasks.yml")

def get_steps_for(tasks):
    steps = list(tasks)
    steps.sort()
    return steps

STEPS = get_steps_for(TASKS)

def get_question(step, index = None):
    step = STEPS[step]
    i = random.choice(range(len(TASKS[step])))
    question_dict = TASKS[step][i]  
    random_question = question_dict['question']
    random_answers = question_dict['answers']
    correct_answer = str(question_dict['answers'][0]).strip()
    if index == 0 or index == 1:
        again = TASKS[step][index]['question']
        again_answers = TASKS[step][index]['answers']
        again_correct = str(TASKS[step][index]['answers'][0]).strip()
        return again, again_answers, again_correct
    return random_question, random_answers, correct_answer, i

def prepare_answers(answers):
    mix = random.sample(answers, len(answers))
    letters = ['A', 'B', 'C', 'D']
    prepared_answers = dict(zip(letters, mix)) #just put in a dictionary!
    return prepared_answers

def display_answers(answers):
    for key in answers:
        print(f"{key}. {answers[key]}")

def user_input(answers):
    user_answer = input('Enter your answer (A, B, C, D): ').strip().upper()
    if user_answer == 'Q':
        return user_answer
    return answers[user_answer] if user_answer in answers else user_input(answers)

def check_answer(user_answer, correct_answer, step, shot = None): #shot - is a number of tries
    result = {}
    if user_answer == correct_answer and (step + 1) != len(STEPS):
        result['status'] = 'next_step'
        result['step'] =  step + 1
    elif user_answer == correct_answer and (step + 1) == len(STEPS):
        result['status'] = 'win'
        result['prize'] = STEPS[step]
    elif user_answer == 'Q':
        result['status'] = 'quit'
        result['prize'] = 0 if step == 0 else STEPS[step-1]
    elif user_answer != correct_answer and shot == 2:
        result['status'] = 'lose'
        result['prize'] = 0 if step == 0 else STEPS[step-1]
    elif user_answer != correct_answer and shot == 1: #here is a shot
        result['status'] = 'retry'   
        result['shot'] = 1
    elif user_answer != correct_answer:
        result['status'] = 'retry'
        result['shot'] = 0
    else:
        result['status'] = 'lose'
        result['prize'] = 0 if step == 0 else STEPS[step-1]
    return result
  
def get_result(user_result, random_question = None, random_answers = None, correct_answer = None, i = None, step = None):
    if user_result['status'] == 'win':
        print(fg.yellow + 'You win!' + fg.rs)
        return user_result['prize']
    elif user_result['status'] == 'next_step':
        print('Right! Lets go to the next!')
        return next_question(user_result['step'])
    elif user_result['status'] == 'quit':
        print("You decided to finish the game. Here is your money:")
        return user_result['prize']
    elif user_result['status'] == 'retry' and user_result['shot'] == 0:
        print('One more time!')
        print(f"You have {user_result['shot'] + 2} more efforts!")
        print(f"This is your question {random_question}")
        answers = prepare_answers(random_answers)
        display_answers(answers)
        user_guess = user_input(answers)
        user_result = check_answer(user_guess, correct_answer, step, shot = 1)
        return get_result(user_result) if user_result['status'] != 'retry' else get_result(user_result, random_question, random_answers, correct_answer, i, step)
    elif user_result['status'] == 'retry' and user_result['shot'] == 1:
        print('One more time!')
        print(f"You have {user_result['shot']} more effort!")
        print(f"This is your question: \n{random_question}")
        answers = prepare_answers(random_answers)
        display_answers(answers)
        user_guess = user_input(answers)
        user_result = check_answer(user_guess, correct_answer, step, shot = 2)
        return get_result(user_result) if user_result['status'] != 'retry' else get_result(user_result, random_question, random_answers, correct_answer, i, step)
    else:
        print('You loose')
        return user_result['prize']

def next_question(step = 0, index = None):
    random_question, random_answers, correct_answer, i = get_question(step) #here to change index
    print(f"This is round {step + 1}. The sum is {STEPS[step]}")
    print(f"This is your question: \n{random_question}")
    answers = prepare_answers(random_answers)
    display_answers(answers)
    user_guess = user_input(answers)
    user_result = check_answer(user_guess, correct_answer, step)
    user_status = get_result(user_result, random_question, random_answers, correct_answer, i, step)
    with open('results.txt', 'a', encoding = 'utf8') as results:
        results.write('The result is ' + str(user_status) + '\n')
        results.write('The time is ' + str(datetime.datetime.now()) + '\n')
    return fg.red + str(user_status) + fg.rs

def initiation():
    print('---The rules of the game are simple!--- \nYou have to answer 4 questions. \nYou have 2 more efforts if your answer is wrong.\nYou can finish the game and grab your money by enter "Q". \n---Good luck, samurai. We have game to play!---')
    print('   ')

initiation()    
print(next_question())