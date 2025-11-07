## CoAura — NASA's SOS Response Agent

An interactive space station emergency simulation game built with Gradio. Play as a Commander responding to critical system failures or play a fun trivia game with our own CoAura with the help of CoAura NASA's SOS Response Agent chatbot. The UI runs in your browser with a simple chat-like interface and multiple-choice decisions.


### Quick start (Windows / PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Upgrade pip and install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python main.py
```

After launching, Gradio will print a local URL (for example http://127.0.0.1:7860) — open it in your browser to play.

- **Visual system**: The code includes `img_state` values (1-7) ready for adding spacecraft visuals:
  - `1` = Normal/stable
  - `2` = Oxygen issue (gas leaking)
  - `3` = Cooling issue (freezing)
  - `4` = Power issue (battery malfunction)
  - `5` = System recovering (bandage on spacecraft)
  - `6` = Stable state
  - `7` = Critical failure (spacecraft imploding)

### License

This repository includes a `LICENSE` file — see it for license details.

---
https://docs.google.com/presentation/d/1L2-AftcGhO7MEDxqE9Z8Z3PKgertAWzI7fQjVZP8vUs/edit?usp=sharing
