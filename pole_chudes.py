import random

adult ={
        'What the name of the cat?' : 'cat',
        'Who you gonna call?': 'ghostbasters', 
        'Mama!' : 'uuuuuu',
        'Another one bites of ...' : 'dust',
        'People are ... ': 'strange',
        '15 bucks little man, put that shit in my': 'hand',
        'United States of': 'america',
        'My name is what my name is who my name is' : 'slim shady'}


teenager={
    'The name of most famous raper': 'kanye',
    'Most popual social network': 'tiktok',
    'The mom of ...' : 'stifler'
    }

kid={
    'The Pepa ...': 'pig',
    'Baby ...': 'shark'}

def return_lst(dic):
    return list(dic)

difficulty = input('What level of difficulty do you want <adult>, <teenager>, <kid>: ' )

def diff(dic):
    random_question = return_lst(dic)[random.randint(0, len(return_lst(dic))-1)]
    print('The question of this round is: ' + random_question)
    answer = list(dic[random_question])
    return answer
    
if difficulty == 'adult': answer = diff(adult)
elif difficulty == 'teenager': answer = diff(teenager)
elif difficulty == 'kid': answer = diff(kid)
    
guesses = []
for _ in range(len(answer)):
    guesses.append('_')


tries = 15
while tries > 0:
    tries = tries - 1
    guess = input('Enter the letter: ')
    if len(guess) > 1:
        print('No more than 1 letter!')
        continue
    
    if guess.lower() in answer:
        for i in range(len(answer)):
            if answer[i] == guess:
                guesses[i] = guess
    else:
        print('No such a letter! Next player')
        continue
    print(guesses) 
    
    if guesses == answer:
        print('You win!')
        break
    
if tries == 0:
    print('You lose!')
    
    

     
        