import requests
import json

fixer_key = '92eb6c649f02cd29b5541a797a70619b'
baseurl = 'http://data.fixer.io/api/latest'
params = {'access_key': fixer_key}
fixer_resp = requests.get(baseurl, params = params)


#url = "http://data.fixer.io/api/latest?access_key=53d609ad140b77fa8bfaa08e912e13d6"
#raw_data = urllib.request.urlopen(url).read()
#parsed_data = json.loads(raw_data)



data = fixer_resp.json()
if not data['success']:
    exit('No data!')
print('Welcome to our service! Today is ', data['date'])
rates = data['rates']

while True:
    while True:
        user_input = input('Enter the currency code <from EUR to>: ')
        if user_input in rates:
            print('The rate now is ' + str(rates[user_input]))
            break
        else:
            print('We do not have this currency for you!')
            break

    eur = float(input('Enter the sum in EUR: '))
    result = eur * float(rates[user_input])
    print('Your exchange is ' + str(result))
    print('Do you want to calculate another one?')
    another_one = input('<Y>, <N>: ')
    if another_one == 'Y':
        continue
    elif another_one == 'N':
        print('Goodbye!')
        break 