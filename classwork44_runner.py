from classwork44_groq import generate_response
import re
import streamlit as st
import io

css="""
<style>

.history-wrap {max-height: 420px; overflow-y: auto; padding-right: 6px;}

.qa-card{

border: 1px solid #e6e6e6;

background: #ffffff;

border-radius: 10px;

padding: 14px 16px;

margin: 10px 0;

box-shadow: 0 1px 2px rgba(0,0,0,0.04);

}

.q{font-weight: 700; color: #0a6ebd; margin-bottom: 8px;}

.a{white-space: pre-wrap; color: #333; line-height: 1.5;}

</style>"""
def export_b(his):
    text="".join([f"Q{i}: {h['question']}\nA{i}: {h['answer']}\n\n" for i,h in enumerate(his,1)])
    return io.BytesIO(text.encode('utf-8'))
def setup_ui():
    st.set_page_config(page_title="ai teaching assistant",layout="centered")
    st.title("ai teching assitant")
    st.write("ask anything!")
    st.session_state.setdefault("history",[])
    col_cle,col_exp=st.columns([1,2])
    with col_cle:
        if st.button("clear conversation"):
            st.session_state.history=[]
            st.rerun()
    with col_exp:
        if st.session_state.history:
            st.download_button(label="export chat history",data=export_b(st.session_state.history),file_name="conversation.txt",mime="text/plain")
    u=st.text_input("enter your question:")
    if st.button("ask"):
        q=u.strip()
        if q:
            with st.spinner("generating responce..."):
                a=generate_response(q)
            st.session_state.history.insert(0,{"question":q,"answer":a})
            st.rerun()
        else:
            st.warning("type a question")
    st.markdown("history")
    st.markdown(css,unsafe_allow_html=True)
    cords=[]
    for i,h in enumerate(st.session_state.history,1):
        cords.append(f'<div class="qa-card"><div class="q"> Q{i}: {h["question"]}</div> <div class="a"> {h["answer"]}</div></div>')
    st.markdown('<div class="history-wrap">' + "".join(cords) + "</div>",unsafe_allow_html=True)
if __name__ == "__main__":
    setup_ui()