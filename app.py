import base64
import json
import os
import random
import subprocess
import streamlit as st

st.title("数理科学 問題プリント自動生成ツール")

# ==========================================
# 🔒 パスワード認証ブロック
# ==========================================
if "authenticated" not in st.session_state:
  st.session_state.authenticated = False

if not st.session_state.authenticated:
  st.subheader("🔒 ログイン認証")
  st.markdown("このツールを利用するにはパスワードが必要です。")

  # パスワード入力欄（文字が隠れる設定）
  password_input = st.text_input(
      "パスワードを入力してください", type="password"
  )

  if st.button("ログイン"):
    # ▼▼▼ ここの "Inkimath" がパスワードになります（自由に変更できます） ▼▼▼
    if password_input == "Inkimath":
      st.session_state.authenticated = True
      st.rerun()  # 画面を再読み込みしてメイン画面に進む
    else:
      st.error("❌ パスワードが間違っています。")

  # 認証されるまで、ここでプログラムを停止（これより下は表示されない）
  st.stop()
# ==========================================


# --- 以下は従来のメイン処理 ---


# 1. 外部のJSONファイルから問題データを読み込む関数
def load_questions():
  if os.path.exists("questions.json"):
    with open("questions.json", "r", encoding="utf-8") as f:
      return json.load(f)
  else:
    return {
        "サンプル単元": [{
            "question": "ファイルが見つかりません",
            "answer": "-",
        }]
    }


question_bank = load_questions()

# 2. 条件選択
st.header("1. プリント条件の設定")
selected_unit = st.selectbox("単元を選択してください", list(question_bank.keys()))
max_q = len(question_bank[selected_unit])
num_questions = st.slider(
    "出題数を選択", min_value=1, max_value=max_q, value=min(2, max_q)
)

# 3. プリント生成ボタン
if st.button("PDFプリントを自動生成する"):
  with st.spinner("TeXをコンパイルしてPDFを作成中..."):
    # 選ばれた問題をランダム抽出
    unit_questions = question_bank[selected_unit]
    selected = random.sample(unit_questions, num_questions)

    # TeXコードのボディを組み立て
    tex_body = ""
    for i, q in enumerate(selected, 1):
      tex_body += f"\\item {q['question']}\n\n"

    full_tex_code = f"""\\documentclass[a4paper,11pt]{{ltjsarticle}}
\\usepackage{{luatexja}}
\\usepackage{{amsmath,amssymb}}

\\begin{{document}}

\\section*{{{selected_unit} 演習プリント}}
\\begin{{enumerate}}
{tex_body}\\end{{enumerate}}

\\end{{document}}
"""

    # 一時ファイルのファイル名
    tex_filename = "output.tex"
    pdf_filename = "output.pdf"

    # .texファイルを書き出す
    with open(tex_filename, "w", encoding="utf-8") as f:
      f.write(full_tex_code)

    try:
      # Pythonから lualatex コマンドを呼び出して自動コンパイル
      result = subprocess.run(
          ["lualatex", "-interaction=nonstopmode", tex_filename],
          capture_output=True,
          text=True,
          encoding="utf-8",
      )

      # コンパイルが成功し、PDFが生成されているか確認
      if result.returncode == 0 and os.path.exists(pdf_filename):
        st.success("✨ PDFの自動生成に成功しました！")

        # PDFをバイナリとして読み込む
        with open(pdf_filename, "rb") as pdf_file:
          pdf_bytes = pdf_file.read()

        # ダウンロードボタン
        st.download_button(
            label="📥 完成PDFをダウンロード",
            data=pdf_bytes,
            file_name=f"{selected_unit}_print.pdf",
            mime="application/pdf",
        )

        # 画面上にPDFプレビューを表示
        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px" type="application/pdf"></iframe>'

        st.markdown("### 📄 プレビュー画面")
        st.markdown(pdf_display, unsafe_allow_html=True)

      else:
        st.error(
            "❌ TeXのコンパイル中にエラーが発生しました。ログを確認してください。"
        )
        st.code(result.stdout)

    except Exception as e:
      st.error(
          f"システムエラー: `lualatex` コマンドが見つからないか、実行できません。"
          f" 詳細: {e}"
      )