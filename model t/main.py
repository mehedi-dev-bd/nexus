import sys
from dataset import load_jailbreak_dataset
from detector import NLPJailbreakDetector

def main():
    print("=" * 65)
    print("  PROJECT 'BREAKING BAD': NLP LLM JAILBREAK GUARDRAIL SYSTEM  ")
    print("=" * 65)
    
    df = load_jailbreak_dataset()
    guardrail = NLPJailbreakDetector()
    guardrail.fit(df)
    
    print("\n[+] Guardrail model trained successfully.")
    print("[+] System ready to analyze user prompts.\n")
    print("-" * 65)
    print("Type your prompt to evaluate (Type 'exit' or 'quit' to stop):")
    print("-" * 65)

    while True:
        try:
            user_prompt = input("\nEnter Prompt: ").strip()
            
            if user_prompt.lower() in ['exit', 'quit']:
                print("\nShutting down system. Goodbye!")
                break
                
            if not user_prompt:
                print("Warning: Prompt cannot be empty.")
                continue

            is_jailbreak, score, source = guardrail.predict(user_prompt)

            print("\n" + "=" * 50)
            print("PROMPT ANALYSIS RESULT")
            print("=" * 50)
            
            if is_jailbreak:
                print("Status:      ⚠️ BLOCKED")
                print(f"Risk Score:  {score * 100:.1f}%")
                print(f"Detected By: {source}")
                print("\nAdvice: Prompt contains potential jailbreak or bypass triggers.")
            else:
                print("Status:      ✅ ALLOWED")
                print(f"Risk Score:  {score * 100:.1f}%")
                print(f"Detected By: {source}")
                print("\nAdvice: Prompt is safe to process.")
                
            print("=" * 50)

        except KeyboardInterrupt:
            print("\n\nProgram terminated.")
            sys.exit()

if __name__ == "__main__":
    main()