import streamlit as st
from google import genai
import urllib.parse

# -------------------------------
# ページ設定
# -------------------------------
st.set_page_config(
    page_title="Mood-Based Cooking App",
    page_icon="🍳",
    layout="wide"
)

# -------------------------------
# カスタムCSS
# -------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    font-family: "Helvetica", sans-serif;
}

.main-card {
    background: white;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    margin-top: 20px;
}

.recipe-box {
    background: #fff8ef;
    padding: 20px;
    border-radius: 14px;
    margin-top: 20px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
}

h1 {
    text-align: center;
    font-weight: 800;
    color: #333;
}

.subtitle {
    text-align: center;
    color: #777;
    font-size: 18px;
    margin-bottom: 20px;
}

.stButton > button {
    background: #ff8c42 !important;
    color: white !important;
    font-size: 18px !important;
    padding: 12px 22px !important;
    border-radius: 12px !important;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# タイトル
# -------------------------------
st.title("🍳 Mood-Based Cooking App")
st.markdown(
    '<p class="subtitle">AI suggests a recipe based on your mood, cuisine, and time</p>',
    unsafe_allow_html=True
)

# -------------------------------
# メインカード
# -------------------------------
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# -------------------------------
# Gemini API
# -------------------------------
client = genai.Client(api_key=st.secrets["api_key"])

# -------------------------------
# 入力欄
# -------------------------------
mood = st.text_input(
    "How are you feeling today?",
    placeholder="e.g. tired, energetic, relaxed"
)

genre = st.selectbox(
    "Cuisine",
    ["Any", "Japanese", "Western", "Chinese"]
)

cooking_time = st.selectbox(
    "Cooking time",
    ["Any", "Within 10 minutes", "Within 20 minutes", "Within 30 minutes", "Within 45 minutes", "Within 1 hour"]
)

# -------------------------------
# Web画像取得（Unsplash）
# -------------------------------
def get_food_image(dish_name):
    query = urllib.parse.quote(dish_name)
    return f"https://source.unsplash.com/800x500/?food,{query}"

# -------------------------------
# ボタン処理
# -------------------------------
if st.button("🍽 Get a Recipe"):
    if not mood:
        st.error("Please enter your mood.")
    else:
        with st.spinner("AI is thinking about the best recipe for you..."):
            prompt = f"""
Mood: {mood}
Cuisine: {genre}
Cooking time: {cooking_time}

Suggest ONE dish that fits the conditions.
Answer in ENGLISH only.

Format:
Dish name:
Ingredients:
- item
Steps:
1.
Reason why it matches the mood:
"""

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                recipe_text = response.text

                # 料理名抽出
                dish_name = recipe_text.splitlines()[0].replace("Dish name:", "").strip()

                # 画像取得
                image_url = get_food_image(dish_name)

                # 表示
                st.image(image_url, caption=dish_name, use_container_width=True)

                st.markdown("<div class='recipe-box'>", unsafe_allow_html=True)
                st.markdown(recipe_text)
                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("</div>", unsafe_allow_html=True)
