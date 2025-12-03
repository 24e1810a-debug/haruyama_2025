import streamlit as st
from google import genai

st.title("🍳 今日の気分で料理を決めるアプリ")

# APIキー設定
client = genai.Client(api_key=st.secrets["api_key"])

# ユーザー入力
mood = st.text_input("今日の気分を入力してください", placeholder="例: 疲れ気味、元気、リラックスしたい")

if st.button("料理を提案する") and mood:
    with st.spinner("料理を考えています…"):
        prompt_text = f"""
今日の気分が「{mood}」です。
この気分に合う料理を1つ提案してください。
レシピは手順ごとにわかりやすく書き、必要な材料も箇条書きで教えてください。
        """
        try:
            # 最新 SDK では generate_content() を使用
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_text
            )

            recipe_text = response.text if hasattr(response, "text") else None

            if recipe_text:
                st.subheader("🍽 今日のおすすめ料理")
                st.write(recipe_text)
            else:
                st.error("料理の提案が返ってきませんでした。")

        except Exception as e:
            st.error(f"料理の提案中にエラーが発生しました: {e}")


