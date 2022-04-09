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
    server_id INTEGER NOT NULL,
    time DATETIME
);
CREATE TABLE IF NOT EXISTS punishments (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    issuer_id INTEGER NOT NULL,
    server_id INTEGER NOT NULL,
    type TEXT, /*BAN, KICK, TIMEOUT, WARN*/
    reason TEXT,
    time DATETIME,
    deleted BOOLEAN
);
CREATE TABLE IF NOT EXISTS passphrases (
    id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    content TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS experience (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    server_id INTEGER NOT NULL,
    last_experience DATETIME,
    amount INTEGER
);
CREATE TABLE IF NOT EXISTS raffles_and_polls (
    id INTEGER PRIMARY KEY,
    organizer_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    server_id INTEGER NOT NULL,
    type TEXT NOT NULL, /*RAFFLE or POLL*/
    name TEXT NOT NULL,
    description TEXT,
    end_date DATETIME NOT NULL
);
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY,
    content TEXT,
    reminder_date DATETIME NOT NULL,
    public BOOLEAN NOT NULL, /*Anyone can add themselves to a public reminder*/
    interval INTEGER, /*The reminder interval in milliseconds*/
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
CREATE TABLE IF NOT EXISTS server_roles (
    id INTEGER PRIMARY KEY,
    role_id INTEGER NOT NULL,
    server_id INTEGER NOT NULL,
    type TEXT /*NEW, VERIFIED, NORMAL, BIRTHDAY, MODERATOR, ADMIN*/
);
CREATE TABLE IF NOT EXISTS level_reward_roles (
    id INTEGER PRIMARY KEY,
    role_id INTEGER NOT NULL,
    server_id INTEGER NOT NULL,
    level_requirement INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS blacklist (
    id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    type TEXT NOT NULL, /*WORD or LINK*/
    content TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS blacklist_rules (
    id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    target_id INTEGER NOT NULL,
    target_type TEXT NOT NULL, /*CHANNEL or ROLE*/
    type TEXT NOT NULL, /*WORD or LINK*/
    mode TEXT NOT NULL /*BLACKLIST or WHITELIST*/
);
CREATE TABLE IF NOT EXISTS left_members (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    server_id INTEGER NOT NULL,
    leave_date DATETIME NOT NULL
);
CREATE TABLE IF NOT EXISTS unverified_kick_rules (
    id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    timedelta INTEGER /*in milliseconds*/
);
CREATE TABLE IF NOT EXISTS unverified_reminder_messages (
    id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    timedelta INTEGER
);
CREATE TABLE IF NOT EXISTS text_contents (
    id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    content TEXT,
    type TEXT /*WELCOME TEXT, WELCOME IMAGE*/
);
CREATE TABLE IF NOT EXISTS log_content_rules (
    id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    log_type TEXT NOT NULL, /*refer to documentation for possible log types*/
    enabled BOOLEAN
);
CREATE TABLE IF NOT EXISTS log_rules (
    id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    target_id INTEGER NOT NULL,
    target_type TEXT NOT NULL, /*MEMBER, ROLE, CHANNEL*/
    mode TEXT NOT NULL /*BLACKLIST or WHITELIST*/
);
CREATE TABLE IF NOT EXISTS default_channels (
    id INTEGER PRIMARY KEY,
    channel_id INTEGER NOT NULL,
    server_id INTEGER NOT NULL,
    channel_purpose /*LOG, RULES, PASSPHRASE*/
);