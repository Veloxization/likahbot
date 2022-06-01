CREATE TABLE IF NOT EXISTS usernames (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
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
CREATE TABLE IF NOT EXISTS passphrases (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    content TEXT NOT NULL
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
    content TEXT NOT NULL,
    reminder_date DATETIME NOT NULL,
    public BOOLEAN NOT NULL, /*Anyone can add themselves to a public reminder*/
    interval INTEGER, /*The reminder interval in seconds*/
    repeats_left INTEGER,
    next_reminder TEXT
);
CREATE TABLE IF NOT EXISTS user_reminders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    reminder_id INTEGER NOT NULL,
    FOREIGN KEY (reminder_id) REFERENCES reminders (id)
);
CREATE TABLE IF NOT EXISTS time_zones (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
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
    FOREIGN KEY (category_id) REFERENCES guild_role_categories (id)
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
    FOREIGN KEY (reminder_message_id) REFERENCES unverified_reminder_messages (id)
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
    channel_purpose /*LOG, RULES, PASSPHRASE*/
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
    FOREIGN KEY (currency_id) REFERENCES currencies (id)
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
    FOREIGN KEY (product_id) REFERENCES products (id)
);
CREATE TABLE IF NOT EXISTS user_products (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (id)
);
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER NOT NULL,
    name TEXT NOT NULL,
    default_status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS guild_settings (
    id INTEGER NOT NULL,
    guild_id INTEGER NOT NULL,
    setting_id INTEGER NOT NULL,
    setting_status TEXT,
    FOREIGN KEY (setting_id) REFERENCES settings (id)
);