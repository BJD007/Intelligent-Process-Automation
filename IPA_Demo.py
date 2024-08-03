import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import nltk
from nltk.corpus import stopwords
import re
import smtplib
from email.mime.text import MIMEText
import time

# Download necessary NLTK data
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# 1. RPA Component: Simulating ticket extraction
def extract_tickets(file_path):
    # In a real scenario, this would interact with email APIs or web forms
    df = pd.read_csv(file_path)
    return df

# 2. AI/ML Component: Text preprocessing
def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    return ' '.join([word for word in text.split() if word not in stop_words])

# Ticket classification model
class TicketClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = MultinomialNB()

    def train(self, X, y):
        X_processed = [preprocess_text(text) for text in X]
        X_vectorized = self.vectorizer.fit_transform(X_processed)
        self.model.fit(X_vectorized, y)

    def predict(self, X):
        X_processed = [preprocess_text(text) for text in X]
        X_vectorized = self.vectorizer.transform(X_processed)
        return self.model.predict(X_vectorized)

# Initial response generation (simplified)
def generate_initial_response(category):
    responses = {
        'Technical': "Thank you for contacting our technical support. We're looking into your issue.",
        'Billing': "We've received your billing inquiry and will respond shortly.",
        'General': "Thank you for your inquiry. We'll get back to you soon."
    }
    return responses.get(category, "Thank you for contacting us. We'll respond soon.")

# Simulated ticket routing
def route_ticket(ticket_id, category, department_emails):
    # In a real scenario, this would integrate with a ticketing system API
    print(f"Ticket {ticket_id} routed to {category} department: {department_emails[category]}")

# Simulated email sending
def send_email(to_email, subject, body):
    # In a real scenario, replace with actual SMTP server details
    print(f"Email sent to {to_email}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")

# 3. Process Analytics Component
class ProcessAnalytics:
    def __init__(self):
        self.start_time = time.time()
        self.processed_tickets = 0
        self.category_counts = {}

    def update(self, category):
        self.processed_tickets += 1
        self.category_counts[category] = self.category_counts.get(category, 0) + 1

    def get_metrics(self):
        elapsed_time = time.time() - self.start_time
        return {
            "total_processed": self.processed_tickets,
            "average_time": elapsed_time / self.processed_tickets if self.processed_tickets > 0 else 0,
            "category_distribution": self.category_counts
        }

# Main IPA process
def run_ipa_process(data_file, department_emails):
    # Load and prepare data
    df = extract_tickets(data_file)
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['category'], test_size=0.2, random_state=42)

    # Train the model
    classifier = TicketClassifier()
    classifier.train(X_train, y_train)

    # Evaluate the model
    y_pred = classifier.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Process Analytics setup
    analytics = ProcessAnalytics()

    # Process new tickets
    new_tickets = extract_tickets('new_tickets.csv')  # Simulated new tickets
    for _, ticket in new_tickets.iterrows():
        category = classifier.predict([ticket['text']])[0]
        initial_response = generate_initial_response(category)
        
        # Route ticket
        route_ticket(ticket['id'], category, department_emails)
        
        # Send initial response
        send_email(ticket['email'], f"Re: {ticket['subject']}", initial_response)
        
        # Update analytics
        analytics.update(category)

    # Display process analytics
    print("Process Analytics:")
    print(analytics.get_metrics())

# Run the IPA process
department_emails = {
    'Technical': 'tech@example.com',
    'Billing': 'billing@example.com',
    'General': 'support@example.com'
}

run_ipa_process('customer_support_data.csv', department_emails)
