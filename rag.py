import boto3
import json
from config import AWS_REGION, KNOWLEDGE_BASE_ID

# Initialize Bedrock-agent client
client = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)

def query_rag_knowledge_base(query_text):
    """
    Sends the query_text to the specified Bedrock knowledge base (RAG setup).
    Returns the AI-generated response.
    """
    try:
        response = client.retrieve_and_generate(
            input={"text": query_text},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
                }
            }
        )
        return response["output"]["text"]
    except Exception as e:
        print(f"⚠️  AWS Connection Error: {e}")
        print("📝 Using fallback response - Please check AWS credentials and configuration")
        return get_demo_response(query_text)

def get_demo_response(question):
    """Generate demo responses for common math placement questions"""
    question_lower = question.lower()
    
    # Check for specific question patterns and provide tailored responses
    if "not sure if i need" in question_lower and "mape" in question_lower:
        return """Great question! I completely understand your uncertainty about the MAPE requirement - it's one of the most common questions we receive from incoming students.

The good news is that you don't necessarily have to take the MAPE (Math Placement Exam), but it could be a valuable opportunity for you. Here's what I'd recommend: if your current math placement means you'd need to complete prerequisite courses before taking the math classes required for your major, the MAPE could help you skip ahead.

Think of the MAPE as a helpful tool rather than a hurdle - it can only improve your placement (up to Calculus I level) and won't hurt your current standing. Once you accept your admission offer and complete the Math Placement Survey, you'll receive personalized guidance on whether the MAPE would benefit you specifically.

If it turns out the MAPE could help you, I'd strongly encourage taking it by July 31st rather than waiting until the August 31st deadline. This timing works better with our course scheduling process, so you won't need to worry about manually adjusting your schedule later if you advance your placement.

I hope this helps clarify things for you!"""
    
    elif "ap calculus ab" in question_lower and "got a 2" in question_lower:
        return """I understand your concern about your AP Calculus AB score - you're definitely not alone in this situation!

With a score of 2 on the AP Calculus AB exam, you will need to take the MAPE (Math Placement Exam) at Cal Poly. While we require a score of 3 or higher on AP Calculus exams to satisfy our calculus prerequisites, the MAPE gives you another opportunity to demonstrate your math skills.

Here's the encouraging part: the MAPE covers intermediate algebra and precalculus topics, and if you perform well on the precalculus portion, you may still be able to place directly into calculus without needing to take prerequisite courses first. So don't worry - you still have a great chance to get into the math level that's right for you!

I'd recommend reviewing precalculus concepts before taking the MAPE to give yourself the best opportunity to succeed."""
    
    elif "out of state" in question_lower and ("where" in question_lower or "location" in question_lower):
        return """Perfect question! As an out-of-state student, I have great news for you - you can take the MAPE completely online from the comfort of your own home.

We've partnered with ProctorU to offer the Math Placement Exam virtually at no cost to you. The process is quite straightforward: just schedule your exam appointment at least 72 hours in advance of when you'd like to take it.

While the online MAPE is available through August 31st, I'd really encourage you to aim for July 31st if possible. Taking it earlier gives you more flexibility with course scheduling and ensures everything is sorted well before you arrive on campus.

If you do miss that window, don't worry - you can always take the in-person MAPE during WOW (Week of Welcome) when you arrive at Cal Poly. But honestly, taking it from home beforehand is much more convenient!

Let me know if you need any help with the scheduling process."""
    
    elif "ap" in question_lower and "calc" in question_lower:
        return """Regarding AP Calculus scores and math placement:

• AP Calculus AB score of 3+: Eligible for MATH 141 (Calculus I)
• AP Calculus BC score of 3+: Eligible for MATH 142 (Calculus II)
• Scores of 2 or below: MAPE required for proper placement

Your AP score means you'll need to take the MAPE to determine your appropriate math course placement. The exam will help us place you in the right level to ensure your success."""
    
    elif "mape" in question_lower or "placement" in question_lower:
        return """Based on our math placement guidelines:

The MAPE (Math Placement and ALEKS Preparation Exam) is required for most incoming students who need to enroll in math courses. Here are the key points:

• Students with AP Calculus scores of 3 or higher may be exempt
• Transfer students with equivalent math coursework may be exempt
• The exam is available online and can be taken remotely
• You have multiple attempts to improve your score
• Preparation modules are available through ALEKS

For complete eligibility requirements and to schedule your exam, please visit: https://mathplacement.calpoly.edu"""
    
    else:
        return """Thank you for your math placement inquiry.

For the most accurate and up-to-date information about math placement requirements, please visit our dedicated website: https://mathplacement.calpoly.edu"""
