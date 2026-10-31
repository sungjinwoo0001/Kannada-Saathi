
import gradio as gr  # pyright: ignore[reportMissingImports]
import asyncio
import edge_tts
import os
import uuid


# ---------------- MISSIONS ----------------

MISSIONS = {
    "Bus Mission": [
        {
            "question": "Where do you want to go?",
            "kannada": "ನನಗೆ ಮೈಸೂರು ರಸ್ತೆ ಬೇಕು.",
            "pronunciation": "Nanage Mysore Road beku.",
            "choices": [
                "ನನಗೆ ಮೈಸೂರು ರಸ್ತೆ ಬೇಕು.",
                "ನನಗೆ ಸಹಾಯ ಮಾಡಿ.",
                "ಧನ್ಯವಾದಗಳು."
            ],
            "correct": 0,
            "meaning": "I want Mysore Road."
        },
        {
            "question": "Do you need a ticket?",
            "kannada": "ಹೌದು, ಒಂದು ಟಿಕೆಟ್ ಕೊಡಿ.",
            "pronunciation": "Haudu, ondu ticket kodi.",
            "choices": [
                "ಹೌದು, ಒಂದು ಟಿಕೆಟ್ ಕೊಡಿ.",
                "ನನಗೆ ದಾರಿ ತೋರಿಸಿ.",
                "ನನಗೆ ನೀರು ಬೇಕು."
            ],
            "correct": 0,
            "meaning": "Yes, please give me one ticket."
        },
        {
            "question": "Where should I get off?",
            "kannada": "ನಾನು ಎಲ್ಲಿ ಇಳಿಯಬೇಕು?",
            "pronunciation": "Naanu elli iliyabeku?",
            "choices": [
                "ನಾನು ಎಲ್ಲಿ ಇಳಿಯಬೇಕು?",
                "ಇದರ ಬೆಲೆ ಎಷ್ಟು?",
                "ನನಗೆ ವೈದ್ಯರು ಬೇಕು."
            ],
            "correct": 0,
            "meaning": "Where should I get off?"
        }
    ],

    "Shopping Mission": [
        {
            "question": "Ask the shopkeeper the price.",
            "kannada": "ಇದು ಎಷ್ಟು?",
            "pronunciation": "Idu eshtu?",
            "choices": [
                "ಇದು ಎಷ್ಟು?",
                "ನಾನು ಎಲ್ಲಿ ಇಳಿಯಬೇಕು?",
                "ನನಗೆ ವೈದ್ಯರು ಬೇಕು."
            ],
            "correct": 0,
            "meaning": "How much is this?"
        },
        {
            "question": "Buy a bottle of water.",
            "kannada": "ಒಂದು ನೀರಿನ ಬಾಟಲಿ ಕೊಡಿ.",
            "pronunciation": "Ondu neerina bottle kodi.",
            "choices": [
                "ನನಗೆ ದಾರಿ ತೋರಿಸಿ.",
                "ಒಂದು ನೀರಿನ ಬಾಟಲಿ ಕೊಡಿ.",
                "ನನಗೆ ಟಿಕೆಟ್ ಬೇಕು."
            ],
            "correct": 1,
            "meaning": "Please give me one bottle of water."
        },
        {
            "question": "Thank the shopkeeper.",
            "kannada": "ಧನ್ಯವಾದಗಳು.",
            "pronunciation": "Dhanyavaadagalu.",
            "choices": [
                "ಇದು ಎಷ್ಟು?",
                "ನನಗೆ ನೀರು ಬೇಕು.",
                "ಧನ್ಯವಾದಗಳು."
            ],
            "correct": 2,
            "meaning": "Thank you."
        }
    ],

    "Directions Mission": [
        {
            "question": "Ask someone where the bus stand is.",
            "kannada": "ಬಸ್ ನಿಲ್ದಾಣ ಎಲ್ಲಿದೆ?",
            "pronunciation": "Bus nildaana ellide?",
            "choices": [
                "ಬಸ್ ನಿಲ್ದಾಣ ಎಲ್ಲಿದೆ?",
                "ಇದು ಎಷ್ಟು?",
                "ನನಗೆ ಊಟ ಬೇಕು."
            ],
            "correct": 0,
            "meaning": "Where is the bus stand?"
        },
        {
            "question": "Tell someone to go straight.",
            "kannada": "ನೇರವಾಗಿ ಹೋಗಿ.",
            "pronunciation": "Neravaagi hogi.",
            "choices": [
                "ಎಡಕ್ಕೆ ತಿರುಗಿ.",
                "ನೇರವಾಗಿ ಹೋಗಿ.",
                "ಧನ್ಯವಾದಗಳು."
            ],
            "correct": 1,
            "meaning": "Go straight."
        },
        {
            "question": "Ask someone to turn left.",
            "kannada": "ಎಡಕ್ಕೆ ತಿರುಗಿ.",
            "pronunciation": "Edakke tirugi.",
            "choices": [
                "ಬಲಕ್ಕೆ ತಿರುಗಿ.",
                "ಇದು ಎಷ್ಟು?",
                "ಎಡಕ್ಕೆ ತಿರುಗಿ."
            ],
            "correct": 2,
            "meaning": "Turn left."
        }
    ]
}


# ---------------- AUDIO ----------------

def generate_audio(text):
    if not text or not text.strip():
        raise gr.Error("No Kannada phrase available.")

    output_file = os.path.abspath(
        f"kannada_audio_{uuid.uuid4().hex}.mp3"
    )

    async def create_audio():
        voice = edge_tts.Communicate(
            text,
            "kn-IN-SapnaNeural"
        )
        await voice.save(output_file)

    try:
        asyncio.run(create_audio())
        return output_file

    except Exception as exc:
        raise gr.Error(
            f"Audio generation failed: {exc}. Check your internet connection."
        )


# ---------------- START MISSION ----------------

def start_mission(mission_name):
    mission = MISSIONS[mission_name]
    first = mission[0]

    return (
        mission_name,
        0,
        0,
        False,
        f"Mission started: {mission_name}",
        first["question"],
        first["kannada"],
        first["pronunciation"],
        gr.update(choices=first["choices"], value=None),
        "Choose the best response.",
        gr.update(interactive=False),
        None
    )


# ---------------- CHECK ANSWER ----------------

def check_answer(choice, mission_name, step, score, answered):
    mission = MISSIONS[mission_name]

    if step >= len(mission):
        return score, answered, "Mission already completed.", gr.update(
            interactive=False
        )

    if answered:
        return (
            score,
            answered,
            "You already answered correctly. Click Next Question.",
            gr.update(interactive=True)
        )

    if choice is None:
        return (
            score,
            answered,
            "Choose an answer first.",
            gr.update(interactive=False)
        )

    current = mission[step]
    correct_choice = current["choices"][current["correct"]]

    if choice == correct_choice:
        score += 1
        answered = True

        feedback = (
            "✅ Correct!\n\n"
            f"Meaning: {current['meaning']}\n\n"
            "You can continue to the next question."
        )

        return score, answered, feedback, gr.update(interactive=True)

    feedback = (
        "❌ Not quite. Try again!\n\n"
        f"Hint: {current['meaning']}"
    )

    return score, False, feedback, gr.update(interactive=False)


# ---------------- NEXT QUESTION ----------------

def next_question(mission_name, step, score, answered):
    mission = MISSIONS[mission_name]

    if not answered:
        return (
            step,
            answered,
            "Answer correctly before moving forward.",
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            "Try again.",
            gr.update(interactive=False),
            None
        )

    step += 1

    if step >= len(mission):
        return (
            step,
            False,
            "🏆 Mission complete!",
            "Congratulations! You completed this mission.",
            "",
            "",
            gr.update(choices=[], value=None),
            f"## Final Score: {score}/{len(mission)}\n\nYou completed {mission_name}!",
            gr.update(interactive=False),
            None
        )

    current = mission[step]

    return (
        step,
        False,
        f"Question {step + 1} of {len(mission)}",
        current["question"],
        current["kannada"],
        current["pronunciation"],
        gr.update(choices=current["choices"], value=None),
        "Choose the best response.",
        gr.update(interactive=False),
        None
    )


# ---------------- USER INTERFACE ----------------

with gr.Blocks(title="Kannada Saathi", theme=gr.themes.Soft()) as app:

    gr.Markdown(
        """
        # ಕನ್ನಡ ಸಾಥಿ | Kannada Saathi

        ### Learn Kannada through real-life conversations.

        Practise useful Kannada phrases for everyday situations.
        Listen to pronunciation, answer questions and improve your skills.

        **Your Kannada journey starts here!**
        """
    )

    gr.Markdown("## Select Your Mission")

    mission_picker = gr.Dropdown(
        choices=list(MISSIONS.keys()),
        value="Bus Mission",
        label="Choose a real-life situation"
    )

    mission_state = gr.State("Bus Mission")
    step = gr.State(0)
    score = gr.State(0)
    answered = gr.State(False)

    status = gr.Markdown("Select a mission and press Start Mission.")

    progress = gr.Markdown("Progress: 0/3")

    question = gr.Textbox(
        label="Situation",
        interactive=False
    )

    kannada = gr.Textbox(
        label="Kannada Phrase",
        interactive=False
    )

    pronunciation = gr.Textbox(
        label="English Pronunciation",
        interactive=False
    )

    listen_btn = gr.Button("🔊 Listen to Kannada")

    audio_output = gr.Audio(
        label="Kannada Audio",
        autoplay=True
    )

    answer = gr.Radio(
        label="Choose your response",
        choices=[]
    )

    feedback = gr.Markdown()

    with gr.Row():
        start = gr.Button("Start Mission", variant="primary")
        check = gr.Button("Check Answer")
        next_btn = gr.Button(
            "Next Question",
            interactive=False
        )

    gr.Markdown(
        """
        ---
        **Kannada Saathi | Hackathon Project**

        Learn Kannada. Practise confidently. Connect with people.
        """
    )

    # Start event
    start.click(
        start_mission,
        inputs=[mission_picker],
        outputs=[
            mission_state,
            step,
            score,
            answered,
            status,
            question,
            kannada,
            pronunciation,
            answer,
            feedback,
            next_btn,
            audio_output
        ]
    ).then(
        lambda: "Progress: 0/3",
        outputs=[progress]
    )

    # Check answer event
    check.click(
        check_answer,
        inputs=[answer, mission_state, step, score, answered],
        outputs=[score, answered, feedback, next_btn]
    ).then(
        lambda s: f"Current score: {s}/3",
        inputs=[score],
        outputs=[progress]
    )

    # Next question event
    next_btn.click(
        next_question,
        inputs=[mission_state, step, score, answered],
        outputs=[
            step,
            answered,
            status,
            question,
            kannada,
            pronunciation,
            answer,
            feedback,
            next_btn,
            audio_output
        ]
    ).then(
        lambda s: f"Progress: {min(s + 1, 3)}/3",
        inputs=[step],
        outputs=[progress]
    )

    # Audio event
    listen_btn.click(
        generate_audio,
        inputs=[kannada],
        outputs=[audio_output]
    )



if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 10000))
    )
