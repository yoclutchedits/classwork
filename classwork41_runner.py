from classwork41_groq import generate_response
def bias_mitigation():
    print("welcome to bias mitigation")
    prompt = input("enter a prompt to test for bias: ")
    if not prompt:
        print("no prompt entered,enter a prompt to test for bias")
        return
    i_r=generate_response(prompt, temperature=0.3, max_tokens=1024)
    print("initial response:")
    print(i_r)
    m_prompt = input("enter a prompt to make it more nuetral: ")
    if  m_prompt:
        m_r=generate_response(m_prompt, temperature=0.3, max_tokens=1024)
        print("mitigated response:")
        print(m_r)
    else:
        print("no prompt entered,skipping mitigation")
def token_limitations_activity():
    print("welcome to token limitations activity")
    prompt = input("enter a long prompt: ")
    if prompt:
        l_r=generate_response(prompt, temperature=0.3, max_tokens=1024)
        preview = (l_r[:500] + '...') if len(l_r) > 500 else l_r
        print("response (truncated to 500 characters):")
        print(preview)
    else:
        print("no prompt entered,skipping token limitations activity")
    s_prompt = input("enter a short prompt: ")
    if s_prompt:
        s_r=generate_response(s_prompt, temperature=0.3, max_tokens=1024)
        print("response:")
        print(s_r)
    else:
        print("no prompt entered,skipping short prompt activity")
def main():
    print("welcome to the classwork 41 activities")
    while True:
        print("\nselect an activity:")
        print("1) bias mitigation")
        print("2) token limitations")
        print("3) exit")
        choice = input("enter your choice (1/2/3): ")
        if choice == "1":
            bias_mitigation()
        elif choice == "2":
            token_limitations_activity()
        elif choice == "3":
            print("exiting the activities. goodbye!")
            break
        else:
            print("invalid choice, please enter 1, 2, or 3.")
if __name__ == "__main__":
    main()