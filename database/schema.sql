PRAGMA user_version = 21;

CREATE TABLE IF NOT EXISTS usernames (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    time DATETIME
);
CREATE TABLE IF NOT EXISTS global_names (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    global_name TEXT NOT NULL,
    time DATETIME
);
CREATE TABLE IF NOT EXISTS nicknames (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    nickname TEXT NOT NULL,
    guild_id INTEGER NOT NULL,
    time DATETIME
);
CREATE TABLE IF NOT EXISTS punishments (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    issuer_id INTEGER NOT NULL,
    guild_id INTEGER NOT NULL,
    type TEXT, /*BAN, KICK, TIMEOUT, WARN*/
    reason TEXT,
    time DATETIME,
    deleted BOOLEAN
);
CREATE TABLE IF NOT EXISTS verification_questions (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    question_priority INTEGER
);
CREATE TABLE IF NOT EXISTS verification_answers (
    id INTEGER PRIMARY KEY,
    question_id INTEGER NOT NULL,
    answer TEXT,
    FOREIGN KEY (question_id) REFERENCES verification_questions (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS experience (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    guild_id INTEGER NOT NULL,
    last_experience DATETIME,
    amount INTEGER
);
CREATE TABLE IF NOT EXISTS raffles_and_polls (
    id INTEGER PRIMARY KEY,
    organizer_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    guild_id INTEGER NOT NULL,
    type TEXT NOT NULL, /*RAFFLE or POLL*/
    name TEXT NOT NULL,
    description TEXT,
    end_date DATETIME NOT NULL
);
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY,
    creator_id INTEGER NOT NULL,
    creator_guild_id INTEGER,
    content TEXT NOT NULL,
    reminder_date DATETIME NOT NULL,
    public BOOLEAN NOT NULL, /*Anyone can add themselves to a public reminder*/
    interval INTEGER, /*The reminder interval in seconds*/
    reminder_type TEXT NOT NULL, /*weekday, date, time, after*/
    repeats_left INTEGER
);
CREATE TABLE IF NOT EXISTS user_reminders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    reminder_id INTEGER NOT NULL,
    FOREIGN KEY (reminder_id) REFERENCES reminders (id) ON DELETE CASCADE,
    CONSTRAINT unq UNIQUE (user_id, reminder_id)
);
CREATE TABLE IF NOT EXISTS time_zones (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    time_zone TEXT
);
CREATE TABLE IF NOT EXISTS birthdays (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    birth_date DATE NOT NULL
);
CREATE TABLE IF NOT EXISTS guild_role_categories (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    category TEXT NOT NULL, /*NEW, VERIFIED, NORMAL, BIRTHDAY, MODERATOR, ADMIN*/
    CONSTRAINT unq UNIQUE (guild_id, category)
);
CREATE TABLE IF NOT EXISTS guild_roles (
    id INTEGER PRIMARY KEY,
    role_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES guild_role_categories (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS level_reward_roles (
    id INTEGER PRIMARY KEY,
    role_id INTEGER NOT NULL,
    guild_id INTEGER NOT NULL,
    level_requirement INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS blacklist (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    type TEXT NOT NULL, /*WORD or LINK*/
    content TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS blacklist_rules (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    target_id INTEGER NOT NULL,
    target_type TEXT NOT NULL, /*CHANNEL or ROLE*/
    type TEXT NOT NULL, /*WORD or LINK*/
    mode TEXT NOT NULL /*BLACKLIST or WHITELIST*/
);
CREATE TABLE IF NOT EXISTS left_members (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    guild_id INTEGER NOT NULL,
    leave_date DATETIME NOT NULL
);
CREATE TABLE IF NOT EXISTS temporary_bans (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    guild_id INTEGER NOT NULL,
    unban_date DATETIME NOT NULL,
    CONSTRAINT unq UNIQUE (user_id, guild_id)
);
CREATE TABLE IF NOT EXISTS unverified_kick_rules (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER NOT NULL UNIQUE,
    timedelta INTEGER /*in seconds*/
);
CREATE TABLE IF NOT EXISTS unverified_reminder_messages (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    timedelta INTEGER
);
CREATE TABLE IF NOT EXISTS unverified_reminder_history (
    id INTEGER PRIMARY KEY,
    reminder_message_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (reminder_message_id) REFERENCES unverified_reminder_messages (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS text_contents (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    content TEXT,
    type TEXT, /*WELCOME TEXT, WELCOME IMAGE*/
    CONSTRAINT unq UNIQUE (guild_id, type)
);
CREATE TABLE IF NOT EXISTS log_content_rules (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    log_type TEXT NOT NULL, /*refer to documentation for possible log types*/
    enabled BOOLEAN
);
CREATE TABLE IF NOT EXISTS log_rules (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    target_id INTEGER NOT NULL,
    target_type TEXT NOT NULL, /*MEMBER, ROLE, CHANNEL*/
    mode TEXT NOT NULL /*BLACKLIST or WHITELIST*/
);
CREATE TABLE IF NOT EXISTS utility_channels (
    id INTEGER PRIMARY KEY,
    channel_id INTEGER NOT NULL,
    guild_id INTEGER NOT NULL,
    channel_purpose TEXT NOT NULL, /*LOG, RULES, PASSPHRASE*/
    CONSTRAINT unq UNIQUE (channel_id, guild_id, channel_purpose)
);
CREATE TABLE IF NOT EXISTS currencies (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    currency_name TEXT,
    currency_abbreviation TEXT
);
CREATE TABLE IF NOT EXISTS user_currencies (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    currency_id INTEGER NOT NULL,
    amount INTEGER,
    FOREIGN KEY (currency_id) REFERENCES currencies (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    product_data TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS store_products (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    price_currency_id INTEGER NOT NULL,
    price INTEGER,
    FOREIGN KEY (price_currency_id) REFERENCES currencies (id),
    FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS user_products (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    setting_value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS guild_settings (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    setting_id INTEGER NOT NULL,
    setting_value TEXT NOT NULL,
    FOREIGN KEY (setting_id) REFERENCES settings (id) ON DELETE CASCADE,
    CONSTRAINT unq UNIQUE (guild_id, setting_id)
);
CREATE TRIGGER IF NOT EXISTS update_price_currency_to_null
BEFORE DELETE ON currencies
FOR EACH ROW
BEGIN
    UPDATE store_products
    SET price_currency_id = NULL
    WHERE price_currency_id = OLD.id;
END;
DELETE FROM settings;
INSERT INTO settings (name, setting_value) VALUES ('log_edited_messages', '1');
INSERT INTO settings (name, setting_value) VALUES ('log_deleted_messages', '1');
INSERT INTO settings (name, setting_value) VALUES ('log_membership_changes', '1');
INSERT INTO settings (name, setting_value) VALUES ('log_bans', '1');
INSERT INTO settings (name, setting_value) VALUES ('log_timeouts', '1');
INSERT INTO settings (name, setting_value) VALUES ('log_warnings', '1');
INSERT INTO settings (name, setting_value) VALUES ('log_name_changes', '0');
INSERT INTO settings (name, setting_value) VALUES ('log_member_role_changes', '0');
INSERT INTO settings (name, setting_value) VALUES ('log_avatar_changes', '0');
INSERT INTO settings (name, setting_value) VALUES ('log_channel_changes', '0');
INSERT INTO settings (name, setting_value) VALUES ('log_guild_role_changes', '0');
INSERT INTO settings (name, setting_value) VALUES ('log_invites', '0');
INSERT INTO settings (name, setting_value) VALUES ('log_message_reactions', '0');
INSERT INTO settings (name, setting_value) VALUES ('log_webhook_changes', '0');
