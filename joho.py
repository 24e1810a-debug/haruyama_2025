import streamlit as st
import google.generativeai as genai

# -------------------------------
# ページ全体の設定
# -------------------------------
st.set_page_config(
    page_title="気分でレシピアプリ",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# カスタムCSS（デザイン強化）
# -------------------------------
st.markdown("""
<style>
/* 全体のフォントと背景 */
body {
    background: #f7f7f7;
    font-family: "Hiragino Sans", "Noto Sans JP", sans-serif;
}

/* コンテナのデザイン */
.stContainer {
    background: white;
    padding: 2rem;
    border-radius: 18px;
    box-shadow: 0 3px 15px rgba(0,0,0,0.1);
}

/* タイトルのオシャレ化 */
h1 {
    color: #333;
    text-align: center;
    font-weight: 700;
    margin-bottom: 30px;
}

/* セレクトボックスのデザイン */
.css-1cpxqw2 {
    background: white !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# APIキー読み込み
# -------------------------------
api_key = st.secrets["api_key"]
genai.configure(api_key=api_key)

# ★ GPTクライアント
client = genai.GenerativeModel("gemini-pro")

# -------------------------------
# UI
# -------------------------------
st.title("🍽️ 気分でおすすめレシピを提案するアプリ")

mood = st.selectbox(
    "今日の気分を選んでください",
    ["元気いっぱい", "疲れ気味", "さっぱりしたい", "こってりしたい", "落ち込んでいる"],
    help="気分に合わせて、最適なレシピをAIが提案します！"
)

if st.button("レシピを生成する"):
    with st.spinner("レシピを考えています…🍳"):
        prompt = f"""
        あなたはトップシェフです。
        ユーザーの今日の気分「{mood}」にぴったり合う料理を1つ提案してください。
        
        出力フォーマット：
        ・料理名
        ・概要（短め）
        ・必要な材料
        ・シンプルな作り方
        ・おすすめポイント
        """

        response = client.generate_content(prompt)

        st.markdown("### ✨ 今日のおすすめ料理")
        st.markdown(f'<div class="stContainer">{response.text}</div>', unsafe_allow_html=True)

