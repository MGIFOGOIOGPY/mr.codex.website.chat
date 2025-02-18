from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# قالب HTML
html_template = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CODEX TEAM WEBSIT CHAT</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1e1e2f;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .chat-container {
            width: 80%;
            max-width: 600px;
            background-color: #28293d;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }
        h1 {
            text-align: center;
            color: #00bcd4;
        }
        #chat-box {
            height: 300px;
            overflow-y: auto;
            background-color: #33334d;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .message {
            padding: 5px;
            margin: 5px 0;
            border-bottom: 1px solid #444;
        }
        #message-input {
            width: calc(100% - 80px);
            padding: 10px;
            border-radius: 5px;
            border: none;
            outline: none;
        }
        #send-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #00bcd4;
            color: #ffffff;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>CODEX TEAM WEBSIT CHAT</h1>
        <div id="chat-box"></div>
        <input type="text" id="message-input" placeholder="دخل رسالة هون يل قلاوي🙂" />
        <button id="send-btn">إرسال</button>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        var socket = io();
        var chatBox = document.getElementById("chat-box");
        var messageInput = document.getElementById("message-input");
        var sendBtn = document.getElementById("send-btn");

        sendBtn.addEventListener("click", function() {
            var message = messageInput.value;
            if (message.trim() !== "") {
                socket.send(message);
                messageInput.value = "";
            }
        });

        socket.on("message", function(msg) {
            var messageElement = document.createElement("div");
            messageElement.className = "message";
            messageElement.textContent = msg;
            chatBox.appendChild(messageElement);
            chatBox.scrollTop = chatBox.scrollHeight;
        });
    </script>
</body>
</html>
"""

# الصفحة الرئيسية
@app.route('/chat')
def index():
    return render_template_string(html_template)

# استقبال الرسائل وإرسالها لجميع المستخدمين
@socketio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
