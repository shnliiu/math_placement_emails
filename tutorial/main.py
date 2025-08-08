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
    import os
    # Use absolute path to tutorial directory
    tutorial_dir = '/Users/shannonliu/Documents/Workspace/tutorial'
    mock_emails_path = os.path.join(tutorial_dir, 'mock_emails.json')
    
    try:
        print(f"📁 Looking for mock emails at: {mock_emails_path}")
        with open(mock_emails_path, 'r') as f:
            emails = json.load(f)
        print(f"✅ Loaded {len(emails)} mock emails")
    except FileNotFoundError:
        print(f"❌ mock_emails.json not found at: {mock_emails_path}")
        print(f"📁 Current directory: {os.getcwd()}")
        print(f"📁 Tutorial directory: {tutorial_dir}")
        return
    except Exception as e:
        print(f"❌ Error loading mock emails: {str(e)}")
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
            personalized_query = f"""You are a helpful and encouraging assistant for Cal Poly's math department. Your tone is nice, friendly, encouraging, welcoming, and warm. Always respond in clear, concise sentences still keeping it formal. Format your response in short, accessible paragraphs with an organized, readable style. No more than 5 sentences per paragraph. Be as helpful as possible and ensure the user does not have to email the math department. Use bullet points, bolding, italics, headers, hyperlinks, and other formatting options to separate text and make it readable. Your priority is to provide students with advice and information about the department and its courses as well as information about math placement. If the user asks about potential math placement, reply with particular courses they are eligible to take using all the information provided. State which specific Cal Poly courses the student is eligible to enroll in (e.g., A score of 5 on the AP Calculus AB exam gives you credit for MATH 141 and allows you to enroll in MATH 142), as well as their next available courses. After clarification, if the question hasn't been answered with complete certainty, tell the user to contact the math department but do not provide any email. Address their specific situation directly: {email['body']}"""
            
            # Query AWS knowledge base with personalized context
            answer = query_rag_knowledge_base(personalized_query)
            
            # Send email via SES
            student_name = email['from'].split('@')[0].replace('.', ' ').title()
            email_body = f"""Dear {student_name},


{answer}

I hope this information is helpful. If you have additional questions, please visit our math placement chatbot at https://math.calpoly.edu/reqs-exams

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

