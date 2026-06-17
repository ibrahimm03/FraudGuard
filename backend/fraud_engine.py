from datetime import datetime, timedelta
from database import get_recent_transactions, flag_transaction, create_alert

class FraudEngine:
    """
    The brain of FraudGuard.
    Analyses transactions and flags suspicious activity.
    """

    def __init__(self):
        self.large_amount_threshold = 3000
        self.frequency_limit = 3
        self.frequency_window_minutes = 1
        self.suspicious_hours = range(1, 5)  # 1am to 4am

    def analyse(self, transaction_id, card_number, amount, location, timestamp):
        """
        Main method — runs all fraud checks on a transaction.
        Returns a list of alerts if fraud is detected.
        """
        alerts = []
        transaction_time = datetime.fromisoformat(timestamp)

        # Run each check
        if self._check_large_amount(amount):
            alerts.append({
                'reason': f'Large transaction amount: £{amount}',
                'severity': 'high' if amount > 5000 else 'medium'
            })

        if self._check_high_frequency(card_number, transaction_time):
            alerts.append({
                'reason': 'High frequency of transactions detected',
                'severity': 'high'
            })

        if self._check_suspicious_hours(transaction_time):
            alerts.append({
                'reason': f'Transaction at suspicious hour: {transaction_time.strftime("%H:%M")}',
                'severity': 'low'
            })

        # If any alerts were raised, flag the transaction
        if alerts:
            flag_transaction(transaction_id)
            for alert in alerts:
                create_alert(
                    transaction_id=transaction_id,
                    reason=alert['reason'],
                    severity=alert['severity'],
                    timestamp=datetime.now().isoformat()
                )

        return alerts

    def _check_large_amount(self, amount):
        """Flag transactions over the threshold"""
        return amount > self.large_amount_threshold

    def _check_high_frequency(self, card_number, transaction_time):
        """Flag if too many transactions in a short window"""
        recent = get_recent_transactions(card_number, limit=10)
        window_start = transaction_time - timedelta(minutes=self.frequency_window_minutes)
        recent_count = sum(
            1 for t in recent
            if datetime.fromisoformat(t['timestamp']) > window_start
        )
        return recent_count >= self.frequency_limit

    def _check_suspicious_hours(self, transaction_time):
        """Flag transactions in the early hours"""
        return transaction_time.hour in self.suspicious_hours