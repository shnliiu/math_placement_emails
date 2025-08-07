import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rag import query_rag_knowledge_base
from config import AWS_REGION, KNOWLEDGE_BASE_ID

class MathPlacementAgent:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.processed_emails = []
        
    def is_math_placement_email(self, email_content):
        """Identify if email is about math placement"""
        keywords = [
            "math placement", "MAPE", "aleks", "math class", 
            "math eligibility", "placement test", "calculus", 
            "math requirement", "precalculus", "algebra"
        ]
        
        text_to_check = f"{email_content.get('subject', '')} {email_content.get('body', '')}"
        return any(keyword.lower() in text_to_check.lower() for keyword in keywords)
    
    def generate_response(self, email_body):
        """Generate response using AWS Bedrock knowledge base"""
        try:
            response = query_rag_knowledge_base(email_body)
            return response
        except Exception as e:
            return f"I apologize, but I'm having trouble accessing our knowledge base right now. Please contact the Math Department directly for assistance with your math placement question. Error: {str(e)}"
    
    def compose_email_response(self, original_email, response_content):
        """Compose the email response"""
        return {
            "to": original_email["from"],
            "subject": f"Re: {original_email['subject']}",
            "body": f"""Dear Student,

Thank you for your inquiry about math placement at Cal Poly.

{response_content}

For additional questions or immediate assistance, please visit our math placement chatbot on the Cal Poly website: https://mathplacement.calpoly.edu

If you need further help, please don't hesitate to reach out.

Best regards,
Cal Poly Math Placement Assistant
Mathematics Department
California Polytechnic State University

---
This is an automated response. For urgent matters, please contact the Math Department directly.
"""
        }
    
    def send_email(self, email_data, sender_email, sender_password):
        """Send email response (demo version - prints instead of actually sending)"""
        print(f"\n📧 SENDING EMAIL:")
        print(f"TO: {email_data['to']}")
        print(f"SUBJECT: {email_data['subject']}")
        print(f"BODY:\n{email_data['body']}")
        print("-" * 60)
        
        # For actual email sending, uncomment below:
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email_data['to']
            msg['Subject'] = email_data['subject']
            
            msg.attach(MIMEText(email_data['body'], 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
        """
        return True
    
    def process_emails(self, emails, sender_email="math.placement@calpoly.edu", sender_password=""):
        """Process a batch of emails and respond to math placement inquiries"""
        math_placement_count = 0
        
        print("🤖 AI MATH PLACEMENT AGENT STARTING...")
        print("=" * 60)
        
        for email in emails:
            print(f"\n📨 Processing Email ID: {email.get('id', 'N/A')}")
            print(f"FROM: {email['from']}")
            print(f"SUBJECT: {email['subject']}")
            print(f"BODY: {email['body'][:100]}...")
            
            if self.is_math_placement_email(email):
                print("✅ IDENTIFIED: Math placement inquiry")
                math_placement_count += 1
                
                # Generate response using knowledge base
                response_content = self.generate_response(email['body'])
                
                # Compose email response
                email_response = self.compose_email_response(email, response_content)
                
                # Send email (demo version)
                success = self.send_email(email_response, sender_email, sender_password)
                
                # Store processed email
                self.processed_emails.append({
                    "original_email": email,
                    "response": email_response,
                    "sent_successfully": success
                })
                
            else:
                print("❌ SKIPPED: Not a math placement inquiry")
        
        print(f"\n📊 SUMMARY:")
        print(f"Total emails processed: {len(emails)}")
        print(f"Math placement emails identified: {math_placement_count}")
        print(f"Responses sent: {len(self.processed_emails)}")
        
        return self.processed_emails

def demo():
    """Run the AI agent demo"""
    # Load mock emails
    with open('mock_emails.json', 'r') as f:
        emails = json.load(f)
    
    # Create and run the agent
    agent = MathPlacementAgent()
    results = agent.process_emails(emails)
    
    # Save results
    with open('outbox_responses.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Demo completed! Results saved to outbox_responses.json")

if __name__ == "__main__":
    demo()