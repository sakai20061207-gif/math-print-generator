import base64
import io
import os
import random
import subprocess
import tempfile
import streamlit as st
import streamlit.components.v1 as components

# ページの基本設定
st.set_page_config(
    page_title="Math Print Generator", page_icon="数学", layout="wide"
)

# ---------------------------------------------------------
# 単元ごとの問題データの定義（全問題リスト）
# ---------------------------------------------------------
question_database = {
    "展開・因数分解": [
        "$(3a-4b)^3$",
        "$(2x+1)^3$",
        "$(4p-3q)^3$",
        "$(x+2y)^3$",
        "$(x+5)^3$",
        "$(a-3)^3$",
        "$(5x+3y)^3$",
        "$(ab-4)^3$",
        "$(3x+1)^3$",
        "$(4x-1)^3$",
        "$(x+5)(x^2-5x+25)$",
        "$(x+4)(x^2-4x+16)$",
        "$(x+2)(x^2-2x+4)$",
        "$(3x+1)(9x^2-3x+1)$",
        "$(4a-3b)(16a^2+12ab+9b^2)$",
        "$(2x^2+3)(4x^4-6x^2+9)$",
        "$(2a-3b)(4a^2+6ab+9b^2)$",
        "$(2a-1)(4a^2+2a+1)$",
        "$(7x-3y)(49x^2+21xy+9y^2)$",
        "$(a^2-2b^2)(a^4+2a^2b^2+4b^2)$",
        "$(x-3)(x-1)(x+2)(x+4)$",
        "$(x+1)(x+2)(x+3)(x+6)$",
        "$(x-1)(x-3)(x-5)(x-7)$",
        "$(x-2)(x+3)(x+4)(x-6)$",
        "$(x+1)^3(x-1)^3$",
        "$(a-2b)^3(a+2b)^3$",
        "$(3a+1)^3(3a-1)^3$",
        "$(x+2)(x-2)(x^4+4x^2+16)$",
        "$(x+1)(x-1)(x^2+x+1)(x^2-x+1)$",
        "$(x+2)(x-3)(x^2-2x+4)(x^2+3x+9)$",
        "$(a+b)(a-b)(a^2+ab+b^2)(a^2-ab+b^2)$",
        "$8x^3-1$",
        "$a^3-64b^3$",
        "$27a^3+8$",
        "$16x^3-2x^3y^3$",
        "$135x^3y+40y^4$",
        "$x^3+12x^2+48x+64$",
        "$a^3b^3-c^3d^3$",
        "$27x^3-27x^2+9x-1$",
        "$8x^3-12x^2+6x-1$",
        "$x^3+6x^2+12x+8$",
        "$64a^6-1$",
        "$a^6-b^6$",
        "$a^6-28a^3b^3+27b^6$",
        "$x^6-124x^3-125$",
        "$x^6-7x^3-8$",
        "$x^3+4x^2-8x-8$",
        "$x^6+26x^3-27$",
        "$(a+b)^3+c^3$",
    ],
    "複素数": [
        "$\\frac{1-2i}{2-i}$",
        "$\\frac{1}{i^3}$",
        "$\\frac{2i-3}{i}$",
        "$\\frac{1}{1+i}$",
        "$\\frac{5-2i}{5+2i}$",
        "$\\frac{3+2i}{2-i}$",
        "$\\left(\\frac{5+3i}{1+i}\\right)^2$",
        "$\\left(\\frac{3+2i}{2-3i}\\right)^2$",
        "$\\left(\\frac{-1-\\sqrt{3}}{2}\\right)^3$",
        "$\\left(\\frac{2+2i}{2-2i}\\right)^2$",
        "$(2+i)^3$",
        "$\\frac{1+3i}{3-i}\\times\\frac{2i+3}{5i-1}$",
        "$\\frac{1-i}{3+i}+\\frac{1+i}{3-i}$",
        "$\\frac{1-2i}{2+i}+\\frac{2-i}{1+2i}$",
        "$\\frac{1-2i}{3-i}-\\frac{5+i}{5i}$",
        "$\\left(\\frac{7+3i}{2+5i}\\right)^{10}$",
        "$i^{100}$",
        "$(1+\\sqrt{3})^8$",
        "$i+i^2+i^3+i^4$",
        "$i+i^2+i^3+i^4+\\cdots+i^{30}$",
        "次の多項式を[\\quad]内の式で割ったときの余りを求めよ：$x^3+x^2+2x-1\\quad[x-2]$",
        "次の多項式を[\\quad]内の式で割ったときの余りを求めよ：$x^3+4\\quad[2x+3]$",
        "次の多項式を[\\quad]内の式で割ったときの余りを求めよ：$x^2-5x-14\\quad[x-3]$",
        "次の多項式を[\\quad]内の式で割ったときの余りを求めよ：$x^3+3x^2-2x+1\\quad[x+2]$",
        "次の多項式を[\\quad]内の式で割ったときの余りを求めよ：$3x^3-10x^2+1\\quad[3x-1]$",
        "次の多項式を[\\quad]内の式で割ったときの余りを求めよ：$2x^2-3x+9\\quad[2x+1]$",
        "次の多項式を[\\quad]内の式で割ったときの余りを求めよ：$2x^3-x^2+5\\quad[2x-3]$",
        "次の多項式を[\\quad]内の式で割ったときの余りを求めよ：$x^{20}+1\\quad[x^2+x]$",
        "次の多項式を[\\quad]内の式で割ったときの余りを求めよ：$x^{20}+x^5-5\\quad[x^2-1]$",
        "次の多項式を[\\quad]内の式で割ったときの余りを求めよ：$x^{100}+x^{99}+1\\quad[x^2-x]$",
        "次の式を有理数の範囲で因数分解せよ：$3x^3-x^2-8x-4$",
        "次の式を有理数の範囲で因数分解せよ：$2x^3-5x^2+1$",
        "次の式を有理数の範囲で因数分解せよ：$x^3-5x+4$",
        "次の式を有理数の範囲で因数分解せよ：$x^3-13x-12$",
        "次の式を有理数の範囲で因数分解せよ：$x^3-x^2-14x+24$",
        "次の式を有理数の範囲で因数分解せよ：$x^3+x^2-5x-6$",
        "次の式を有理数の範囲で因数分解せよ：$x^3-27x+54$",
        "次の式を有理数の範囲で因数分解せよ：$3x^3+5x^2-6x-8$",
        "次の式を有理数の範囲で因数分解せよ：$2x^3+x^2-3x+1$",
        "次の式を有理数の範囲で因数分解せよ：$6x^3-x^2-20x+12$",
    ],
    "二次関数": [
        "次の二次関数の最大・最小値を求めよ：$y=2x^2-4x+5\\;(-1\\leqq x\\leqq5)$",
        "次の二次関数の最大・最小値を求めよ：$y=\\frac{1}{2}x^2-4x+2\\;(-4\\leqq x\\leqq2)$",
        "次の二次関数の最大・最小値を求めよ：$y=-2x^2+4x+2\\;(0\\leqq x\\leqq6)$",
        "次の二次関数の最大・最小値を求めよ：$y=-x^2-2x+2\\;(-4\\leqq x\\leqq2)$",
        "次の二次関数の最大・最小値を求めよ：$y=3x^2+24x+28\\;(-2\\leqq x\\leqq0)$",
        "次の二次関数の最大・最小値を求めよ：$y=-\\frac{1}{4}x^2-2x+1\\;(-3\\leqq x\\leqq-2)$",
        "次の二次関数の最大・最小値を求めよ：$y=2x^2+\\frac{3}{2}x-2\\;(-1\\leqq x\\leqq0)$",
        "次の二次関数の最大・最小値を求めよ：$y=\\frac{3}{2}x^2+\\frac{7}{3}x+\\frac{7}{3}\\;(-2\\leqq x\\leqq3)$",
        "次の二次関数の最大・最小値を求めよ：$y=-\\frac{4}{3}x^2+2x+1\\;(0\\leqq x\\leqq2)$",
        "次の二次関数の最大・最小値を求めよ：$y=-x^2+x+\\frac{7}{3}\\;(0\\leqq x\\leqq1)$",
        "頂点が$(1, 1)$で，点$(-1, 9)$を通る二次関数を求めよ。",
        "頂点が$(3, 6)$で，点$(1, -2)$を通る二次関数を求めよ。",
        "頂点が$(2, 3)$で，点$(3, 6)$を通る二次関数を求めよ。",
        "3点$(0, 3), (-1, 9), (1, 1)$を通る二次関数を求めよ。",
        "3点$(-1, -8), (2, -2), (3, -4)$を通る二次関数を求めよ。",
        "3点$(-1, 5), (2, 5), (3, 9)$を通る二次関数を求めよ。",
        "軸が直線$x=-1$で，2点$(1, 9), (0, 3)$を通る二次関数を求めよ。",
        "軸が直線$x=1$で，2点$(0, 5), (-2, 3)$を通る二次関数を求めよ。",
        "軸が直線$x=1$で，2点$(-1, -5), (2, 1)$を通る二次関数を求めよ。",
        "$x$軸と2点$(1, 0), (4, 0)$で交わり，点$(0, 4)$を通る二次関数を求めよ。",
        "$x$軸と2点$(2, 0), (-3, 0)$で交わり，点$(-1, 18)$を通る二次関数を求めよ。",
        "$x$軸と2点$(1, 0), (-3, 0)$で交わり，点$(-5, 24)$を通る二次関数を求めよ。",
        "$x=3$で最小値が-4となり点$(5, 0)$を通る二次関数を求めよ。",
        "$x=2$で最大値が-3となり点$(1, -4)$を通る二次関数を求めよ。",
        "$x=1$で最小値が2となり点$(3, 6)$を通る二次関数を求めよ。",
        "$y=3x^2$を平行移動したもので，頂点が$(2, -3)$となる二次関数を求めよ。",
        "$y=-2x^2+5x+1$を平行移動したもので，2点$(0, 3), (-2, -7)$を通る二次関数を求めよ。",
        "$y=x^2-3x+1$を平行移動したもので，点$(2, 3)$を通り，その頂点は直線$y=3x-1$上にある二次関数を求めよ。",
        "次の不等式を解け：$x^2-4<0$",
        "次の不等式を解け：$3x^2-x>0$",
        "次の不等式を解け：$x^2-3x+2>0$",
        "次の不等式を解け：$2x^2+9x+9\\geqq 0$",
        "次の不等式を解け：$-3x^2+10x-8>0$",
        "次の不等式を解け：$3x^2-\\sqrt{7}x-1\\geqq 1$",
        "次の不等式を解け：$x^2+x\\leqq 3x+24$",
        "次の不等式を解け：$x^2-4x+2>0$",
        "次の不等式を解け：$x^2+5x+1<0$",
        "次の不等式を解け：$2x^2-9\\geqq 0$",
        "次の不等式を解け：$x^2+12\\geqq 7x$",
        "次の不等式を解け：$4x^2-4x+1>0$",
        "次の不等式を解け：$-3x^2+6x-2\\geqq 0$",
        "次の不等式を解け：$x^2+7x+6\\leqq 0$",
        "次の不等式を解け：$9x^2+1\\leqq 6x$",
        "次の不等式を解け：$x^2-x+3\\geqq 0$",
        "次の不等式を解け：$-2x^2-6x-5>0$",
        "次の不等式を解け：$9x^2+24x+16\\leqq 0$",
        "次の不等式を解け：$-x^2+2x+4\\leqq 0$",
        "次の不等式を解け：$-6x^2+7x+3\\geqq 0$",
        "次の連立不等式を解け：$\\begin{cases} x^2+6x+8>0\\\\ x^2+2x-3<0 \\end{cases}$",
        "次の連立不等式を解け：$\\begin{cases} x^2-x-12\\leqq 0\\\\ x^2-3x+2>0 \\end{cases}$",
        "次の連立不等式を解け：$\\begin{cases} x^2+2x-2\\geqq 0\\\\ x^2+2x-8<0 \\end{cases}$",
        "次の連立不等式を解け：$\\begin{cases} 2x^2+5x<3\\\\ 3x^2+11x<4 \\end{cases}$",
        "次の連立不等式を解け：$\\begin{cases} x^2+x-2<0\\\\ x^2+x-1\\geqq 0 \\end{cases}$",
        "次の連立不等式を解け：$\\begin{cases} x^2-10x+20<0\\\\ -x^2+6x-3>0 \\end{cases}$",
        "次の連立不等式を解け：$\\begin{cases} x^2+4x\\geqq 0\\\\ x^2-9>0 \\end{cases}$",
        "次の連立不等式を解け：$\\begin{cases} x^2-4x+1\\leqq 0\\\\ -3x^2+11x+4>0 \\end{cases}$",
        "次の連立不等式を解け：$\\begin{cases} 4x+4\\geqq 3x^2\\\\ 2x^2+1>4x \\end{cases}$",
        "次の連立不等式を解け：$\\begin{cases} x^2+x-1>0\\\\ 6x^2+x-15<0 \\end{cases}$",
    ],
    "三角関数": [
        "$0 \\leqq x < 2\\pi$ のとき，方程式 $\\sin x = -\\frac{1}{2}$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，方程式 $2\\cos x = -\\sqrt{3}$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，方程式 $\\tan x = -1$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，不等式 $\\sin x > \\frac{\\sqrt{3}}{2}$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，不等式 $2\\cos x \\geqq -1$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，方程式 $2\\sin \\frac{x}{2} = \\sqrt{3}$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，不等式 $\\tan x \\leqq -\\sqrt{3}$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，方程式 $\\cos\\left(x + \\frac{\\pi}{3}\\right) = \\frac{\\sqrt{3}}{2}$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，方程式 $2\\cos^2 x - \\sin x - 1 = 0$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，不等式 $2\\sin^2 x + \\cos x - 1 \\leqq 0$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，方程式 $\\cos x + \\cos 2x = 0$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，不等式 $\\sin 2x + \\cos x \\leqq 0$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，不等式 $\\cos 2x - 3\\cos x + 2 < 0$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，方程式 $\\sin x \\cos x = \\frac{1}{4}$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，方程式 $\\cos^4 x - \\sin^4 x = -1$ を解け。",
        "$0 \\leqq x \\leqq \\pi$ のとき，方程式 $\\sin x \\cos x \\cos 2x = -\\frac{1}{8}$ を解け。",
        "$0 \\leqq \\theta < 2\\pi$ のとき，不等式 $\\cos 2\\theta + \\sqrt{3}\\sin \\theta \\geqq 1$ を解け。（龍谷大学）",
        "$0 < x < \\frac{\\pi}{2}$ のとき，方程式 $\\frac{\\sin x}{\\cos x} + \\frac{\\cos x}{\\sin x} = 4$ を解け。（文教大学）",
        "$0 \\leqq x < 2\\pi$ のとき，不等式 $\\cos 2x + 3\\cos x - 1 \\leqq 0$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，不等式 $2(\\cos^2 x - \\sin^2 x) \\leqq -\\sqrt{3}$ を解け。",
        "$0 < x < \\frac{\\pi}{2}$ のとき，方程式 $\\cos^2 x - \\sin^2 x + \\frac{1}{16} \\left( \\frac{1}{\\cos^2 x} - \\frac{1}{\\sin^2 x} \\right) = 0$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，方程式 $\\sin x + \\cos x = -1$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，方程式 $\\sqrt{3}\\sin x + 3\\cos x = -3$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，方程式 $\\sin 2x - \\sqrt{3}\\cos 2x = 1$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，不等式 $\\sin x - \\cos x \\leqq \\frac{\\sqrt{2}}{2}$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，不等式 $\\sqrt{3}\\sin x - \\cos x < 1$ を解け。",
        "$0 \\leqq x < 2\\pi$ のとき，方程式 $\\sin\\left(x + \\frac{\\pi}{3}\\right) - \\sin x = 1$ を解け。",
        "$0 \\leqq x \\leqq \\pi$ のとき，不等式 $2\\sin x \\cos x + \\sqrt{3}\\cos 2x + \\sqrt{3} < 0$ を解け。",
        "$0 \\leqq \\theta < 2\\pi$ のとき，不等式 $\\cos\\left(\\theta + \\frac{\\pi}{4}\\right) + \\cos\\left(\\theta - \\frac{\\pi}{4}\\right) \\leqq 1$ を解け。",
        "$0 \\leqq x \\leqq \\pi$ のとき，不等式 $-1 < \\cos x - \\sin x < \\frac{\\sqrt{2}}{2}$ を解け。（日本大学）",
        "$\\frac{\\pi}{2} \\leqq \\theta \\leqq \\pi$ のとき，方程式 $2\\sin\\left(\\theta + \\frac{\\pi}{5}\\right) - 2\\cos\\left(\\theta + \\frac{\\pi}{30}\\right) = 1$ を解け。（センター試験）",
        "$0 \\leqq x < 2\\pi$ のとき，不等式 $\\sin 2x > \\sqrt{2}\\cos\\left(x + \\frac{\\pi}{4}\\right) + \\frac{1}{2}$ を解け。（センター試験）",
        "$0 < \\theta < \\frac{\\pi}{2}$ のとき，不等式 $\\cos 3\\theta + 2\\cos \\theta > 0$ を解け。（南山大学）",
        "$0 \\leqq x < 2\\pi$ のとき，方程式 $\\cos x + \\cos 2x + \\cos 3x = 0$ を解け。（甲南大学）",
        "$0 < x < \\pi$ のとき，方程式 $\\sqrt{3}\\sin 2x - \\cos 2x - \\frac{1}{\\sqrt{3}}(\\sqrt{3}\\sin x + \\cos x) = 0$ を解け。（北海道大学）",
        "$0 \\leqq x \\leqq \\pi$ のとき，$y = \\sin x - \\cos x$ の最大値，最小値とそのときの $x$ の値を求めよ。",
        "$0 \\leqq x \\leqq \\pi$ のとき，$y = 3\\sin x + 4\\cos x$ の最大値，最小値を求めよ。",
        "$0 \\leqq x < 2\\pi$ のとき，$y = \\cos^2 x + \\sin x - 1$ の最大値，最小値とそのときの $x$ の値を求めよ。",
        "$0 \\leqq x < 2\\pi$ のとき，$y = \\cos 2x + 2\\cos x - 2$ の最大値，最小値とそのときの $x$ の値を求めよ。",
        "$0 \\leqq \\theta \\leqq \\frac{\\pi}{2}$ のとき，$y = \\cos^2 2\\theta + 2\\sin 2\\theta + 2$ の最大値，最小値とそのときの $\\theta$ を求めよ。（甲南大学）",
        "$0 \\leqq \\theta \\leqq 2\\pi$ のとき，$y = 2\\cos \\theta + 4\\sqrt{3}\\sin\\left(\\frac{\\theta}{2} - \\frac{\\pi}{2}\\right)$ の最大値，最小値とそのときの $\\theta$ の値を求めよ。",
        "$0 \\leqq \\theta \\leqq \\pi$ のとき，$f(\\theta) = \\sin^4 \\theta + \\cos^4 \\theta$ の最大値，最小値とそのときの $\\theta$ を求めよ。（長崎大学）",
        "$0 < x \\leqq \\frac{\\pi}{2}$ のとき，$y = \\frac{2 - \\cos^2 x + \\frac{1}{4}}{\\sin^2 x}$ の最小値とそのときの $x$ の値を求めよ。（甲南大学）",
        "$0 \\leqq \\theta \\leqq \\pi$ のとき，$y = \\sin \\frac{\\theta}{2} + \\cos(\\frac{\\theta}{2} - \\frac{\\pi}{6})$ の最大値，最小値とそのときの $\\theta$ を求めよ。",
        "$\\theta$ を実数とし，$y = \\cos 2\\theta - \\sin \\theta + 2\\sin\\left(\\theta + \\frac{\\pi}{3}\\right)$ の最大値と最小値を求めよ。（南山大学）",
        "$f(\\theta) = (\\cos \\theta + \\sqrt{3}\\sin \\theta)(\\sqrt{3}\\cos \\theta - \\sin \\theta) \\left(0 \\leqq \\theta \\leqq \\frac{\\pi}{2}\\right)$ の最大値，最小値を求めよ。（名城大学）",
        "$f(\\theta) = 4\\left(\\sin^3 \\frac{\\theta}{2} + \\cos^3 \\frac{\\theta}{2}\\right) + 6\\left(\\sin \\frac{\\theta}{2} + \\cos \\frac{\\theta}{2}\\right)(\\sin \\theta - 2) - \\sqrt{6}(\\sin \\theta + 1)$ の最小値とそのときの $\\theta$ の値を求めよ。（熊本大学）",
        "$0 \\leqq \\theta < 2\\pi$ のとき，$y = -4\\sin \\theta \\cos^2 \\theta + 3\\cos 2\\theta + 4\\sin \\theta$ の最小値とそのときの $\\theta$ を求めよ。（関西学院大学）",
        "$y = 2\\sin^3 x \\cos x - \\sin x \\cos x \\left(0 \\leqq x \\leqq \\frac{\\pi}{2}\\right)$ の最大値，最小値とそのときの $x$ の値を求めよ。",
        "$y = \\sin^2 x + 3\\cos^2 x + 2\\sqrt{3}\\sin x \\cos x \\left(0 \\leqq x \\leqq \\frac{\\pi}{2}\\right)$ の最大値，最小値とそのときの $x$ の値を求めよ。",
        "$f(x) = 4\\cos^2 \\frac{x}{2} + 2\\sin^2 \\frac{x}{2} + \\sqrt{3}\\sin x$ ($0 \\leqq x < 2\\pi$) の最大値とそのときの $x$ を求めよ。（上智大学）",
        "$0 \\leqq \\theta < \\pi$ のとき，$f(\\theta) = \\cos^2 \\theta - 6\\cos \\theta \\sin \\theta - 5\\sin^2 \\theta$ の最大値，最小値およびそのときの $\\theta$ の値を求めよ。（関西学院大学）",
        "$y = \\cos 2\\theta + \\sqrt{3}\\sin 2\\theta - 2\\sqrt{3}\\cos \\theta - 2\\sin \\theta\\left(-\\frac{\\pi}{2} \\leqq \\theta \\leqq 0\\right)$ の最小値を求めよ。① $t = \\sin \\theta + \\sqrt{3}\\cos \\theta$ とおくとき，$y$ を $t$ の式で表せ。② $y$ の最小値とそのときの $\\theta$ の値を求めよ。（センター試験）",
        "$y = \\sin 2\\theta + 2\\cos^2 \\frac{\\theta}{2} + \\sin \\theta + 2$ ($0 \\leqq \\theta < 2\\pi$) の最大値を求めよ。（名城大学）",
        "$-\\frac{\\pi}{2} \\leqq x \\leqq \\frac{7}{6}\\pi$ のとき，$y = \\sin^2 x + 3\\cos^2 x - 2\\sqrt{3}\\sin x \\cos x - 2\\sqrt{3}\\sin x + 6\\cos x - 1$ の最大値，最小値とそのときの $x$ の値を求めよ。（日本女子大学）",
        "$f(\\theta) = 3(1 + \\sin 2\\theta)^2 - 4(\\sin \\theta + \\cos \\theta)^3 \\left(-\\frac{\\pi}{2} \\leqq \\theta \\leqq \\frac{\\pi}{2}\\right)$ の最小値とそのときの $\\theta$ の値を求めよ。（神奈川大学）",
        "関数 $f(\\theta) = 6\\sin \\theta \\cos \\theta - 8\\sin^3 \\theta \\cos \\theta + 2\\cos^2 \\theta - 1$ の最大値，最小値を求めよ。（宮城教育大学）",
        "$f(\\theta) = \\sqrt{2}(\\sin \\theta + \\sqrt{3}\\cos \\theta) - \\cos \\theta(\\sqrt{3}\\sin \\theta + \\cos \\theta) \\left(0 \\leqq \\theta \\leqq \\frac{\\pi}{2}\\right)$ の最大値，最小値とそのときの $\\theta$ の値を求めよ。（尾道大学）",
        "$f(\\theta) = \\sin 3\\theta - 3(\\sin \\theta + \\sqrt{3}\\cos \\theta)$ ($0 \\leqq \\theta \\leqq \\pi$) の最大値，最小値とそのときの $\\theta$ の値を求めよ。（関西学院大学）",
        "$\\alpha = \\frac{\\pi}{5}$ とおくと，$5\\alpha = \\pi$ である。これを用いて，$\\cos \\frac{\\pi}{5}$ の値を求めよ。",
        "2直線 $\\ell: y = 3x - 1, m: y = \\frac{1}{2}x$ のなす角 $\\theta \\left(0 \\leqq \\theta \\leqq \\frac{\\pi}{2}\\right)$ を求めよ。",
        "$f(x) = x^2 + 4 \\left( \\frac{3\\tan \\theta}{1 + \\tan^2 \\theta} - \\sqrt{3} \\right)x + 3(\\sin^2 \\theta + 3\\cos^2 \\theta)^2$ とし，すべての実数 $x$ に対して $f(x) > 0$ となるような $\\theta$ の値の範囲を求めよ。ただし，$-\\frac{\\pi}{2} < \\theta < \\frac{\\pi}{2}$ とする。（センター試験）",
        "座標平面上に $A(1, 0), P(\\cos 2\\theta, \\sin 2\\theta), Q(2\\cos 3\\theta, 2\\sin 3\\theta)$ をとる。$\\theta$ が $\\frac{\\pi}{3} \\leqq \\theta < \\pi$ の範囲を動くとき，$AP^2 + PQ^2$ の最大値，最小値とそのときの $\\theta$ の値を求めよ。（センター試験）",
        "$-\\frac{\\pi}{2} \\leqq \\theta \\leqq \\frac{\\pi}{4}$ とし，$f(\\theta) = \\sin 3\\theta - \\cos 3\\theta - 3\\sin 2\\theta + 3(\\sin \\theta + \\cos \\theta)$ とする。方程式 $f(\\theta) = k$ が異なる3つの実数解をもつとき，$k$ の値の範囲を求めよ。（新潟大学）",
        "$0 \\leqq \\theta \\leqq \\pi$ とし，$f(\\theta) = 2(\\cos^3 \\theta - \\sin^3 \\theta), t = \\cos \\theta - \\sin \\theta$ とおき，$f(\\theta)$ を $t$ で表し，$f(\\theta) = k$ を満たす $\\theta$ の個数を調べよ。（大阪教育大学）",
        "$0 \\leqq x \\leqq 2\\pi$ とし，$f(x) = |\\sin 2x - 2\\sin x - 2\\cos x + 1|$ とする。方程式 $f(x) = k$ の異なる実数解の個数を $k$ の値で場合分けをして求めよ。（近畿大学）",
        "$f(\\theta) = \\frac{1}{\\sqrt{2}}\\sin 2\\theta - \\sin \\theta + \\cos \\theta$ ($0 \\leqq \\theta \\leqq \\pi$) とする。① $f(\\theta)$ の最大値，最小値とそのときの $\\theta$ の値を求めよ。② $f(\\theta) = a$ となる $\\theta$ がちょうど2個存在するような $a$ の値の範囲を求めよ。（北海道大学）",
        "$0 \\leqq \\alpha \\leqq \\pi, 0 \\leqq \\beta \\leqq \\pi, \\alpha < \\beta$ であり，$\\begin{cases} \\cos 2\\alpha - \\cos 2\\beta = \\frac{4}{15} \\\\ \\cos \\alpha \\cos \\beta = -\\frac{2\\sqrt{15}}{15} \\\\ |\\cos \\alpha| \\geqq |\\cos \\beta| \\end{cases}$ を満たすとき，$\\cos \\alpha, \\cos \\beta$ の値をそれぞれ求めよ。（センター試験）",
        "$0 < x < 2\\pi$ のとき，方程式 $\\sin 5x = \\sin x$ を解け。（京都工芸繊維大学）",
        "$0 \\leqq x \\leqq \\pi$ のとき，方程式 $\\sin x + \\sin 2x + \\sin 3x = \\cos x + \\cos 2x + \\cos 3x$ を解け。（宮崎大学）",
        "次の問いに答えよ。① $\\sin \\frac{2\\pi}{5} = \\sin \\frac{3\\pi}{5}$ に着目して，$\\cos \\frac{\\pi}{5}$ と $\\sin \\frac{\\pi}{5}$ の値を求めよ。② $\\sin \\frac{\\pi}{5} \\sin \\frac{2\\pi}{5} \\sin \\frac{3\\pi}{5} \\sin \\frac{4\\pi}{5}$ の値を求めよ。（中央大学）",
        "$a = \\cos \\frac{2}{7}\\pi + \\cos \\frac{4}{7}\\pi + \\cos \\frac{6}{7}\\pi, b = \\cos \\frac{2}{7}\\pi \\cos \\frac{4}{7}\\pi \\cos \\frac{6}{7}\\pi$ の値を求めよ。① $\\cos 3\\theta = \\cos 4\\theta$ を満たすとき，解の1つが $\\cos \\theta$ であるような4次の方程式を作れ。② $a, b$ の値を求めよ。（東京慈恵会医科大学）",
    ],
    "指数・対数関数": [
        "方程式 $4^x = 2^{x+3}$ を解け。",
        "方程式 $27^{x+1} = 9^{2x+3}$ を解け。（神奈川大学）",
        "不等式 $\\left( \\frac{1}{2} \\right)^{x-2} > \\left( \\frac{1}{8} \\right)^x$ を解け。",
        "不等式 $\\left( \\frac{4}{3} \\right)^x < \\left( \\frac{3}{4} \\right)^{2x-1}$ を解け。",
        "方程式 $9^x - 10 \\cdot 3^x + 9 = 0$ を解け。",
        "方程式 $2^{2x+1} = 3 \\cdot 2^{x+2} + 32$ を解け。（福岡大学）",
        "方程式 $8^x + 8 = 3(4^x + 2^{x+1})$ を解け。（龍谷大学）",
        "方程式 $8^x + 4^x = 9 \\cdot 2^x + 9$ を解け。（会津大学）",
        "不等式 $3^{x-2} < 9^{1-2x} < 27^{2x+2}$ を解け。（島根県立大学）",
        "不等式 $2^{2x+1} - 7 \\cdot 2^x - 4 < 0$ を解け。",
        "不等式 $4^x - 6 \\cdot 2^x + 8 > 0$ を解け。",
        "不等式 $3^{2x+1} - 28 \\cdot 3^x + 9 < 0$ を解け。（日本大学）",
        "$6 \\cdot 3^x + 7 \\sqrt{3^x} - 3 = 0$ を解け。（駒澤大学）",
        "方程式 $2^{x+2} + 2^{-x+1} - 9 = 0$ を解け。（関西学院大学）",
        "方程式 $\\frac{1}{2} \\cdot \\left( \\frac{1}{16} \\right)^{x-1} - 9 \\cdot \\left( \\frac{1}{4} \\right)^x + 1 = 0$ を解け。",
        "不等式 $2 \\cdot 4^{1-x} + 9 \\cdot 2^{1-x} \\geqq 5$ を解け。（福岡大学）",
        "不等式 $\\left( \\frac{1}{4} \\right)^x - 5 \\cdot \\left( \\frac{1}{2} \\right)^{x+2} + \\frac{1}{4} < 0$ を解け。",
        "方程式 $4^x - 3 \\cdot 2^x + 3 \\cdot 2^{-x} + 4^{-x} = 0$ を解け。（信州大学）",
        "方程式 $\\log_3 x = 4$ を解け。",
        "方程式 $\\log_8 x = \\frac{1}{2}$ を解け。",
        "方程式 $\\log_2 x + \\log_2(x+3) = 2$ を解け。",
        "不等式 $\\log_2(x-3) < 4$ を解け。",
        "不等式 $\\log_{\\frac{1}{3}} x < 2$ を解け。",
        "不等式 $\\log_3(x+5) + \\log_3(7-x) < 3$ を解け。",
        "不等式 $\\log_{10}(x-1) + \\log_{10}(x+3) < 0$ を解け。（麻布大学）",
        "不等式 $(\\log_{\\frac{1}{2}} x)^2 - \\log_{\\frac{1}{2}} x^3 < 4$ を解け。",
        "不等式 $\\log_{\\frac{1}{2}} x^2 < (\\log_{\\frac{1}{2}} x)^2$ を解け。（北九州市立大学）",
        "不等式 $(\\log_3 x)^2 - \\log_3 x^4 + 3 > 0$ を解け。（久留米大学）",
        "方程式 $(\\log_2 x)^2 + \\log_2(4x^2) - 5 \\geqq 0$ を解け。（青山学院大学）",
        "方程式 $(\\log_3 x)^2 = \\log_3 9x$ を解け。（専修大学）",
        "方程式 $\\log_2 x + \\log_8 x = (\\log_2 x)(\\log_8 x)$ を解け。（京都府立大学）",
        "方程式 $\\log_2(x-1) - \\log_{\\frac{1}{2}}(x-4) = 1$ を解け。（琉球大学）",
        "方程式 $\\log_2(x+4) - \\log_4(x+7) = 1$ を解け。（関西学院大学）",
        "方程式 $\\log_3(x+3) + \\log_3(x+5) - \\log_3(x+9) = 0$ を解け。（駒澤大学）",
        "不等式 $\\log_2(3x-1) + \\log_2(4x+5) < \\log_4(7x-1)^2$ を解け。（甲南大学）",
        "方程式 $\\frac{4 \\cdot 2^x}{4^{x-1} + 1} = 2$ を解け。（日本大学）",
        "不等式 $\\log_2(x-2) > \\log_4(12-x^2)$ を解け。（福岡大学）",
        "不等式 $\\log_{\\frac{1}{4}}(x^2+8) \\leqq \\log_{\\frac{1}{2}}(x+2)$ を解け。（福岡大学）",
        "不等式 $2\\log_{\\frac{1}{3}} x + \\log_3(x+4) > 1$ を解け。（文教大学）",
        "不等式 $2\\log_3(x+3) + \\log_{\\frac{1}{3}}(x+9) - 1 \\leqq 0$ を解け。（島根県立大学）",
        "不等式 $\\frac{3}{4}\\log_2 \\sqrt{2}(x-6) + \\log_{\\frac{1}{4}}(x-3) < -1$ を解け。",
        "不等式 $12(\\log_2 \\sqrt{x})^2 - 7\\log_4 x - 10 > 0$ を解け。（センター試験）",
        "不等式 $\\log_2(\\log_2(\\log_2 x)) \\leqq 1$ を解け。（甲南大学）",
        "方程式 $\\log_x 8 - \\log_2 \\frac{x}{4} = 0$ を解け。（龍谷大学）",
        "方程式 $\\log_2 x + 2\\log_x 2 = 3$ を解け。（成蹊大学）",
        "不等式 $\\log_2 x - \\log_x 8 + 2 > 0$ を解け。（日本大学）",
        "不等式 $\\log_2(\\sqrt{2}x) - \\log_{\\sqrt{x}} 8 + 2 > 0$ を解け。（法政大学）",
        "不等式 $\\log_3(5-x^2) + \\log_{\\frac{1}{3}}(5-x) \\geqq \\log_9(x^2-2x+1) - 1$ を解け。（福島県立医科大学）",
        "方程式 $\\log_2 |x^2-3x+2| + \\log_2 |x^2-5x+6| = 2\\log_2(x-2)$ を解け。（山形大学）",
        "$x < y$ とし，$xy = 128$, $\\frac{1}{\\log_2 x} + \\frac{1}{\\log_2 y} = \\frac{7}{12}$ とするとき，$x, y$ の値を求めよ。（センター試験）",
        "連立方程式 $\\begin{cases} 8 \\cdot 3^x - 3^y = -27 \\\\ \\log_2(x+1) - \\log_2(y+3) = -1 \\end{cases}$ を解け。（早稲田大学）",
        "連立方程式 $\\begin{cases} \\log_{2x} y + \\log_x 2y = 1 \\\\ \\log_2 xy = 1 \\end{cases}$ を解け。（横浜国立大学）",
        "連立方程式 $\\begin{cases} \\log_2(x+2) - 2\\log_4(y+3) = -1 \\\\ \\left(\\frac{1}{3}\\right)^y - 11 \\cdot \\left(\\frac{1}{3}\\right)^{x+1} + 6 = 0 \\end{cases}$ を解け。（センター試験）",
        "$y = 2^{2x+1} - 2^x + 1$ の最小値とそのときの $x$ の値を求めよ。",
        "$y = 2^{x+3} - 3 \\cdot 4^x$ ($0 \\leqq x \\leqq 2$) の最大値，最小値とそのときの $x$ の値を求めよ。",
        "$y = 2(4^x + 4^{-x}) - 4(2^x + 2^{-x}) + 3$ の最小値とそのときの $x$ の値を求めよ。（日本大学）",
        "$a$ を定数とし，$y = 9^x + \\frac{1}{9^x} - 4a\\left(3^x + \\frac{1}{3^x}\\right)$ の最小値とそのときの $x$ の値を $a$ を用いてそれぞれ表せ。（大分大学）",
        "$x$ が $\\log_2(x-1) + \\log_{\\frac{1}{2}}(3-x) \\leqq 0$ を満たすとき，$y = 4^x - 6 \\cdot 2^x + 10$ の最大値，最小値とそのときの $x$ の値を求めよ。（センター試験）",
        "$y = 2(\\log_5 x)^2 - \\log_5 x^8 + 6$ ($1 \\leqq x \\leqq 125$) の最大値，最小値とそのときの $x$ の値を求めよ。（鹿児島大学）",
        "$y = (\\log_5 x - 1)(\\log_5 x - 3) \\left(\\frac{1}{25} \\leqq x \\leqq 125\\right)$ の最大値，最小値を求めよ。（甲南大学）",
        "$y = (\\log_2 x)^2 - \\log_2 2x$ ($1 \\leqq x \\leqq 64$) の最大値，最小値を求めよ。（北里大学）",
        "$y = (2 \\log_3 x)^2 + \\log_3 (9x^2) + 1 \\left( \\frac{1}{9} \\leqq x \\leqq 27 \\right)$ の最大値，最小値を求めよ。",
        "$y = \\log_{\\frac{1}{5}}(5-x) - \\frac{1}{2}\\log_{\\sqrt{5}}(x+4)$ ($-1 \\leqq x \\leqq 4$) の最大値，最小値とそのときの $x$ の値を求めよ。",
        "$y = (\\log_2 2x)\\left(\\log_4 \\frac{x}{8}\\right) \\left(\\frac{1}{8} \\leqq x \\leqq 4\\right)$ の最大値，最小値を求めよ。",
        "$y = 1 + \\left(\\log_{10} \\frac{1}{x}\\right)\\left(\\log_{10} \\frac{100}{x}\\right) + \\log_{10} \\frac{1}{x^2}\\left(\\frac{1}{10} \\leqq x \\leqq 1000\\right)$ の最大値，最小値を求めよ。（北海道大学）",
        "$y = \\log_2 x + \\log_4(-2x+1)$ の最大値とそのときの $x$ の値を求めよ。（信州大学）",
        "$f(x) = 4^x + 4^{-x} - a(2^{x+1} + 2^{-x+1}) + 6a + 1$ の最小値が 2 となる $a$ の値を求めよ。（尾道大学）",
        "方程式 $9^x + 9^{-x} - (a+1)(3^x + 3^{-x}) - 2a^2 + 8a - 4 = 0$ が実数解をもつような $a$ の値の範囲を求めよ。（東京理科大学）",
        "$\\log_{10} 2 = 0.3010$ とする。$2^{50}$ の桁数を求めよ。",
        "$\\log_{10} 2 = 0.3010, \\log_{10} 3 = 0.4771$ とする。$6^{200}$ の桁数を求めよ。",
        "$\\log_{10} 2 = 0.3010$ とする。$5^{100}$ の桁数を求めよ。",
        "$\\log_{10} 2 = 0.3010, \\log_{10} 3 = 0.4771, \\log_{10} 7 = 0.8451$ とする。$7^{30}$ の桁数と最高位の数を求めよ。",
        "$\\log_{10} 3 = 0.4771$ とする。$\\left(\\frac{3}{10}\\right)^{40}$ を小数で表すと，小数第何位にはじめて 0 でない数が現れるか。",
        "$(1.2)^n \\geqq 100$ を満たす最小の自然数 $n$ を求めよ。ただし，$\\log_{10} 2 = 0.3010, \\log_{10} 3 = 0.4771$ とする。",
    ],
}


# ---------------------------------------------------------
# PDFプレビュー＆ワンクリック印刷機能（統合型）
# ---------------------------------------------------------
def render_pdf_with_print_button(pdf_bytes: bytes):
    """1つのPDFとして表示し、専用のワンクリック印刷ボタンを配置する"""
    base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            .container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 100%;
            }}
            .print-btn {{
                background-color: #ff4b4b;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                margin-bottom: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: background 0.2s;
            }}
            .print-btn:hover {{
                background-color: #ff2222;
            }}
            embed {{
                width: 100%;
                height: 650px;
                border: 1px solid #ddd;
                border-radius: 6px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <button class="print-btn" onclick="printPDF()">🖨️ このまま印刷する（ワンクリック）</button>
            <embed id="pdfEmbed" src="data:application/pdf;base64,{base64_pdf}" type="application/pdf" />
        </div>

        <script>
            function printPDF() {{
                const embed = document.getElementById('pdfEmbed');
                try {{
                    embed.contentWindow.print();
                }} catch (e) {{
                    const pdfData = "{base64_pdf}";
                    const byteCharacters = atob(pdfData);
                    const byteNumbers = new Array(byteCharacters.length);
                    for (let i = 0; i < byteCharacters.length; i++) {{
                        byteNumbers[i] = byteCharacters.charCodeAt(i);
                    }}
                    const byteArray = new Uint8Array(byteNumbers);
                    const blob = new Blob([byteArray], {{type: 'application/pdf'}});
                    const blobUrl = URL.createObjectURL(blob);
                    const printWindow = window.open(blobUrl, '_blank');
                    if (printWindow) {{
                        printWindow.onload = function() {{
                            printWindow.print();
                        }};
                    }}
                }}
            }}
        </script>
    </body>
    </html>
    """
    st.markdown("### 📄 PDFプレビュー & 印刷")
    components.html(html_code, height=730)


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
st.write("ランダムに問題が選ばれるオリジナル演習プリントを生成できます。")

# サイドバーの設定
st.sidebar.header("プリント設定")
print_title = st.sidebar.text_input("プリントタイトル", "数学演習プリント")

# 辞書のキーから単元の選択肢を自動生成
available_units = list(question_database.keys())
problem_type = st.sidebar.selectbox("単元・テーマの選択", available_units)

# 選択された単元に含まれる問題数に合わせてスライダーの最大値を設定
max_q_count = len(question_database[problem_type])
num_questions = st.sidebar.slider("出力する問題数", 1, max_q_count, min(10, max_q_count))

# プリント生成ボタン
if st.sidebar.button("プリントを生成する"):
    # LaTeXコードの組み立て
    latex_source = f"""
    \\documentclass[11pt,a4paper]{{ltjsarticle}}
    \\usepackage{{amsmath,amssymb,amsthm}}
    \\begin{{document}}
    \\begin{{center}}
        {{\\Large \\textbf{{{print_title}}}}}
    \\end{{center}}
    \\vspace{{1em}}
    \\noindent \\textbf{{単元: {problem_type}}} \\hfill \\textbf{{氏名: \\underline{{\\hspace{{5cm}}}}}}
    \\vspace{{1.5em}}
    \\hrule
    \\vspace{{1em}}
    """

    # 指定された数だけランダムに問題を取り出す
    selected_questions = random.sample(
        question_database[problem_type], num_questions
    )

    for i, q_text in enumerate(selected_questions, start=1):
        latex_source += f"""
        \\noindent \\textbf{{[問題 {i}]}} \\\\
        {q_text}
        \\vspace{{1.5em}}
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
    # 1. 1つのPDFとしてプレビュー表示し、ワンクリック印刷ボタンを配置
    render_pdf_with_print_button(st.session_state["pdf_data"])

    # 2. ダウンロードボタン（バックアップ用）
    st.download_button(
        label="📥 生成されたPDFをダウンロード",
        data=st.session_state["pdf_data"],
        file_name="math_print.pdf",
        mime="application/pdf",
    )
