import streamlit as st
from google import genai

# -------------------------------
# ページ設定
# -------------------------------
st.set_page_config(
    page_title="Mood-Based Cooking App",
    page_icon="🍳",
    layout="wide"
)

# -------------------------------
# カスタム CSS
# -------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    font-family: "Helvetica", sans-serif;
}

/* メインカード */
.main-card {
    background: white;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    margin-top: 20px;
}

/* 出力カード */
.recipe-box {
    background: #fff8ef;
    padding: 20px;
    border-radius: 14px;
    margin-top: 25px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
}

/* タイトル */
h1 {
    text-align: center;
    font-weight: 800;
    color: #333;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #777;
    font-size: 18px;
    margin-bottom: 20px;
}

/* ボタン */
.stButton > button {
    background: #ff8c42 !important;
    color: white !important;
    font-size: 18px !important;
    padding: 12px 22px !important;
    border-radius: 12px !important;
    border: none;
    box-shadow: 0 3px 10px rgba(0,0,0,0.15);
    transition: 0.2s;
}
.stButton > button:hover {
    background: #ff7a1a !important;
}

/* テキスト入力 */
.stTextInput > div > div > input {
    border-radius: 10px !important;
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# タイトル
# -------------------------------
st.title("🍳 Mood-Based Cooking App")
st.markdown(
    '<p class="subtitle">AI suggests the best recipe based on your mood, cuisine, and time</p>',
    unsafe_allow_html=True
)

# -------------------------------
# メインカード
# -------------------------------
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# APIキー
client = genai.Client(api_key=st.secrets["AIzaSyCm-rRT2Ekpy2uBeUQserHbEaEXUS4DGyg"])

# -------------------------------
# ユーザー入力
# -------------------------------
mood = st.text_input(
    "How are you feeling today?",
    placeholder="e.g. tired, energetic, relaxed"
)

genre = st.selectbox(
    "Cuisine type",
    ["Any", "Japanese", "Western", "Chinese"]
)

cooking_time = st.selectbox(
    "How much time do you have?",
    ["Any", "Within 10 minutes", "Within 20 minutes", "Within 30 minutes", "Within 45 minutes", "Within 1 hour"]
)

st.write("")

# -------------------------------
# 提案ボタン
# -------------------------------
if st.button("🍽 Get a recipe"):
    if not mood:
        st.error("Please enter your mood.")
    else:
        with st.spinner("The AI is thinking of a recipe..."):
            prompt = f"""
You are an English-speaking cooking assistant.

Today's mood: {mood}
Cuisine type: {genre}
Cooking time: {cooking_time}

Please suggest ONE dish that matches these conditions.

IMPORTANT:
- Answer EVERYTHING in English.
- Do NOT use Japanese.

【Output format】
■ Dish name
■ Ingredients (bullet points)
■ Instructions (numbered steps)
■ Why this dish matches the mood (short explanation)
            """

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                recipe_text = response.text if hasattr(response, "text") else None

                if recipe_text:
                    st.markdown(
                        f"<div class='recipe-box'>{recipe_text}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.error("No recipe was returned.")

            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("</div>", unsafe_allow_html=True)



