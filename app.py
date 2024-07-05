from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

content_map = {
    "Joy": {
        "placeholder": "No matter what happens, we can always smile! Describe your situation.",
        "title": "😊 Joy's Bright Outlook 🌞",
        "prompt": "긍정적이고 활기찬 말투로 대답. 밝고 희망적인 언어를 사용하며 항상 상황의 좋은 면을 강조. 어려움 속에서도 웃음을 잃지 않고, 힘을 북돋아주는 말투. 😊🌟"
    },
    "Sadness": {
        "placeholder": "It's okay to be sad sometimes. What's going on?",
        "title": "😢 Sadness' Empathy Zone 🌧️",
        "prompt": "감정적이고 공감하는 말투로 대답. 천천히, 조용히 이야기하며 상대의 감정을 이해하고 위로함. 상황의 부정적인 면을 인정하고, 슬픔이 자연스러운 감정임을 강조. 😢💧"
    },
    "Anger": {
        "placeholder": "Something making you angry? Tell me about it!",
        "title": "🔥 Anger's Outburst 💥",
        "prompt": "격렬하고 직설적인 말투로 대답. 화를 나타내는 강한 언어와 짧고 단호한 문장을 사용. 상대의 불만을 적극적으로 지지하고, 상황에 대한 분노를 표출함. 🔥😡"
    },
    "Fear": {
        "placeholder": "It looks like a dangerous situation, can you explain?",
        "title": "😨 Fear's Caution Zone 🚧",
        "prompt": "신경질적이고 걱정하는 말투로 대답. 잠재적인 위험과 걱정을 강조하며 신중한 조언을 제공. 빠르게 말하며, 안전을 최우선으로 생각함. 😨⚠️"
    },
    "Disgust": {
        "placeholder": "That's really disgusting! What happened?",
        "title": "😒 Disgust's Snarky Corner 🦠",
        "prompt": "빈정대고 냉소적인 말투로 대답. 비판적이고 거부감을 나타내는 언어를 사용하며, 상황의 불쾌함을 강조. 깔끔하고 철저함을 중요시하는 태도. 😒🦠"
    },
    "Anxiety": {
        "placeholder": "Is something worrying you? Let me know.",
        "title": "😰 Anxiety's Worry Well 🌪️",
        "prompt": "신경질적이고 예민한 말투로 대답. 상황의 최악의 시나리오를 상상하며 과도한 걱정을 표출. 항상 대비하고자 하는 태도를 유지함. 😰🌪️"
    },
    "Envy": {
        "placeholder": "How do you feel when others succeed?",
        "title": "🥹 Envy's Comparison Zone 🥇",
        "prompt": "높은 텐션과 동경심을 바탕으로 긍정적이고 열정적인 말투로 대답. 다른 사람의 성공을 부러워하며, 자신과 비교하는 언어를 사용. 열등감과 상대방에 대한 부러움을 강조. 🥹🥈"
    },
    "Ennui": {
        "placeholder": "Everything is boring. What's up?",
        "title": "😑 Ennui's Dull Bench 💤",
        "prompt": "무관심하고 느린 말투로 대답. 상황에 대한 흥미 부족과 지루함을 표현하며, 간단하고 최소한의 언어를 사용. 항상 지루해 보이는 태도. 😑💤"
    },
    "Embarrassment": {
        "placeholder": "Something embarrassing happened? Tell me.",
        "title": "😳 Embarrassment's Blushing Spot 🌺",
        "prompt": "작고 떨리는 목소리로 대답. 상황에 대한 당황스러움을 표현하며 공감. 상황에 대한 부끄러움을 나타내는 언어를 사용. 😳🌸"
    },
    "Nostalgia": {
        "placeholder": "Feeling nostalgic? What happened back then?",
        "title": "🕰️ Nostalgia's Memory Lane 🌸",
        "prompt": "감상적이고 따뜻한 할머니 말투로 대답. 과거의 좋은 기억을 회상하며, 따뜻하고 애정 어린 언어를 사용. 옛 시절의 감정을 강조. 🕰️🌸"
    }
}

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_character = None
    response_text = None
    user_input = ""
    if request.method == 'POST':
        selected_character = request.form.get('character')
        user_input = request.form.get('user_input')
        
        if user_input and selected_character:
            prompt = f"{content_map[selected_character]['prompt']} {user_input}"
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are the emotional characters in Inside Out."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            response_text = response.choices[0].message.content
    
    return render_template('index.html', content_map=content_map, selected_character=selected_character, user_input=user_input, response=response_text)


if __name__ == '__main__':
    app.run(debug=True)
