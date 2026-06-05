from classwork40_groq import generate_response
def reinforce_learning():
    print("Reinforcement Learning ")
    p=input("Enter a prompt for the model: ").strip()
    if not p:
        print("Prompt cannot be empty.")
        return
    i_response = generate_response(p, temperature=0.3, max_tokens=1024)
    print("initial response:", i_response)
    try:
        rating = int(input("Rate the response on a scale of 1 to 5: ").strip())
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5.")
            return
    except ValueError:
        print("Invalid rating. Please enter a number between 1 and 5.")
        rating = 3
    feedback = input("Provide feedback to improve the response: ").strip()
    imp_response = f"{i_response}(improved with feedback: {feedback}, rating: {rating})"
    print("Improved response:", imp_response)
    print("reflection questions:")
    print("1) What did you like about the initial response?")
    print("2) What did you dislike about the initial response?")
    print("3) How did the feedback and rating influence the improved response?")
    print("4) What would you do differently next time to get a better response?")
def role_based_prompts():
    print("Role-based Prompts")
    catgory = input("Choose a category (e.g., 'science', 'history', 'technology'): ").strip().lower()
    item = input("Enter a specific item within that category (e.g., 'black holes' for science): ").strip().lower()
    if not catgory or not item:
        print("Category and item cannot be empty.")
        return
    teacher_prompt = f"As a teacher, explain the concept of {item} in the context of {catgory} to a student."
    expert_prompt = f"As an expert in {catgory}, provide a detailed analysis of {item}."
    teacher_response = generate_response(teacher_prompt, temperature=0.3, max_tokens=1024)
    expert_response = generate_response(expert_prompt, temperature=0.3, max_tokens=1024)
    print("Teacher's Response:")
    print(teacher_response)
    print("Expert's Response:")
    print(expert_response)
    print("reflection questions:")
    print("1) How does the teacher's explanation differ from the expert's analysis?")
    print("2) What unique insights does each perspective provide?")
    print("3) Which response is more helpful for a student's understanding?")
    print("4) How can the responses be combined to create a more comprehensive explanation?")
def main():
    print("Welcome to the AI Learning and Role-based Prompting Exercise!")
    print("Choose an exercise:")
    print("1) Reinforcement Learning")
    print("2) Role-based Prompts")
    choice = input("Enter the number of your choice: ").strip()
    if choice == '1':
        reinforce_learning()
    elif choice == '2':
        role_based_prompts()
    else:
        print("Invalid choice. Please enter 1 or 2.")
if __name__ == "__main__":
    main()