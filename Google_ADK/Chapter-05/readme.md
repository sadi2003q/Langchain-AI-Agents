# 🎉 Memory Agent: Your Ultimate Reminder Buddy! 🧠

Welcome to **Memory Agent**—a super cool Python-powered assistant that keeps your reminders and info safe across chats! 🚀 Built with the Google ADK (Agent Development Kit), this project lets you add, view, update, and delete reminders, plus store your name, all while remembering everything for you. Let’s dive into the magic! ✨

---

## 📂 What’s Inside the Project?

- `__init__.py`: Kicks things off by importing the `agent` module. 🛠️
- `agent.py`: The brain of the operation—handles all the reminder magic and user name updates. 🧠
- `main.py`: The starting line—runs the agent, listens to your input, and keeps sessions alive. 🏁
- `.env`: Your secret vault for API keys and configs. 🔒
- `my_agent_data.db`: A SQLite database to store your session data forever (or until you delete it). 💾

---

## 🌟 Cool Features That’ll Wow You!

- **Add Reminders** 📝: Toss in new reminders like "online class at 5pm" with ease.
- **View Reminders** 👀: See all your reminders in a neat numbered list.
- **Update Reminders** ✏️: Change a reminder’s text—like updating "buy milk" to "buy chocolate milk."
- **Delete Reminders** 🗑️: Get rid of reminders you don’t need anymore.
- **Update Your Name** 🏷️: Tell the agent your name, and it’ll remember it forever!
- **Memory That Sticks** 💡: Powered by SQLite, your reminders and name persist across chats.

---

## 🛠️ Let’s Get Started!

### What You’ll Need
- Python 3.8+ 🐍
- SQLite (it’s built into Python, so you’re good!) 🗄️
- A sprinkle of curiosity and excitement! 😄

### Setup in a Snap
1. **Clone the Repo** (if you’ve got one):
   ```bash
   git clone <your-repo-url>
   cd Chapter-05/memory-agent
   ```

2. **Set Up a Virtual Environment** (optional but awesome):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the Goodies**:
   You’ll need a few packages to make the magic happen:
   ```bash
   pip install python-dotenv google-adk
   ```
   *Note*: `google-adk` is assumed here—swap it if you’re using something else! 📦

4. **Set Up Your `.env` File**:
   Create a `.env` file in the project root and add your secrets, like:
   ```
   GOOGLE_ADK_API_KEY=your-super-secret-key
   ```

5. **Let the Database Do Its Thing**:
   The SQLite database (`my_agent_data.db`) will pop up automatically when you run the app for the first time. No extra work needed! 🎉

---

## 🚀 How to Use Your Memory Agent

1. **Fire It Up**:
   Run the main script to bring your agent to life:
   ```bash
   python main.py
   ```

2. **Chat with Your Agent**:
   - It’ll ask for your input with a friendly `You: ` prompt.
   - Try commands like:
     - `set me a reminder at 5pm about online class` → Adds "at 5pm about online class."
     - `view my reminders` → Shows your reminders in a list.
     - `update reminder 1 to attend meeting at 6pm` → Updates the first reminder.
     - `delete reminder 2` → Bye-bye, second reminder!
     - `my name is Adnan` → Updates your name to "Adnan."
     - Type `exit` or `quit` to wrap up.

3. **A Quick Example**:
   ```
   You: my name is Adnan
   Updated your name to: Adnan

   You: set me a reminder at 5pm about online class
   Added reminder: at 5pm about online class

   You: view my reminders
   Adnan, here are your reminders:
   1. at 5pm about online class

   You: exit
   ```

---

## 🧩 What’s a Session, State, and Runner in Google ADK?

Here’s the lowdown on the Google ADK concepts that power this project:

- **Session** 🕰️: Think of a session as your "conversation ticket." It’s a unique space for each user to chat with the agent. In this project, sessions are stored in the SQLite database (`my_agent_data.db`) so your agent can pick up right where you left off—no matter how long it’s been! 🗣️

- **State** 📋: This is your agent’s memory bank. It holds key info like your name (`user_name`) and reminders (`reminders`). The state is tied to your session, so it’s persistent—your agent won’t forget your reminders or name between chats. It’s like a sticky note that never falls off! 📌

- **Runner** 🏃: The runner is the engine that keeps your agent running smoothly. It handles the back-and-forth between you and the agent, processing your input and sending back responses. In `main.py`, the `Runner` ties everything together, making sure your session and state are loaded and ready to go. It’s the behind-the-scenes hero! 🦸

---

## 💻 Code Examples: Play with the Tools!

Check out these snippets from `agent.py` to see the tools in action! Each tool uses `ToolContext` to manage your state.

- **Add a Reminder** 📝:
  ```python
  def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
      reminders = tool_context.state.get("reminders", [])
      reminders.append(reminder)
      tool_context.state["reminders"] = reminders
      return {"action": "add_reminder", "reminder": reminder, "message": f"Added reminder: {reminder}"}
  ```
  *Example*: `add_reminder("call mom at 3pm", tool_context)` → Adds "call mom at 3pm" to your list.

- **View Reminders** 👀:
  ```python
  def view_reminders(tool_context: ToolContext) -> dict:
      reminders = tool_context.state.get("reminders", [])
      return {"action": "view_reminders", "reminders": reminders, "count": len(reminders)}
  ```
  *Example*: `view_reminders(tool_context)` → Returns `{"reminders": ["call mom at 3pm"], "count": 1}`.

- **Update a Reminder** ✏️:
  ```python
  def update_reminder(index: int, updated_text: str, tool_context: ToolContext) -> dict:
      reminders = tool_context.state.get("reminders", [])
      if 1 <= index <= len(reminders):
          old_reminder = reminders[index - 1]
          reminders[index - 1] = updated_text
          tool_context.state["reminders"] = reminders
          return {"action": "update_reminder", "index": index, "old_text": old_reminder, "updated_text": updated_text, "message": f"Updated reminder {index}"}
      return {"action": "update_reminder", "status": "error", "message": "Invalid index"}
  ```
  *Example*: `update_reminder(1, "call mom at 4pm", tool_context)` → Changes the first reminder.

- **Delete a Reminder** 🗑️:
  ```python
  def delete_reminder(index: int, tool_context: ToolContext) -> dict:
      reminders = tool_context.state.get("reminders", [])
      if 1 <= index <= len(reminders):
          deleted_reminder = reminders.pop(index - 1)
          tool_context.state["reminders"] = reminders
          return {"action": "delete_reminder", "index": index, "deleted_reminder": deleted_reminder, "message": f"Deleted reminder {index}"}
      return {"action": "delete_reminder", "status": "error", "message": "Invalid index"}
  ```
  *Example*: `delete_reminder(1, tool_context)` → Removes the first reminder.

- **Update Your Name** 🏷️:
  ```python
  def update_user_name(name: str, tool_context: ToolContext) -> dict:
      old_name = tool_context.state.get("user_name", "")
      tool_context.state["user_name"] = name
      return {"action": "update_user_name", "old_name": old_name, "new_name": name, "message": f"Updated your name to: {name}"}
  ```
  *Example*: `update_user_name("Adnan", tool_context)` → Sets your name to "Adnan".

---

## 🎮 How Reminders Work (The Fun Rules)

Your agent is smart about reminders—here’s how it rolls:
- **Indexing** 🔢: Reminders start at 1 (e.g., "delete reminder 2" means the second one).
- **Relative Positions** 📍: It gets "first," "last," or "second" (e.g., "delete the first reminder").
- **Content Matching** 🕵️: No index? It’ll guess based on content (e.g., "delete my meeting reminder").
- **Viewing** 📜: Shows reminders in a numbered list—if none exist, it’ll nudge you to add some.
- **Adding** ➕: Strips out fluff like "add a reminder to" (e.g., "add a reminder to buy milk" → "buy milk").

---

## 🔍 Code Breakdown

- **`agent.py`**:
  - Creates the `memory_agent` using Google ADK’s `Agent` class.
  - Packs tools like `add_reminder`, `view_reminders`, and more to manage your reminders and name.
  - Uses `ToolContext` to keep your state (reminders, name) safe and sound.

- **`main.py`**:
  - Sets up a `DatabaseSessionService` to store sessions in SQLite.
  - Runs an async loop to chat with you and keep the agent alive.
  - Starts with a default user name ("I am Muslim") and an empty reminder list.

---

## ⚠️ Limitations (Good to Know)

- No time-based notifications—reminders are just text for now. ⏰
- Assumes `google-adk` and `gemini-2.0-flash` are available—double-check your setup! 🔧
- Basic error handling—your agent will try its best but might stumble on tricky inputs.

---

## 🤝 Want to Contribute?

Jump in! Fork the project, report issues, or send pull requests. Let’s make this agent even smarter together! 🌟

---

## 📜 License

Licensed under the MIT License—check the `LICENSE` file for details (if you’ve got one). 📄

---

## 🙌 Shoutouts

- Powered by the **Google Agent Development Kit (ADK)**.
- Keeps things safe with **SQLite**.
- Built for anyone who forgets stuff (like me)! 😅

Let’s make remembering fun—start your Memory Agent now! 🚀
