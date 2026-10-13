import io
import os
import subprocess
import tempfile
import fitz  # PyMuPDF
from PIL import Image
import streamlit as st

# ページの基本設定
st.set_page_config(
    page_title="Math Print Generator", page_icon="数学", layout="wide"
)

# ---------------------------------------------------------
# PDFプレビュー表示関数 (PyMuPDF使用・Chromeブロック回避)
# ---------------------------------------------------------
def render_pdf_preview(pdf_bytes: bytes):
    """PDFのバイナリデータを受け取り、全ページを画像に変換してプレビュー表示する"""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        st.markdown(f"### 📄 プレビュー画面 (全 {len(doc)} ページ)")

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # dpiを150に設定して数式や文字をくっきり綺麗に表示
            pix = page.get_pixmap(dpi=150)
            img = Image.open(io.BytesIO(pix.tobytes("png")))

            st.image(
                img, caption=f"第 {page_num + 1} ページ", use_container_width=True
            )
            st.markdown("---")

    except Exception as e:
        st.error(f"PDFのプレビュー表示に失敗しました: {e}")


# ---------------------------------------------------------
# LaTeXコンパイル関数
# ---------------------------------------------------------
def compile_latex_to_pdf(latex_code: str) -> bytes:
    """LaTeXのソースコードからPDFをコンパイルしてバイナリを返す"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "output.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_code)

        try:
            subprocess.run(
                ["lualatex", "-interaction=nonstopmode", "output.tex"],
                cwd=tmpdir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            pdf_path = os.path.join(tmpdir, "output.pdf")
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    return f.read()
        except subprocess.CalledProcessError as e:
            st.error("LaTeXのコンパイルエラーが発生しました。")
            log_path = os.path.join(tmpdir, "output.log")
            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8", errors="ignore") as log_f:
                    st.text_area("コンパイルログ", log_f.read(), height=200)
            raise e

    return b""


# ---------------------------------------------------------
# メイン画面のUI
# ---------------------------------------------------------
st.title("📐 数学問題プリントジェネレーター")
st.write("LaTeXを用いた美しい数学プリントを生成・プレビューできます。")

# サイドバーの設定
st.sidebar.header("プリント設定")
print_title = st.sidebar.text_input("プリントタイトル", "演習問題プリント")
problem_type = st.sidebar.selectbox(
    "単元・テーマの選択",
    ["微積分 (Real Analysis)", "線形代数 (Linear Algebra)", "図形と方程式 (Geometry)"],
)
num_questions = st.sidebar.slider("問題数", 1, 5, 3)

# プリント生成ボタン
if st.sidebar.button("プリントを生成する"):
    # LaTeXコードの組み立て
    latex_source = f"""
    \\documentclass[11pt,a4paper]{{ltjsarticle}}
    \\usepackage{{amsmath,amssymb,amsthm}}
    \\usepackage{{tcolorbox}}
    \\begin{{document}}
    \\begin{{center}}
        {{\\Large \\textbf{{{print_title}}}}}
    \\end{{center}}
    \\vspace{{1em}}
    \\noindent \\textbf{{単元: {problem_type}}} \\hfill \\textbf{{氏名: \\underline{{\\hspace{{5cm}}}}}}
    \\vspace{{1.5em}}
    """

    for i in range(1, num_questions + 1):
        latex_source += f"""
        \\begin{{tcolorbox}}[colback=white,colframe=blue!50!black,title={{問題 {i}}}]
        関数 $f(x) = x^3 - 3x$ の極値を求めよ。また、グラフの概形を描け。
        \\end{{tcolorbox}}
        \\vspace{{1em}}
        """

    latex_source += """
    \\end{document}
    """

    with st.spinner("PDFをコンパイル中..."):
        try:
            pdf_data = compile_latex_to_pdf(latex_source)
            st.session_state["pdf_data"] = pdf_data
            st.success("✨ プリントの生成が完了しました！")
        except Exception:
            st.error("PDFの生成に失敗しました。")

# 生成されたPDFがある場合の表示
if "pdf_data" in st.session_state:
    # 1. 画像として画面内にプレビュー表示（ブロックを完全に回避）
    render_pdf_preview(st.session_state["pdf_data"])

    # 2. ダウンロードボタン
    st.download_button(
        label="📥 生成されたPDFをダウンロード",
        data=st.session_state["pdf_data"],
        file_name="math_print.pdf",
        mime="application/pdf",
    )
