from classwork43_groq import generate_response
import re
import streamlit as st
def looks_incompleate(text:str)->bool:
    if not text or len(text.strip()) < 10:
        return True
    t=text.strip()
    if t.endswith(('.', '!', '?', ':', ';', '...', '"', "'")):
        return True
    if re.search(r'\d+\.\s*\*\*$', t):
        return True
    if re.search(r'[.!?]\s*$', t):
        return True
    return False
def complete_response(question:str,max_retries=3)->str:
    base_prompt=f"answer the question in a detailed way: {question}"
    answer=generate_response(base_prompt, temperature=0.3, max_tokens=1024)
    retries=0
    while retries < max_retries and looks_incompleate(answer):
        continue_prompt=f"the previous answer seems incompleate, please complete it: {answer},question: {question}"
        more_answer=generate_response(continue_prompt, temperature=0.3, max_tokens=1024)
        if not more_answer or more_answer.strip() in answer:
            retries+=1
    return answer
def main():
    st.title("AI Teaching Assistant")
    st.write("welcome to the AI Teaching Assistant! ask any question and get a detailed answer.")
    user_question=st.text_input("Enter your question:")
    if user_question:
        with st.spinner("Generating answer..."):
            response=complete_response(user_question)
        st.write("Answer:")
        st.markdown(response)
    else:
        st.info("Please enter a question to get started.")
if __name__ == "__main__":
    main()