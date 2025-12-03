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
body {
    background-color: #f5f7fa;
}
.recipe-box {
    background: white;
    padding: 20px;
    margin-top: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.stTextInput > div > div > input {
    border-radius: 10px;
    padding: 10px;
}
.stSelectbox > div > div:first-child {
    border-radius: 10px;
}
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

# ▼ 追加①：料理ジャンル
food_type = st.selectbox(
    "どの料理が食べたい？（料理の系統）",
    ["指定なし", "和食", "洋食", "中華", "韓国料理", "イタリアン", "エスニック", "ヘルシー"],
)

# ▼ 追加②：料理時間
cook_time = st.selectbox(
    "どれくらいで出来上がる料理がいい？（調理時間）",
    ["指定なし", "5分以内", "10分以内", "20分以内", "30分以内", "45分以内", "1時間以内"]
)

if st.button("料理を提案する") and mood:
    with st.spinner("料理を考えています…"):
        prompt_text = f"""
今日の気分は「{mood}」です。

料理の系統: {food_type}
希望の調理時間: {cook_time}

上記の条件に合う料理を1つ提案してください。

【出力内容】
・料理名
・料理ジャンル（例：和食・洋食）
・必要な材料（箇条書き）
・作り方（わかりやすく手順ごとに）
・調理時間（目安）
・おすすめポイント

わかりやすく親しみやすい文章で書いてください。
        """

        try:
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
