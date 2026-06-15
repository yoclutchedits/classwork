from classwork42_groq import generate_response
def get_essay_details():
    print("welcome")
    topic=input("enter a topic you want a essay for").strip()
    essay_type=input("what type of essay are you writing:").strip()
    lengths=['300 words','900 words', '1200 words', '2000 words']
    print ("sellect essay word count")
    for i,l in enumerate(lengths,1): print(f"{i}){l}")
    try:
        lex=int(input("> ").strip()
        length=lengths[lex - 1] if 1 <= lex <= len(lengths) else: "300 words"
    except ValueError:
        length='300 words'
    target_audince=input("target audience:").strip()
    return{"topic": topic,"essay_type":essay_type,"length":length,"target_audince": target_audince}
def generate_essay_responce(details):
    try:
        temp = float(input("Enter temperature (0.1 structured, 0.7 creative): ").strip()
        if not (0.0 <= temp <= 1.0): raise ValueError
    except ValueError:
        print("invalid temp using 0.3")
        temp=0.3
    intro_p = f"Write an introduction for an {details['essay_type']} essay about {details['topic'] on the topic of {details['length']}}"
    intro=generate_response(intro_p, temprature=temp,max_tokens=1024)
    print("generated introduction")
    print(intro)
    print("would you like the body written as a full draft or step by step")
    print("1) full draft \n 2) step by step")
    choice=input("> ").strip()
    if choice =="1":
        body=f"Write an body for an {details['essay_type']} essay about {details['topic'] wish the stance of {deatils['target_audice']}"
        