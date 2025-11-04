import gradio as gr
import random

# simple globals (still learning state machines lol)
phase = "start"
system_health = 100

def reset_game():
    global phase, system_health
    phase = "start"
    system_health = 100

    first_message = [{
        "role": "assistant",
        "content": "CoAura systems online. Reactor anomaly confirmed. Standing by for mission input."
    }]
    
    options = ["Run diagnostics", "Ignore alert"]
    return first_message, gr.update(choices=options, value=None)

def progress(choice, history):
    global phase, system_health

    if not choice:
        history.append({"role":"assistant","content":"Command required. Awaiting your directive."})
        return history, gr.update()

    history.append({"role":"user","content":choice})

    # if reactor already dead before logic
    if system_health <= 0 and phase != "end":
        reply = "Containment failure detected. Simulation complete. Systems entering safe configuration."
        options = ["Restart Simulation"]
        phase = "end"
        history.append({"role":"assistant","content":reply})
        return history, gr.update(choices=options, value="Restart Simulation")

    # ==== GAME PHASES ====

    if phase == "start":
        if choice == "Run diagnostics":
            phase = "coolant"
            reply = "Diagnostics complete. Coolant integrity at 43 percent. Recommend immediate corrective action."
            options = ["Repair coolant system", "Reroute power"]
        elif choice == "Ignore alert":
            phase = "overheat"
            system_health -= 25
            reply = "Thermal spike detected. Core pressure rising. Action required."
            options = ["Emergency shutdown", "Contact control"]
        else:
            reply = "Input not recognized."
            options = []

    elif phase == "coolant":
        if choice == "Repair coolant system":
            if random.random() < 0.5:
                phase = "critical"
                system_health -= 40
                reply = "Repair unsuccessful. Pressure increasing beyond tolerance. Recommend immediate response."
                options = ["Retry repair", "Abort mission"]
            else:
                phase = "reroute"
                reply = "Coolant flow restored. Reactor stability improving. Proceed with secondary power routing."
                options = ["Proceed"]
        elif choice == "Reroute power":
            phase = "end"
            reply = "Power routing realigned. Reactor systems nominal. Mission objective achieved."
            options = ["Restart Simulation"]
        else:
            reply = "Unknown directive."
            options = []

    elif phase == "overheat":
        if choice == "Emergency shutdown":
            if random.random() < 0.3:
                system_health = 0
                reply = "Shutdown sequence interrupted. Containment compromised."
            else:
                phase = "end"
                system_health -= 10
                reply = "Shutdown successful. Thermal output decreasing. Containment stable."
            options = ["Restart Simulation"]
        elif choice == "Contact control":
            phase = "manual"
            system_health -= 20
            reply = "Primary communications offline. Initiating alternate control pathway."
            options = ["Manual override", "Shutdown reactor"]
        else:
            reply = "Invalid procedure."
            options = []

    elif phase == "critical":
        if choice == "Retry repair":
            if random.random() < 0.6:
                phase = "reroute"
                reply = "Repair confirmed. Reactor stabilizing."
                options = ["Proceed"]
            else:
                system_health = 0
                phase = "end"
                reply = "Repair failed. Containment breach confirmed."
                options = ["Restart Simulation"]
        elif choice == "Abort mission":
            system_health = 0
            phase = "end"
            reply = "Mission aborted per command. Reactor collapse confirmed."
            options = ["Restart Simulation"]
        else:
            reply = "Unable to interpret command."
            options = []

    elif phase == "manual":
        if choice == "Manual override":
            if random.random() < 0.7:
                reply = "Override accepted. Reactor stability restored."
            else:
                system_health = 0
                reply = "Override unsuccessful. Containment collapse in progress."
        else:
            system_health = 0
            reply = "Shutdown executed, but containment loss already underway."

        options = ["Restart Simulation"]
        phase = "end"

    elif phase == "reroute":
        reply = "Reactor stability confirmed. Mission accomplished. Thank you for maintaining operational integrity."
        options = ["Restart Simulation"]
        phase = "end"

    elif phase == "end":
        if "restart" in choice.lower():
            msgs, opts = reset_game()
            return msgs, opts

        reply = "Scenario concluded. Select to initiate a new simulation cycle."
        options = ["Restart Simulation"]

    history.append({"role":"assistant","content":reply})
    return history, gr.update(choices=options, value=options[0] if options else None)

# ==== UI ====
with gr.Blocks() as app:
    gr.Markdown("## 🛰️ CoAura — Mission Critical Simulation Console\n### Operate reactor systems in a controlled mission environment.")
    chat = gr.Chatbot(type="messages", height=350)
    picks = gr.Radio([], label="Select Action")
    btn = gr.Button("Execute")

    app.load(reset_game, [], [chat, picks])
    btn.click(progress, [picks, chat], [chat, picks])

app.launch()
