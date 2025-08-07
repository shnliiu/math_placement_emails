#!/usr/bin/env python3
"""
AI Math Placement Agent Demo Runner
Demonstrates email identification and automated responses using AWS Bedrock
"""

from ai_agent import MathPlacementAgent
import json

def run_demo():
    """Execute the complete AI agent demo"""
    print("🤖 AI MATH PLACEMENT AGENT DEMO")
    print("=" * 60)
    print("This demo will:")
    print("1. Load mock emails from mock_emails.json")
    print("2. Identify math placement related emails")
    print("3. Query AWS Bedrock knowledge base for responses")
    print("4. Generate and 'send' email responses")
    print("5. Save all responses to outbox_responses.json")
    print()
    
    # Load mock emails
    try:
        with open('mock_emails.json', 'r') as f:
            emails = json.load(f)
        print(f"📧 Loaded {len(emails)} mock emails")
    except FileNotFoundError:
        print("❌ Error: mock_emails.json not found!")
        return
    
    # Initialize and run the agent
    agent = MathPlacementAgent()
    results = agent.process_emails(emails)
    
    # Display summary
    print("\n📊 FINAL RESULTS:")
    print(f"Total emails processed: {len(emails)}")
    print(f"Math placement emails found: {len(results)}")
    
    if results:
        print("\n📝 Generated Responses:")
        for i, result in enumerate(results, 1):
            original = result['original_email']
            print(f"\n{i}. Response to: {original['from']}")
            print(f"   Subject: {original['subject']}")
            print(f"   Status: {'✅ Sent' if result['sent_successfully'] else '❌ Failed'}")
    
    print(f"\n💾 All responses saved to: outbox_responses.json")
    print("🎉 Demo completed successfully!")

if __name__ == "__main__":
    run_demo()