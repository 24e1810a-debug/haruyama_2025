import streamlit as st
from google import genai

# -------------------------------
# ページ設定
# -------------------------------
st.set_page_config(
    page_title="気分で料理を決めるアプリ",
    page_icon="🍳",
    layout="wide"
)

# -------------------------------
# カスタムデザインCSS
# -------------------------------
st.markdown("""
<style>
/* 背景 */
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

/* サブタイトル */
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

/* セレクト・テキスト */
.stSelectbox > div > div,
.stTextInput > div > div > input {
    border-radius: 10px !important;
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# タイトル
# -------------------------------
st.title("🍳 今日の気分で料理を決めるアプリ")
st.markdown('<p class="subtitle">気分・ジャンル・時間から最適な料理をAIが提案します</p>', unsafe_allow_html=True)

# -------------------------------
# メインコンテナ（カード風）
# -------------------------------
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    # APIキー
    client = genai.Client(api_key=st.secrets["api_key"])

    # ▼ ユーザー入力 ▼
    mood = st.text_input("今日の気分は？", placeholder="例: 疲れ気味、元気、リラックスしたい")

    genre = st.selectbox(
        "食べたい料理のジャンル",
        ["おまかせ", "和食", "洋食", "中華"]
    )

    cooking_time = st.selectbox(
        "どのくらいで作りたい？",
        ["おまかせ", "10分以内", "20分以内", "30分以内", "45分以内", "1時間以内"]
    )

    st.write("")  # 余白

    # -------------------------------
    # 料理を生成
    # -------------------------------
    if st.button("🍽 料理を提案してもらう"):
        if not mood:
            st.error("気分を入力してください！")
        else:
            with st.spinner("AIが最適な料理を考えています…"):

                prompt = f"""
今日の気分: {mood}
料理ジャンル: {genre}
調理時間: {cooking_time}

上記条件に合う料理を1つ提案してください。

【出力フォーマット】
■ 料理名
■ 材料（箇条書き）
■ 作り方（手順を番号付きで）
■ その料理が気分に合う理由（短く）
                """

                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )
                    recipe_text = response.text if hasattr(response, "text") else None

                    if recipe_text:
                        st.markdown(f"<div class='recipe-box'>{recipe_text}</div>", unsafe_allow_html=True)
                    else:
                        st.error("料理の提案が返ってきませんでした。")

                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

