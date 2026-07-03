from classwork45_groq import generate_response
import streamlit as st
import io
SYSTEM_PROMPT = """You are a Math Mastermind. For every math problem:
1) Show step-by-step solution 2) Explain reasoning 3) Give alternate method if possible
4) Verify answer if possible 5) Use proper notation 6) Break complex problems into parts
Format: Problem → Steps → **Final Answer** → Concepts used. Be precise and educational."""
def export_b(his):
    text = "".join([f"Q{i}: {h['question']}\nA{i}: {h['answer']}\n\n" for i, h in enumerate(his, 1)])
    return io.BytesIO(text.encode('utf-8'))
def math_gen(problem: str, level: list, temperature: float = 0.3, max_tokens: int = 1024) -> str:
    prompt = f"{SYSTEM_PROMPT}\n\nProblem: ({level}) {problem}\n\nAnswer:"
    return generate_response(prompt, temperature=temperature, max_tokens=max_tokens)
def setup_ui():
    st.set_page_config(page_title="Math Problem Solver", page_icon=":abacus:", layout="centered")
    st.title("# Math Problem Solver")
    st.write("Enter a math problem, select the difficulty level, and get a detailed solution.")
    with st.expander("example problems"):
        st.markdown('algebra: Solve for x in the equation 2x + 3 = 7'
                    'calculus: Find the derivative of f(x) = x^2 + 3x + 5'
                    'geometry: Calculate the area of a circle with radius r'
                    'trigonometry: Solve for θ in the equation sin(θ) = 0.5')
        st.session_state.setdefault("history", [])
        st.session_state.setdefault("k", 0)
        c1,c2 = st.columns([1,2])
        if c1.button("Clear History"):
            st.session_state.history = []
            st.session_state.k = 0 
        if st.session_state.history:
            c2.download_button("Export History", data=export_b(st.session_state.history), file_name="history.txt", mime="text/plain")
        with st.form("math_form", clear_on_submit=True):
            q=st.text_area("Enter your math problem here:", placeholder="e.g., Solve for x in the equation 2x + 3 = 7", key=f"q_{st.session_state.k}", height=100)
            a,b=st.columns([3,1])
            solve= a.form_submit_button("Solve",use_container_width=True)
            level = b.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"],index=1)
            if solve:
                if not q.strip():
                    st.warning("Please enter a math problem.")
                else:
                    with st.spinner("Solving..."):
                        answer = math_gen(q, level)
                        st.session_state.history.append({"question": q, "answer": answer})
                        st.session_state.k += 1
                        st.success("Problem solved!")
                        st.rerun()
        if not st.session_state.history:return
        st.markdown("""<style>

.box{max-height:500px;overflow-y:auto;border:2px solid #4CAF50;padding:12px;background:#f7fbff;border-radius:10px}

.q{font-weight:700;color:#2E7D32;margin-top:12px}

.lvl{display:inline-block;background:#FF9800;color:#fff;padding:2px 8px;border-radius:12px;font-size:12px;margin-left:8px}

.a{white-space:pre-wrap;color:#1B5E20;background:#fff;padding:10px;border-radius:8px;border-left:4px solid #4CAF50;margin:6px 0 14px}

</style>""", unsafe_allow_html=True)
        html='<div class="box">'
        for i, h in enumerate(st.session_state.history, 1):
            html+=f'<div class="q">Q{i}: {h["question"]}<span class="lvl">{level}</span></div>'
            html+=f'<div class="a">A{i}: {h["answer"]}</div>'
        st.markdown(html+'</div>', unsafe_allow_html=True)
if __name__ == "__main__":
    setup_ui()