from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '202510041200_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table('accounts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('access_token', sa.Text(), nullable=True),
        sa.Column('refresh_token', sa.Text(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('imap_host', sa.String(length=255), nullable=True),
        sa.Column('imap_port', sa.Integer(), nullable=True),
        sa.Column('smtp_host', sa.String(length=255), nullable=True),
        sa.Column('smtp_port', sa.Integer(), nullable=True),
        sa.Column('oauth_type', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )

    op.create_table('threads',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('account_id', sa.Integer(), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('subject', sa.Text(), nullable=True),
        sa.Column('last_message_at', sa.DateTime(), nullable=True),
        sa.Column('participants', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('unread_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('folder', sa.String(length=100), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True)
    )

    op.create_table('messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('account_id', sa.Integer(), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('remote_id', sa.String(length=255), nullable=True),
        sa.Column('thread_id', sa.Integer(), sa.ForeignKey('threads.id', ondelete='SET NULL'), nullable=True),
        sa.Column('subject', sa.Text(), nullable=True),
        sa.Column('from_addr', sa.Text(), nullable=True),
        sa.Column('to_addrs', sa.Text(), nullable=True),
        sa.Column('cc_addrs', sa.Text(), nullable=True),
        sa.Column('bcc_addrs', sa.Text(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.Column('snippet', sa.Text(), nullable=True),
        sa.Column('body_html', sa.Text(), nullable=True),
        sa.Column('body_text', sa.Text(), nullable=True),
        sa.Column('flags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('size', sa.Integer(), nullable=True),
        sa.Column('has_attachments', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('folder', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )

    # Generated tsvector column (Postgres 12+)
    op.execute(
        """
        ALTER TABLE messages
        ADD COLUMN indexed_tsvector tsvector GENERATED ALWAYS AS (
            setweight(to_tsvector('simple', coalesce(subject, '')), 'A') ||
            setweight(to_tsvector('simple', coalesce(body_text, '')), 'B') ||
            setweight(to_tsvector('simple', coalesce(from_addr, '')), 'C') ||
            setweight(to_tsvector('simple', coalesce(to_addrs, '')), 'C')
        ) STORED;
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_messages_fts ON messages USING GIN (indexed_tsvector);")

    op.create_table('attachments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('message_id', sa.Integer(), sa.ForeignKey('messages.id', ondelete='CASCADE'), nullable=False),
        sa.Column('filename', sa.Text(), nullable=False),
        sa.Column('mime', sa.String(length=255), nullable=True),
        sa.Column('size', sa.Integer(), nullable=True),
        sa.Column('s3_key', sa.Text(), nullable=False)
    )

    op.create_table('notes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('thread_id', sa.Integer(), sa.ForeignKey('threads.id', ondelete='CASCADE'), nullable=False),
        sa.Column('author_user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('blocks_json', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )

    op.create_table('rules',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('account_id', sa.Integer(), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('query', sa.Text(), nullable=False),
        sa.Column('action_json', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default='true')
    )

    op.create_index('ix_threads_account_id', 'threads', ['account_id'])
    op.create_index('ix_messages_account_id', 'messages', ['account_id'])
    op.create_index('ix_messages_thread_id', 'messages', ['thread_id'])

def downgrade():
    op.drop_table('rules')
    op.drop_table('notes')
    op.drop_table('attachments')
    op.execute('DROP INDEX IF EXISTS ix_messages_fts')
    op.drop_table('messages')
    op.drop_table('threads')
    op.drop_table('accounts')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
