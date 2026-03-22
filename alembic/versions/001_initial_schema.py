"""initial schema
Revision ID: 001
Revises: 
Create Date: 2025-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = '001'
down_revision = None
branch_labels = None
depends_on = None
def upgrade() -> None:
    # Symbol table
    op.create_table(
        'symbols',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('symbol', sa.String(20), nullable=False, unique=True, index=True),
        sa.Column('display_name', sa.String(100), nullable=False),
        sa.Column('asset_class', sa.String(20), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    # Strategy table
    op.create_table(
        'strategies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('code', sa.String(50), nullable=False, unique=True, index=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('phase', sa.String(20), nullable=False),
        sa.Column('timeframe_bias', sa.String(10), nullable=True),
        sa.Column('timeframe_entry', sa.String(10), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    # Signal table
    op.create_table(
        'signals',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('strategy_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('symbol_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('signal_time', sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column('session_name', sa.String(20), nullable=True),
        sa.Column('direction', sa.String(10), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, default='active', index=True),
        sa.Column('priority_score', sa.Float(), nullable=True),
        sa.Column('confidence_band', sa.String(10), nullable=True),
        sa.Column('htf_bias', sa.String(10), nullable=True),
        sa.Column('entry_tf', sa.String(10), nullable=True),
        sa.Column('entry_zone_low', sa.Numeric(12, 5), nullable=True),
        sa.Column('entry_zone_high', sa.Numeric(12, 5), nullable=True),
        sa.Column('stop_price', sa.Numeric(12, 5), nullable=True),
        sa.Column('target_1', sa.Numeric(12, 5), nullable=True),
        sa.Column('target_2', sa.Numeric(12, 5), nullable=True),
        sa.Column('expiry_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('reason_code', sa.String(50), nullable=True),
        sa.Column('reason_text', sa.Text(), nullable=True),
        sa.Column('json_context', postgresql.JSONB(), nullable=True),
        sa.ForeignKeyConstraint(['strategy_id'], ['strategies.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['symbol_id'], ['symbols.id'], ondelete='CASCADE'),
    )
    # ManualTradeJournal table
    op.create_table(
        'manual_trade_journals',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('signal_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('taken', sa.Boolean(), nullable=False),
        sa.Column('mt5_ticket', sa.String(50), nullable=True),
        sa.Column('actual_entry', sa.Numeric(12, 5), nullable=True),
        sa.Column('actual_stop', sa.Numeric(12, 5), nullable=True),
        sa.Column('actual_target', sa.Numeric(12, 5), nullable=True),
        sa.Column('lot_size', sa.Numeric(8, 2), nullable=True),
        sa.Column('risk_percent', sa.Numeric(5, 2), nullable=True),
        sa.Column('result_status', sa.String(20), nullable=True),
        sa.Column('pnl_amount', sa.Numeric(12, 2), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['signal_id'], ['signals.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_manual_trade_journals_signal_id', 'manual_trade_journals', ['signal_id'])
    # TradeProposal table
    op.create_table(
        'trade_proposals',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('signal_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('proposal_status', sa.String(20), nullable=False, default='pending', index=True),
        sa.Column('order_type', sa.String(20), nullable=False),
        sa.Column('proposed_entry', sa.Numeric(12, 5), nullable=False),
        sa.Column('proposed_stop', sa.Numeric(12, 5), nullable=False),
        sa.Column('proposed_tp1', sa.Numeric(12, 5), nullable=True),
        sa.Column('lot_size', sa.Numeric(8, 2), nullable=False),
        sa.Column('risk_percent', sa.Numeric(5, 2), nullable=False),
        sa.Column('expected_rr', sa.Numeric(5, 2), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('policy_check_passed', sa.Boolean(), nullable=False, default=True),
        sa.Column('safety_check_passed', sa.Boolean(), nullable=False, default=True),
        sa.ForeignKeyConstraint(['signal_id'], ['signals.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_trade_proposals_signal_id', 'trade_proposals', ['signal_id'])
    # ProposalReview table
    op.create_table(
        'proposal_reviews',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('proposal_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('decision', sa.String(20), nullable=False),
        sa.Column('decision_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('review_note', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['proposal_id'], ['trade_proposals.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_proposal_reviews_proposal_id', 'proposal_reviews', ['proposal_id'])
    # Heartbeat table
    op.create_table(
        'heartbeats',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('service_name', sa.String(50), nullable=False, index=True),
        sa.Column('instance_name', sa.String(100), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('heartbeat_at', sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('json_metrics', postgresql.JSONB(), nullable=True),
    )
def downgrade() -> None:
    op.drop_table('proposal_reviews')
    op.drop_table('trade_proposals')
    op.drop_table('manual_trade_journals')
    op.drop_table('signals')
    op.drop_table('strategies')
    op.drop_table('symbols')
    op.drop_table('heartbeats')
