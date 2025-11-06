import gradio as gr
import random
import time
import os

# --- Game State ---
phase = "mode_select"
img_state = 1
completed_components = []
mode = None  # Track which mode the user selected

# --- Image Helper ---
def get_image_path(state):
    return os.path.join("images", f"{state}.png")

# --- Game Logic ---
def reset_game():
    """Resets the game to its initial state."""
    global phase, img_state, completed_components, mode
    phase = "mode_select"
    img_state = 1
    completed_components = []
    mode = None
    intro = [{"role": "assistant", "content": "Hello, Commander. I'm CoAura, your AI assistant. How can I help you today?"}]
    return intro, gr.update(choices=["Emergency Simulation Mode", "Space Chat Mode"], value=None), get_image_path(img_state)

def progress(choice, chat):
    """Main function to handle game progress and UI updates."""
    global phase, img_state, completed_components, mode

    if not choice:
        chat.append({"role": "assistant", "content": "Commander, I need your input to proceed. Please select an option."})
        # CRITICAL CHANGE: The function must always return a value for the image component
        return chat, gr.update(), get_image_path(img_state)

    chat.append({"role": "user", "content": choice})
    time.sleep(random.uniform(0.5, 1.0))

    # --- MODE SELECTION ---
    if phase == "mode_select":
        if choice == "Emergency Simulation Mode":
            mode = "emergency"
            phase = "start"
            reply = "Emergency mode activated. Commander, I'm detecting anomalies in the station systems. We need to address this immediately. Shall I run a full diagnostic scan?"
            options = ["Run a system scan", "Ignore for now"]
        elif choice == "Space Chat Mode":
            mode = "chat"
            phase = "space_chat"
            reply = "Great! I'm here to talk about anything space-related. What would you like to discuss?"
            options = ["Tell me about the International Space Station", "What's it like being an astronaut?", "Explain how rockets work", "Back to Emergency Mode"]
        else:
            reply = "Please select a mode to continue."
            options = ["Emergency Simulation Mode", "Space Chat Mode"]
    
    # --- SPACE CHAT MODE ---
    elif phase == "space_chat":
        if choice == "Tell me about the International Space Station":
            reply = "The International Space Station (ISS) is a marvel of human engineering! It orbits Earth at about 400 km altitude, traveling at 28,000 km/h. It's been continuously inhabited since 2000 and serves as a microgravity research laboratory. The station is about the size of a football field and requires constant maintenance. What else would you like to know?"
            options = ["What's it like being an astronaut?", "Explain how rockets work", "Tell me about space food", "Back to Emergency Mode"]
        elif choice == "What's it like being an astronaut?":
            reply = "Being an astronaut is incredible but challenging! You experience weightlessness, see 16 sunrises and sunsets daily, and witness Earth from a unique perspective. However, you must exercise 2 hours daily to prevent muscle loss, adapt to sleeping while floating, and learn to eat carefully so food doesn't float away. The camaraderie with your crew is essential. Interested in another topic?"
            options = ["Tell me about the International Space Station", "Explain how rockets work", "What about spacewalks?", "Back to Emergency Mode"]
        elif choice == "Explain how rockets work":
            reply = "Rockets work on Newton's third law: for every action, there's an equal and opposite reaction! They burn fuel (like liquid hydrogen and oxygen) in a combustion chamber, creating hot expanding gases. These gases shoot out the bottom nozzle at extreme speeds, pushing the rocket upward. Modern rockets have multiple stages that detach as fuel is used to reduce weight. Fascinating, right?"
            options = ["Tell me about the International Space Station", "What's it like being an astronaut?", "Tell me about Mars missions", "Back to Emergency Mode"]
        elif choice == "Tell me about space food":
            reply = "Space food has come a long way! Early astronauts ate from tubes, but now they enjoy freeze-dried meals, thermostabilized pouches, and even fresh fruit on resupply missions. Everything must be carefully packaged to prevent crumbs (which could damage equipment) and must have a long shelf life. Some foods like salt and pepper come in liquid form to prevent floating particles. What else interests you?"
            options = ["What about spacewalks?", "Tell me about Mars missions", "How do astronauts exercise in space?", "Back to Emergency Mode"]
        elif choice == "What about spacewalks?":
            reply = "Spacewalks (EVAs) are some of the most challenging activities! Astronauts wear 300-pound spacesuits with their own life support systems. They're tethered to the station for safety and can work for 6-8 hours. The suits protect against temperature extremes (-250°F to +250°F), micrometeoroids, and radiation. Training for spacewalks takes months in underwater pools. Anything else?"
            options = ["Tell me about space food", "How do astronauts exercise in space?", "Tell me about Mars missions", "Back to Emergency Mode"]
        elif choice == "Tell me about Mars missions":
            reply = "Mars exploration is humanity's next giant leap! A trip to Mars takes 6-9 months one way. Challenges include radiation exposure, psychological effects of isolation, growing food in Martian soil, and creating breathable air from the CO2 atmosphere. NASA's Perseverance rover is currently exploring Mars, searching for signs of ancient life. The goal is to send humans by the 2030s. Exciting times!"
            options = ["What's it like being an astronaut?", "Explain how rockets work", "What about spacewalks?", "Back to Emergency Mode"]
        elif choice == "How do astronauts exercise in space?":
            reply = "Exercise is crucial in space! Without gravity, muscles and bones weaken rapidly. Astronauts use special equipment: a treadmill with harnesses to simulate running, a stationary bike, and a resistance exercise device (like weightlifting). They exercise 2 hours daily, 6 days a week. Some astronauts even run marathons in space! What else would you like to explore?"
            options = ["Tell me about the International Space Station", "What about spacewalks?", "Tell me about Mars missions", "Back to Emergency Mode"]
        elif choice == "Back to Emergency Mode":
            mode = "emergency"
            phase = "start"
            reply = "Switching to Emergency Simulation Mode. Commander, I'm detecting anomalies in the station systems. We need to address this immediately. Shall I run a full diagnostic scan?"
            options = ["Run a system scan", "Ignore for now"]
        else:
            reply = "That's an interesting question! What else would you like to know about space?"
            options = ["Tell me about the International Space Station", "What's it like being an astronaut?", "Explain how rockets work", "Back to Emergency Mode"]

    # --- rest of the game logic remains the same here ---
    elif phase == "start":
        if choice == "Run a system scan":
            available = [c for c in ["O2", "Cooling", "Power"] if c not in completed_components]
            if not available:
                reply = "Excellent work, Commander! All critical systems are now functioning normally. The station is secure. Would you like to run another simulation?"
                options, phase = ["Restart"], "end"
            else:
                component = random.choice(available)
                if component == "O2":
                    img_state = 2
                    reply = "Commander, I've identified a critical oxygen system failure. Life support is compromised. I'm showing you two repair protocols — which approach do you want me to guide you through?"
                    options = ["Attempt manual valve adjustment", "Reroute backup oxygen supply"]
                    phase = "o2_choice1"
                elif component == "Cooling":
                    img_state = 3
                    reply = "Commander, the thermal management system is overheating. We're approaching dangerous temperature levels. I have two stabilization procedures available — which one should we try?"
                    options = ["Increase coolant flow rate", "Switch to backup cooling loop"]
                    phase = "cooling_choice1"
                else:
                    img_state = 4
                    reply = "Commander, we have a power grid instability. Multiple systems are at risk. I can guide you through two emergency protocols — which would you prefer?"
                    options = ["Stabilize main voltage regulator", "Reroute to auxiliary power"]
                    phase = "power_choice1"
        elif choice == "Ignore for now":
            reply = "Commander, I must advise against ignoring this. The situation is deteriorating rapidly. We need to take action now. What's your decision?"
            options = ["Run a system scan", "Reboot subsystem"]
        elif choice == "Reboot subsystem":
            reply = "The reboot attempt didn't resolve the issue, Commander. The problem is more serious than anticipated. I recommend running a full diagnostic immediately."
            options = ["Run a system scan"]
        else:
            reply = "I didn't catch that, Commander. Could you clarify your instructions?"
            options = ["Run a system scan", "Ignore for now"]

    elif phase == "o2_choice1":
        reply = "Good choice, Commander. Now, I'm walking you through the procedure. Which specific action should I help you execute?"
        phase = "o2_choice2"
        options = ["Open emergency vent slowly", "Close primary intake valve"] if choice == "Attempt manual valve adjustment" else ["Activate redundant oxygen tank", "Purge main O2 line"]

    elif phase == "o2_choice2":
        if random.random() < 0.5:
            img_state = 5
            reply = f"Perfect execution, Commander! Your '{choice}' maneuver worked. Oxygen levels are returning to normal. Life support is stable."
            phase = "finish"
            options = ["Continue"]
            completed_components.append("O2")
        else:
            img_state = 7
            reply = f"Commander, no! The '{choice}' procedure caused a cascade failure. I'm detecting rapid decompression. We've lost life support. I'm sorry, Commander..."
            phase = "end"
            options = ["Restart"]

    elif phase == "cooling_choice1":
        reply = "Understood, Commander. I'm configuring that now. What's your next step?"
        phase = "cooling_choice2"
        options = ["Gradually raise pump pressure", "Flush coolant reservoir"] if choice == "Increase coolant flow rate" else ["Activate secondary radiators", "Divert heat to main radiator"]

    elif phase == "cooling_choice2":
        if random.random() < 0.5:
            img_state = 5
            reply = f"Excellent work, Commander! Your '{choice}' procedure was successful. Temperature readings are normalizing. The cooling system is back online."
            phase = "finish"
            options = ["Continue"]
            completed_components.append("Cooling")
        else:
            img_state = 7
            reply = f"Commander, we have a problem! The '{choice}' caused a thermal runaway. Critical systems are overheating. I'm losing control..."
            phase = "end"
            options = ["Restart"]

    elif phase == "power_choice1":
        reply = "On it, Commander. I'm preparing the power systems. Which final step should I execute?"
        phase = "power_choice2"
        options = ["Recalibrate voltage threshold", "Bypass surge protector"] if choice == "Stabilize main voltage regulator" else ["Switch to battery backup", "Isolate faulty circuit"]

    elif phase == "power_choice2":
        if random.random() < 0.5:
            img_state = 5
            reply = f"Outstanding, Commander! Your '{choice}' decision restored power stability. All systems are drawing clean energy. Grid is secure."
            phase = "finish"
            options = ["Continue"]
            completed_components.append("Power")
        else:
            img_state = 7
            reply = f"Commander, abort! The '{choice}' triggered a massive surge. I'm losing power to all— [CONNECTION LOST]"
            phase = "end"
            options = ["Restart"]

    elif phase == "finish":
        remaining = len([c for c in ["O2", "Cooling", "Power"] if c not in completed_components])
        if remaining > 0:
            reply = "Great work, Commander! That system is stable now. But... hold on, I'm detecting another critical alert. We need to move fast. Running diagnostics..."
            phase = "start"
            options = ["Run a system scan"]
        else:
            reply = "Excellent work, Commander! All critical systems are now functioning normally. The station is secure. Would you like to run another simulation?"
            phase = "end"
            options = ["Restart"]

    elif phase == "end":
        if "restart" in choice.lower():
            # CRITICAL CHANGE: The reset function now returns 3 values
            return reset_game()
        reply = "I'm standing by, Commander. Ready to assist when you need me."
        options = ["Restart"]

    chat.append({"role": "assistant", "content": reply})
    # CRITICAL CHANGE: Notice it now returns the image path at the end
    return chat, gr.update(choices=options, value=options[0] if options else None), get_image_path(img_state)


# --- UI Layout ---
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("##  CoAura — NASA's SOS Response Agent")
    
    # THIS IS THE NEW LAYOUT CODE
    with gr.Row():
        with gr.Column(scale=1):
            # This is the new Image component on the left
            img = gr.Image(value=get_image_path(img_state), label="Spaceship Status", show_label=True, interactive=False)
        with gr.Column(scale=2):
            # This is your chat interface on the right
            chat = gr.Chatbot(type="messages", height=550)
            picks = gr.Radio([], label="Select an option")
            btn = gr.Button("Continue")

    # --- Event Handling ---
    # CRITICAL CHANGE: The 'outputs' list for the functions now includes the 'img' component
    app.load(reset_game, [], [chat, picks, img])
    btn.click(progress, [picks, chat], [chat, picks, img])

app.launch()
