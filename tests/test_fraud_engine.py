import sys
import os
from datetime import datetime

# Add backend folder to the path so we can import our code
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fraud_engine import FraudEngine


def test_large_amount_is_flagged():
    """A transaction over the threshold should be flagged"""
    engine = FraudEngine()
    result = engine._check_large_amount(5000)
    assert result == True


def test_small_amount_is_not_flagged():
    """A transaction under the threshold should NOT be flagged"""
    engine = FraudEngine()
    result = engine._check_large_amount(50)
    assert result == False


def test_suspicious_hour_is_flagged():
    """A transaction at 3am should be flagged"""
    engine = FraudEngine()
    suspicious_time = datetime(2026, 6, 17, 3, 0, 0)  # 3am
    result = engine._check_suspicious_hours(suspicious_time)
    assert result == True


def test_normal_hour_is_not_flagged():
    """A transaction at 2pm should NOT be flagged"""
    engine = FraudEngine()
    normal_time = datetime(2026, 6, 17, 14, 0, 0)  # 2pm
    result = engine._check_suspicious_hours(normal_time)
    assert result == False


def test_threshold_boundary():
    """Exactly at the threshold should NOT be flagged - only ABOVE it"""
    engine = FraudEngine()
    result = engine._check_large_amount(3000)
    assert result == False