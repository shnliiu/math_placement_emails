#!/usr/bin/env python3
"""
Console-based AI Math Placement Agent Demo
Shows email processing and responses in terminal
"""

import json
from ai_agent import MathPlacementAgent

def print_email_chain():
    """Display the complete email processing chain in console"""
    
    print("🤖 AI MATH PLACEMENT AGENT - CONSOLE DEMO")
    print("=" * 60)
    
    # Load mock emails
    try:
        with open('mock_emails.json', 'r') as f:
            emails = json.load(f)
    except FileNotFoundError:
        print("❌ Error: mock_emails.json not found!")
        return
    
    agent = MathPlacementAgent()
    
    for i, email in enumerate(emails, 1):
        print(f"\n📧 EMAIL {i}")
        print("-" * 40)
        print(f"FROM: {email['from']}")
        print(f"SUBJECT: {email['subject']}")
        print(f"BODY: {email['body']}")
        
        # Check if math placement email
        if agent.is_math_placement_email(email):
            print("\n✅ IDENTIFIED: Math placement inquiry")
            
            # Generate response
            print("\n🔍 QUERYING KNOWLEDGE BASE...")
            response_content = agent.generate_response(email['body'])
            
            # Compose email response
            email_response = agent.compose_email_response(email, response_content)
            
            print("\n📤 AI GENERATED RESPONSE:")
            print("=" * 40)
            print(f"TO: {email_response['to']}")
            print(f"SUBJECT: {email_response['subject']}")
            print(f"\n{email_response['body']}")
            print("=" * 40)
            
        else:
            print("\n❌ SKIPPED: Not a math placement inquiry")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    print_email_chain()