import streamlit as st
from google import genai

# -------------------------------
# ページ全体の設定
# -------------------------------
st.set_page_config(
    page_title="気分で料理を決めるアプリ",
    page_icon="🍳",
    layout="wide"
)

# -------------------------------
# カスタムCSS（デザイン強化）
# -------------------------------
st.markdown("""
<style>
/* 背景色 */
body {
    background-color: #f5f7fa;
}

/* カード風のボックス */
.recipe-box {
    background: white;
    padding: 20px;
    margin-top: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

/* 入力欄 */
.stTextInput > div > div > input {
    border-radius: 10px;
    padding: 10px;
}

/* ボタン */
.stButton > button {
    background: #ff8c42;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
    transition: 0.2s;
}
.stButton > button:hover {
    background: #ff7b22;
}

/* タイトル */
h1 {
    text-align: center;
    font-weight: 700;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# タイトル
# -------------------------------
st.title("🍳 今日の気分で料理を決めるアプリ")

# -------------------------------
# APIキー設定
# -------------------------------
client = genai.Client(api_key=st.secrets["api_key"])

# -------------------------------
# ユーザー入力
# -------------------------------
mood = st.text_input("今日の気分を入力してください", placeholder="例: 疲れ気味、元気、リラックスしたい")

if st.button("料理を提案する") and mood:
    with st.spinner("料理を考えています…"):
        prompt_text = f"""
今日の気分が「{mood}」です。
この気分に合う料理を1つ提案してください。
レシピは手順ごとにわかりやすく書き、必要な材料も箇条書きで教えてください。
        """
        try:
            # 最新 SDK の generate_content()
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_text
            )

            recipe_text = response.text if hasattr(response, "text") else None

            if recipe_text:
                st.subheader("🍽 今日のおすすめ料理")
                st.markdown(f"<div class='recipe-box'>{recipe_text}</div>", unsafe_allow_html=True)
            else:
                st.error("料理の提案が返ってきませんでした。")

        except Exception as e:
            st.error(f"料理の提案中にエラーが発生しました: {e}")
