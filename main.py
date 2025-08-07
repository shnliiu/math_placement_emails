import json
from rag import query_rag_knowledge_base

def is_math_placement_question(email_body):
    keywords = ["math placement", "MAPE", "aleks", "math class", "math eligibility", "placement test", "calculus", "ap calc"]
    return any(word.lower() in email_body.lower() for word in keywords)

def compose_personalized_email(to_address, subject, body, student_question):
    # Extract student name from email address
    student_name = to_address.split('@')[0].replace('.', ' ').title()
    greeting = f"Dear {student_name}," if student_name else "Dear Student,"
    
    return f"""
TO: {to_address}
SUBJECT: Re: {subject}
BODY:
{greeting}

I hope this message finds you well! Thank you for reaching out to us regarding your math placement at Cal Poly. I'm happy to help clarify this for you.

{body}

I hope this information is helpful in guiding your next steps. Should you have any additional questions or need further clarification, please feel free to visit our math placement chatbot at https://mathplacement.calpoly.edu for immediate assistance.

We're here to support you in your academic journey at Cal Poly, so please don't hesitate to reach out if you need anything else.

Warm regards,
Cal Poly Math Placement Team
Mathematics Department
California Polytechnic State University

---
This is an automated response designed to provide you with immediate assistance. For urgent matters, please contact the Math Department directly.
"""

def main():
    print("🚀 Starting AI Math Placement Agent Demo")
    print("=" * 50)
    print("🤖 AI MATH PLACEMENT AGENT STARTING...")
    print("=" * 60)
    
    # Load emails
    try:
        with open('mock_emails.json', 'r') as f:
            emails = json.load(f)
    except FileNotFoundError:
        print("❌ mock_emails.json not found!")
        return
    
    responses = []
    
    for email in emails:
        print(f"\n📨 Processing Email ID: {email.get('id', 'unknown')}")
        print(f"FROM: {email['from']}")
        print(f"SUBJECT: {email['subject']}")
        print(f"BODY: {email['body']}...")
        
        if is_math_placement_question(email['body']):
            print("✅ IDENTIFIED: Math placement inquiry")
            
            # Create personalized query for the knowledge base
            personalized_query = f"Please provide a warm, friendly, yet professional response to this student's math placement question. Use a conversational tone that is helpful and encouraging. Address their specific situation directly: {email['body']}"
            
            # Query AWS knowledge base with personalized context
            answer = query_rag_knowledge_base(personalized_query)
            
            # Compose personalized email response
            reply = compose_personalized_email(email['from'], email['subject'], answer, email['body'])
            
            print(f"\n📧 SENDING EMAIL:")
            print(reply)
            print("-" * 60)
            
            responses.append({
                "original_email": email,
                "response": reply
            })
        else:
            print("❌ SKIPPED: Not a math placement inquiry")
    
    # Save responses
    with open('outbox_responses.json', 'w') as f:
        json.dump(responses, f, indent=2)
    
    print(f"\n📊 SUMMARY:")
    print(f"Total emails processed: {len(emails)}")
    print(f"Math placement emails identified: {len(responses)}")
    print(f"Responses sent: {len(responses)}")
    print(f"\n✅ Demo completed! Check outbox_responses.json for all responses.")

if __name__ == "__main__":
    main()
