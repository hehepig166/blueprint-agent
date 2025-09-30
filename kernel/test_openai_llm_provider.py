"""
Test script for OpenAIProvider
"""

import os
from llm_providers import OpenAIProvider


def test_openai_provider():
    """Test OpenAIProvider with user input for API key and base URL."""
    
    print("=== OpenAIProvider Test ===")
    
    # Get API key from user input
    api_key = input("Enter your OpenAI API key (or press Enter to use OPENAI_API_KEY env var): ").strip()
    if not api_key:
        api_key = None  # Will use environment variable
    
    # Get base URL from user input (optional)
    base_url = input("Enter OpenAI base URL (optional, press Enter for default): ").strip()
    if not base_url:
        base_url = None
    
    try:
        # Initialize provider
        print("\nInitializing OpenAIProvider...")
        provider = OpenAIProvider(api_key=api_key, model="gpt-4o-mini")
        
        # Set custom base URL if provided
        if base_url:
            provider.client.base_url = base_url
            print(f"Using custom base URL: {base_url}")
        
        print("✓ Provider initialized successfully")
        
        # Test 1: Single message generation
        print("\n--- Test 1: Single message generation ---")
        response1 = provider.generate_content("Hello! Please respond with 'Hi there!' and nothing else.")
        print(f"Response: {response1}")
        
        # Test 2: Chat session
        print("\n--- Test 2: Chat session ---")
        provider.reset_chat("You are a helpful assistant. Keep responses brief.")
        
        response2 = provider.send_message("What's 2+2?")
        print(f"First message response: {response2}")
        
        response3 = provider.send_message("What about 3+3?")
        print(f"Second message response: {response3}")

        response4 = provider.send_message("What is the previous response?")
        print(f"Third message response: {response4}")
        
        # Test 3: Full response object
        print("\n--- Test 3: Full response object ---")
        full_response = provider.generate_content("Count from 1 to 3", return_full_response=True)
        print(f"Full response type: {type(full_response)}")
        print(f"Usage info: {full_response.usage}")
        
        # Test 4: File upload (if file exists)
        print("\n--- Test 4: File upload ---")
        test_file = "test_file.txt"
        try:
            # Create a test file
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("This is a test file for OpenAI upload.")
            
            file_obj = provider.upload_file(test_file)
            print(f"File uploaded: {file_obj}")
            
            # Clean up
            os.remove(test_file)
            print("Test file cleaned up")
            
        except Exception as e:
            print(f"File upload test failed: {e}")
        
        print("\n✓ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
    
    return True


def interactive_chat():
    """Interactive chat session with OpenAIProvider."""
    
    print("\n=== Interactive Chat ===")
    print("Type 'quit' to exit, 'reset' to reset chat, 'system <prompt>' to set system prompt")
    
    # Get API key
    api_key = input("Enter your OpenAI API key (or press Enter to use OPENAI_API_KEY env var): ").strip()
    if not api_key:
        api_key = None
    
    try:
        provider = OpenAIProvider(api_key=api_key, model="gpt-4o-mini")
        print("Chat started! Type your messages below:")
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'reset':
                provider.reset_chat()
                print("Chat reset!")
                continue
            elif user_input.startswith('system '):
                system_prompt = user_input[7:].strip()
                provider.reset_chat(system_prompt)
                print(f"System prompt set: {system_prompt}")
                continue
            elif not user_input:
                continue
            
            try:
                response = provider.send_message(user_input)
                print(f"Assistant: {response}")
            except Exception as e:
                print(f"Error: {e}")
                
    except Exception as e:
        print(f"Failed to initialize provider: {e}")


if __name__ == "__main__":
    print("OpenAIProvider Test Script")
    print("1. Run basic tests")
    print("2. Interactive chat")
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        test_openai_provider()
    elif choice == "2":
        interactive_chat()
    else:
        print("Invalid choice. Running basic tests...")
        test_openai_provider()
