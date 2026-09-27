from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Zentex-AI Web Response Logic
def process_zentex_input(cmd):
    cmd = cmd.strip().lower()
    if cmd == "status":
        return "SYSTEM OK: Zentex-AI running at peak efficiency in the cloud."
    elif cmd == "diagnostics":
        return "DIAGNOSTICS: Cloud nodes nominal. Core links stable."
    elif cmd == "help":
        return "AVAILABLE COMMANDS: status, diagnostics, build, clear"
    elif cmd == "build":
        return "BUILD PROTOCOL: Ready for hardware script generation or code debugging."
    else:
        return f"Zentex-AI processed input: '{cmd}'."

# Simple HTML user interface rendered directly
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zentex-AI Interface</title>
    <style>
        body { background-color: #0f172a; color: #38bdf8; font-family: monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .terminal { background: #1e293b; padding: 20px; border-radius: 8px; width: 400px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); border: 1px solid #334155; }
        h2 { margin-top: 0; color: #f8fafc; font-size: 1.2rem; border-bottom: 1px solid #334155; padding-bottom: 10px; }
        .output { height: 200px; overflow-y: auto; background: #090d16; padding: 10px; border-radius: 4px; margin-bottom: 15px; font-size: 0.9rem; border: 1px solid #1e293b; }
        .input-box { display: flex; gap: 10px; }
        input { flex: 1; background: #0f172a; border: 1px solid #475569; color: #f8fafc; padding: 8px; border-radius: 4px; font-family: monospace; }
        button { background: #0284c7; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; font-family: monospace; }
        button:hover { background: #0369a1; }
    </style>
</head>
<body>
    <div class="terminal">
        <h2>ZENTEX-AI // CORE v2.0</h2>
        <div class="output" id="outputWindow">SYSTEM INITIALIZED. Type 'help' for options.<br><br></div>
        <div class="input-box">
            <input type="text" id="userInput" placeholder="Enter command..." autofocus>
            <button onclick="sendQuery()">Send</button>
        </div>
    </div>
    <script>
        const inputField = document.getElementById("userInput");
        const outputWindow = document.getElementById("outputWindow");

        inputField.addEventListener("keypress", function(event) {
            if (event.key === "Enter") sendQuery();
        });

        async function sendQuery() {
            let text = inputField.value.trim();
            if(!text) return;
            outputWindow.innerHTML += `> ${text}<br>`;
            inputField.value = "";
            
            let response = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text})
            });
            let data = await response.json();
            outputWindow.innerHTML += `${data.reply}<br><br>`;
            outputWindow.scrollTop = outputWindow.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    reply = process_zentex_input(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)