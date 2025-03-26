from kernel import process_input
from llm import call_llm

def main():
    print("🧠 cidafm is running. Type exit to quit.")
    
    # Init memory
    context = []
    active_afms = set()

    while True:
        user_input = input("👤> ").strip()

        if user_input.lower() == "exit":
            print("👋 Goodbye.")
            break

        # Process AFMs, Commands, or Normal Input
        response, context, active_afms = process_input(user_input, context, active_afms)
        
        if isinstance(response["user_input"], str) and (
            response["user_input"].startswith("CID imported:") or 
            response["user_input"].startswith("[cidafm]")
        ):
            print(response)
            continue
        
        # Call LLM with wrapped prompt
        output = call_llm(response)
        
        print(f"🤖> {output}\n")

if __name__ == "__main__":
    main()