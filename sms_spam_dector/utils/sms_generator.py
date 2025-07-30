# utils/sms_generator.py
import numpy as np

# Ham and Spam templates (copied from your provided code)
spam_templates = [
    "CONGRATULATIONS! You've won $1000! Click here to claim your prize now!",
    "URGENT: Your account will be suspended. Verify now at: www.fake-link.com",
    "FREE! Get your iPhone 15 now! Limited time offer. Call 555-SMS-NOW",
    "WINNER! You've been selected for a cash prize! Text BACK to claim!",
    "FINAL NOTICE: Your subscription expires today. Renew now or lose access!",
    "HOT SINGLES in your area want to meet you! Click here for free access!",
    "You have inherited $5000 from a distant relative. Contact lawyer now!",
    "LAST CHANCE: 90% off everything! Sale ends tonight. Shop www.deal-steal.com",
    "URGENT: IRS tax refund pending. Verify your details to receive payment!",
    "FREE VIAGRA! No prescription needed. Order now with 50% discount!",
    "CONGRATS! You're pre-approved for a $10,000 loan. Apply now instantly!",
    "YOUR PACKAGE DELAYED: Click to reschedule delivery www.track-package.com",
    "BANK ALERT: Suspicious activity detected. Secure your account immediately!",
    "MEET LOCAL SINGLES TONIGHT! Free membership trial. Text FLIRT to 555-LOVE",
    "BIGGEST SALE OF THE YEAR! Everything must go! Visit www.clearance-sale.com"
]

ham_templates = [
    "Hey, are we still meeting for lunch tomorrow at 1 PM?",
    "Thanks for the meeting today. I'll send the report by Friday.",
    "Can you pick up milk and bread on your way home?",
    "Happy birthday! Hope you have a wonderful day!",
    "The meeting has been moved to 3 PM in Conference Room B.",
    "Just checking in to see how you're doing. Call me when free.",
    "Don't forget about the doctor's appointment tomorrow morning.",
    "The project is due next Monday. Let's review it together.",
    "Thanks for helping me with the presentation. It went great!",
    "Can we reschedule our call to Thursday? Something came up.",
    "The kids are doing well in school. Parent-teacher meeting next week.",
    "I'm running late today, will be home around 7 PM.",
    "Did you see the game last night? Amazing finish!",
    "The groceries will be delivered between 2-4 PM today.",
    "Remember to submit the timesheet by end of day tomorrow."
]

def generate_ham_sms():
    """Generate a realistic ham (normal) SMS message"""
    return np.random.choice(ham_templates)

def generate_spam_sms():
    """Generate a realistic spam SMS message"""
    return np.random.choice(spam_templates)

def generate_random_sms():
    """Generate a random SMS (ham or spam)"""
    all_templates = ham_templates + spam_templates
    return np.random.choice(all_templates)
