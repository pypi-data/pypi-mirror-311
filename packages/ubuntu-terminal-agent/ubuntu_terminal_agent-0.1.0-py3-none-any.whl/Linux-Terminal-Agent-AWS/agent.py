import os
from huggingface_hub import InferenceClient

client = InferenceClient(api_key="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")

def get_command_from_prompt(prompt):
    try:
        messages = [
            {"role": "user", "content": f"Generate only the terminal command for: {prompt}. Do not include any extra text."}
        ]
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=messages,
            max_tokens=100  
        )
        command = completion.choices[0].message["content"].strip()
        return command
    except Exception as e:
        print("Error in generating command:", e)
        return None

def execute_command(command):
    try:
        print(f"\nExecuting Command: {command}")
        os.system(command)
    except Exception as e:
        print("Error in executing command:", e)

def main():
    print("Ubuntu Terminal Agent By Agents Valley : Just tell what you want to do and our Agent Will Generate and Execute Commands For You. ")
    while True:
        user_input = input("\nEnter your prompt (or type 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        command = get_command_from_prompt(user_input)
        if command:
            print(f"\nGenerated Command: {command}")
            confirmation = input("Do you want to execute this command? (y/n): ").strip().lower()
            if confirmation == "y":
                execute_command(command)
            else:
                print("Command execution cancelled.")

if __name__ == "__main__":
    main()
