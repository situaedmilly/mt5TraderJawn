"""
Journal service helpers
Could include:
- Signal→journal correlation logic
- Performance analytics
- Trade outcome classification
"""
def calculate_trade_metrics(journal_entry) -> dict:
    """
    Calculate performance metrics from a journal entry

    Returns:
        dict: Calculated metrics
    """
    if not journal_entry.taken:
        return {"skipped": True}
    if journal_entry.actual_entry and journal_entry.pnl_amount:
        # Calculate R-multiple, win rate, etc
        return {
            "skipped": False,
            "completed": journal_entry.result_status in ["win", "loss"],
        }
    return {"skipped": False, "completed": False}
