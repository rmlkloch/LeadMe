class NotificationService:
    def __init__(self):
        pass

    def notify_staff_of_ticket(self, ticket_id: int, client_id: str, question: str, email: str):
        """
        Simulates sending a webhook or email to staff for $0 prototype.
        """
        print("================ ALERT ==================")
        print(f"NEW SUPPORT TICKET #{ticket_id}")
        print(f"Client: {client_id}")
        print(f"User Email: {email}")
        print(f"Question: {question}")
        print("=========================================")

    def notify_lead_of_resolution(self, email: str, answer: str):
        """
        Simulates sending a resolution email back to the lead.
        """
        print(f"Simulated Email sent to Lead ({email}): {answer}")

notification_service = NotificationService()
