#importing required libraries
import json
import boto3
from botocore.exceptions import ClientError
from rag import query_rag_knowledge_base
from config import AWS_REGION

# Email configuration
VERIFIED_EMAIL = "shannon.liu04@gmail.com"

def is_math_placement_question(email_body):
    keywords = ["math placement", "MAPE", "aleks", "math class", "math eligibility", "placement test", "calculus", "ap calc"]
    return any(word.lower() in email_body.lower() for word in keywords)

def send_ses_email(subject, body):
    """Send email using AWS SES"""
    try:
        ses_client = boto3.client('ses', region_name=AWS_REGION)
        
        response = ses_client.send_email(
            Source=f"Cal Poly Math Placement AI <{VERIFIED_EMAIL}>",
            Destination={'ToAddresses': [VERIFIED_EMAIL]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        
        print(f"📧 SES Message ID: {response['MessageId']}")
        return True
        
    except ClientError as e:
        print(f"❌ SES Error: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

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
            
            # Send email via SES
            student_name = email['from'].split('@')[0].replace('.', ' ').title()
            email_body = f"""Dear {student_name},

Thank you for your math placement inquiry at Cal Poly.

{answer}

I hope this information is helpful. If you have additional questions, please visit our math placement chatbot at https://mathplacement.calpoly.edu

Best regards,
Cal Poly Math Placement Team
Mathematics Department

---
Original question from {email['from']}:
{email['body']}"""
            
            # Send via AWS SES
            if send_ses_email(f"Re: {email['subject']}", email_body):
                print(f"\n✅ EMAIL SENT via SES")
            else:
                print(f"\n❌ EMAIL FAILED to send")
            print("-" * 60)
            
            responses.append({
                "original_email": email,
                "response": email_body
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

