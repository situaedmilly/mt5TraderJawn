"""init core tables"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_init_core_tables"
down_revision = None
branch_labels = None
depends_on = None


def guid_type():
    return postgresql.UUID(as_uuid=True)


def json_type():
    return sa.JSON()


def upgrade() -> None:
    op.create_table(
        "symbols",
        sa.Column("id", guid_type(), primary_key=True, nullable=False),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("display_name", sa.String(length=64), nullable=False),
        sa.Column("asset_class", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_symbols_symbol", "symbols", ["symbol"], unique=True)

    op.create_table(
        "strategies",
        sa.Column("id", guid_type(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("phase", sa.String(length=16), nullable=False),
        sa.Column("timeframe_bias", sa.String(length=16), nullable=False),
        sa.Column("timeframe_entry", sa.String(length=16), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_strategies_name", "strategies", ["name"], unique=True)
    op.create_index("ix_strategies_code", "strategies", ["code"], unique=True)

    op.create_table(
        "signals",
        sa.Column("id", guid_type(), primary_key=True, nullable=False),
        sa.Column("strategy_id", guid_type(), sa.ForeignKey("strategies.id"), nullable=False),
        sa.Column("symbol_id", guid_type(), sa.ForeignKey("symbols.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("signal_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("session_name", sa.String(length=32), nullable=False),
        sa.Column("direction", sa.String(length=8), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("priority_score", sa.Numeric(8, 2), nullable=False),
        sa.Column("confidence_band", sa.String(length=4), nullable=False),
        sa.Column("htf_bias", sa.String(length=16), nullable=False),
        sa.Column("entry_tf", sa.String(length=16), nullable=False),
        sa.Column("entry_zone_low", sa.Numeric(18, 6), nullable=False),
        sa.Column("entry_zone_high", sa.Numeric(18, 6), nullable=False),
        sa.Column("stop_price", sa.Numeric(18, 6), nullable=False),
        sa.Column("target_1", sa.Numeric(18, 6), nullable=False),
        sa.Column("target_2", sa.Numeric(18, 6), nullable=True),
        sa.Column("expiry_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reason_code", sa.String(length=64), nullable=False),
        sa.Column("reason_text", sa.Text(), nullable=False),
        sa.Column("json_context", json_type(), nullable=False),
    )
    op.create_index("ix_signals_status", "signals", ["status"], unique=False)

    op.create_table(
        "manual_trade_journal",
        sa.Column("id", guid_type(), primary_key=True, nullable=False),
        sa.Column("signal_id", guid_type(), sa.ForeignKey("signals.id"), nullable=False),
        sa.Column("taken", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("mt5_ticket", sa.String(length=64), nullable=True),
        sa.Column("actual_entry", sa.Numeric(18, 6), nullable=True),
        sa.Column("actual_stop", sa.Numeric(18, 6), nullable=True),
        sa.Column("actual_target", sa.Numeric(18, 6), nullable=True),
        sa.Column("lot_size", sa.Numeric(12, 4), nullable=True),
        sa.Column("risk_percent", sa.Numeric(8, 4), nullable=True),
        sa.Column("result_status", sa.String(length=16), nullable=False),
        sa.Column("pnl_amount", sa.Numeric(18, 2), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_manual_trade_journal_signal_id", "manual_trade_journal", ["signal_id"], unique=False)

    op.create_table(
        "trade_proposals",
        sa.Column("id", guid_type(), primary_key=True, nullable=False),
        sa.Column("signal_id", guid_type(), sa.ForeignKey("signals.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("proposal_status", sa.String(length=16), nullable=False),
        sa.Column("order_type", sa.String(length=16), nullable=False),
        sa.Column("proposed_entry", sa.Numeric(18, 6), nullable=False),
        sa.Column("proposed_stop", sa.Numeric(18, 6), nullable=False),
        sa.Column("proposed_tp1", sa.Numeric(18, 6), nullable=False),
        sa.Column("lot_size", sa.Numeric(12, 4), nullable=False),
        sa.Column("risk_percent", sa.Numeric(8, 4), nullable=False),
        sa.Column("expected_rr", sa.Numeric(8, 4), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("policy_check_passed", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("safety_check_passed", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_trade_proposals_signal_id", "trade_proposals", ["signal_id"], unique=False)
    op.create_index("ix_trade_proposals_proposal_status", "trade_proposals", ["proposal_status"], unique=False)

    op.create_table(
        "proposal_reviews",
        sa.Column("id", guid_type(), primary_key=True, nullable=False),
        sa.Column("proposal_id", guid_type(), sa.ForeignKey("trade_proposals.id"), nullable=False),
        sa.Column("decision", sa.String(length=16), nullable=False),
        sa.Column("decision_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("review_note", sa.Text(), nullable=True),
    )
    op.create_index("ix_proposal_reviews_proposal_id", "proposal_reviews", ["proposal_id"], unique=False)

    op.create_table(
        "heartbeats",
        sa.Column("id", guid_type(), primary_key=True, nullable=False),
        sa.Column("service_name", sa.String(length=64), nullable=False),
        sa.Column("instance_name", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("heartbeat_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("message", sa.String(length=255), nullable=True),
        sa.Column("json_metrics", json_type(), nullable=False),
    )
    op.create_index("ix_heartbeats_service_name", "heartbeats", ["service_name"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_heartbeats_service_name", table_name="heartbeats")
    op.drop_table("heartbeats")
    op.drop_index("ix_proposal_reviews_proposal_id", table_name="proposal_reviews")
    op.drop_table("proposal_reviews")
    op.drop_index("ix_trade_proposals_proposal_status", table_name="trade_proposals")
    op.drop_index("ix_trade_proposals_signal_id", table_name="trade_proposals")
    op.drop_table("trade_proposals")
    op.drop_index("ix_manual_trade_journal_signal_id", table_name="manual_trade_journal")
    op.drop_table("manual_trade_journal")
    op.drop_index("ix_signals_status", table_name="signals")
    op.drop_table("signals")
    op.drop_index("ix_strategies_code", table_name="strategies")
    op.drop_index("ix_strategies_name", table_name="strategies")
    op.drop_table("strategies")
    op.drop_index("ix_symbols_symbol", table_name="symbols")
    op.drop_table("symbols")
