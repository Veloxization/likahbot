import sqlite3
import sys
import hashlib

def updater(cursor, current_version):
    if current_version == 1:
        # Alter the user_products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_products_new (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            );
        """)
        cursor.execute("""
            INSERT INTO user_products_new (id, user_id, product_id)
            SELECT id, user_id, product_id FROM user_products;
        """)
        cursor.execute("DROP TABLE IF EXISTS user_products;")
        cursor.execute("ALTER TABLE user_products_new RENAME TO user_products;")

        # Alter the settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings_new (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                default_status TEXT NOT NULL
            );
        """)
        cursor.execute("""
            INSERT INTO settings_new (id, name, default_status)
            SELECT id, name, default_status FROM settings;
        """)
        cursor.execute("DROP TABLE IF EXISTS settings;")
        cursor.execute("ALTER TABLE settings_new RENAME TO settings;")

        # Alter the guild_settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guild_settings_new (
                id INTEGER PRIMARY KEY,
                guild_id INTEGER NOT NULL,
                setting_id INTEGER NOT NULL,
                setting_status TEXT,
                FOREIGN KEY (setting_id) REFERENCES settings (id),
                CONSTRAINT unq UNIQUE (guild_id, setting_id)
            );
        """)
        cursor.execute("""
            INSERT INTO guild_settings_new (id, guild_id, setting_id, setting_status)
            SELECT id, guild_id, setting_id, setting_status FROM guild_settings;
        """)
        cursor.execute("DROP TABLE IF EXISTS guild_settings;")
        cursor.execute("ALTER TABLE guild_settings_new RENAME TO guild_settings;")

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 2")
        print("Updated database to version 2")
        return False
    elif current_version == 2:
        # Add the default settings
        cursor.execute("INSERT INTO settings (name, default_status) VALUES ('log_edited_messages', '1');")
        cursor.execute("INSERT INTO settings (name, default_status) VALUES ('log_deleted_messages', '1');")
        cursor.execute("INSERT INTO settings (name, default_status) VALUES ('log_membership_changes', '1');")
        cursor.execute("INSERT INTO settings (name, default_status) VALUES ('log_timeouts', '1');")
        cursor.execute("INSERT INTO settings (name, default_status) VALUES ('log_warnings', '1');")
        cursor.execute("INSERT INTO settings (name, default_status) VALUES ('log_name_changes', '0');")
        cursor.execute("INSERT INTO settings (name, default_status) VALUES ('log_member_role_changes', '0');")
        cursor.execute("INSERT INTO settings (name, default_status) VALUES ('log_avatar_changes', '0');")
        cursor.execute("INSERT INTO settings (name, default_status) VALUES ('log_channel_changes', '0');")
        cursor.execute("INSERT INTO settings (name, default_status) VALUES ('log_guild_role_changes', '0');")
        cursor.execute("INSERT INTO settings (name, default_status) VALUES ('log_invites', '0');")
        cursor.execute("INSERT INTO settings (name, default_status) VALUES ('log_message_reactions', '0');")
        cursor.execute("INSERT INTO settings (name, default_status) VALUES ('log_webhook_changes', '0');")

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 3")
        print("Updated database to version 3")
        return False
    elif current_version == 3:
        # Set the new user version
        cursor.execute("PRAGMA user_version = 4")
        print("Updated database to version 4")
        return False
    elif current_version == 4:
        cursor.execute("ALTER TABLE settings RENAME TO settings_backup")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                setting_status TEXT NOT NULL
            )
        """)
        cursor.execute("INSERT INTO settings (id, name, setting_status) SELECT id, name, default_status FROM settings_backup")
        cursor.execute("DROP TABLE IF EXISTS settings_backup")

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 5")
        print("Updated database to version 5")
        return False
    elif current_version == 5:
        cursor.execute("ALTER TABLE guild_settings RENAME TO guild_settings_backup")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guild_settings (
                id INTEGER PRIMARY KEY,
                guild_id INTEGER NOT NULL,
                setting_id INTEGER NOT NULL,
                setting_status TEXT NOT NULL,
                FOREIGN KEY (setting_id) REFERENCES settings (id),
                CONSTRAINT unq UNIQUE (guild_id, setting_id)
            )
        """)
        cursor.execute('INSERT INTO guild_settings (id, guild_id, setting_id, setting_status) SELECT id, guild_id, setting_id, setting_status FROM guild_settings_backup')
        cursor.execute('DROP TABLE IF EXISTS guild_settings_backup')

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 6")
        print("Updated database to version 6")
        return False
    elif current_version == 6:
        cursor.execute("ALTER TABLE reminders RENAME TO reminders_backup")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY,
                creator_id INTEGER NOT NULL,
                creator_guild_id INTEGER,
                content TEXT NOT NULL,
                reminder_date DATETIME NOT NULL,
                public BOOLEAN NOT NULL,
                interval INTEGER,
                repeats_left INTEGER,
                next_reminder TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO reminders (
                id, creator_id, creator_guild_id, content, reminder_date,
                public, interval, repeats_left, next_reminder
            )
            SELECT
                id, 0, 0, content, reminder_date,
                public, interval, repeats_left, next_reminder
            FROM reminders_backup
        """)
        cursor.execute("DROP TABLE IF EXISTS reminders_backup")

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 7")
        print("Updated database to version 7")
        return False
    elif current_version == 7:
        cursor.execute("ALTER TABLE reminders RENAME TO reminders_backup")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY,
                creator_id INTEGER NOT NULL,
                creator_guild_id INTEGER,
                message_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                reminder_date DATETIME NOT NULL,
                public BOOLEAN NOT NULL,
                interval INTEGER,
                repeats_left INTEGER
            )
        """)
        cursor.execute("""
            INSERT INTO reminders (
                id, creator_id, creator_guild_id, message_id, content, reminder_date,
                public, interval, repeats_left
            )
            SELECT
                id, creator_id, creator_guild_id, NULL, content, reminder_date,
                public, interval, repeats_left
            FROM reminders_backup
        """)
        cursor.execute("DROP TABLE IF EXISTS reminders_backup")

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 8")
        print("Updated database to version 8")
        return False
    elif current_version == 8:
        cursor.execute("ALTER TABLE settings RENAME TO settings_backup")
        cursor.execute("ALTER TABLE guild_settings RENAME TO guild_settings_backup")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                setting_value TEXT NOT NULL
            )
        """)
        cursor.execute("INSERT INTO settings (id, name, setting_value) SELECT id, name, setting_status FROM settings_backup")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guild_settings (
                id INTEGER PRIMARY KEY,
                guild_id INTEGER NOT NULL,
                setting_id INTEGER NOT NULL,
                setting_value TEXT NOT NULL,
                FOREIGN KEY (setting_id) REFERENCES settings (id),
                CONSTRAINT unq UNIQUE (guild_id, setting_id)
            )
        """)
        cursor.execute("""
            INSERT INTO guild_settings (id, guild_id, setting_id, setting_value)
            SELECT id, guild_id, setting_id, setting_status FROM guild_settings_backup
        """)
        cursor.execute("DROP TABLE IF EXISTS settings_backup")
        cursor.execute("DROP TABLE IF EXISTS guild_settings_backup")

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 9")
        print("Updated database to version 9")
        return False
    elif current_version == 9:
        # Set the new user_version
        cursor.execute("PRAGMA user_version = 10")
        print("Updated database to version 10")
        return False
    elif current_version == 10:
        # Set the new user_version
        cursor.execute("PRAGMA user_version = 11")
        print("Updated database to version 11")
        return False
    elif current_version == 11:
        cursor.execute("ALTER TABLE time_zones RENAME TO time_zones_backup")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS time_zones (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL UNIQUE,
                time_zone TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO time_zones (id, user_id, time_zone)
            SELECT id, user_id, time_zone FROM time_zones_backup
        """)
        cursor.execute("DROP TABLE IF EXISTS time_zones_backup")

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 12")
        print("Updated database to version 12")
        return False
    elif current_version == 12:
        cursor.execute("ALTER TABLE utility_channels RENAME TO utility_channels_backup")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS utility_channels (
                id INTEGER PRIMARY KEY,
                channel_id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,
                channel_purpose TEXT NOT NULL,
                CONSTRAINT unq UNIQUE (channel_id, guild_id, channel_purpose)
            )
        """)
        cursor.execute("""
            INSERT INTO utility_channels (id, channel_id, guild_id, channel_purpose)
            SELECT id, channel_id, guild_id, channel_purpose FROM utility_channels_backup
        """)
        cursor.execute("DROP TABLE IF EXISTS utility_channels_backup")

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 13")
        print("Updated database to version 13")
        return False
    elif current_version == 13:
        cursor.execute("ALTER TABLE reminders RENAME TO reminders_backup")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY,
                creator_id INTEGER NOT NULL,
                creator_guild_id INTEGER,
                content TEXT NOT NULL,
                reminder_date DATETIME NOT NULL,
                public BOOLEAN NOT NULL,
                interval INTEGER,
                repeats_left INTEGER
            )
        """)
        cursor.execute("""
            INSERT INTO reminders (
                id, creator_id, creator_guild_id, content, reminder_date,
                public, interval, repeats_left
            )
            SELECT
                id, creator_id, creator_guild_id, content, reminder_date,
                public, interval, repeats_left
            FROM reminders_backup
        """)
        cursor.execute("DROP TABLE IF EXISTS reminders_backup")

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 14")
        print("Updated database to version 14")
        return False
    elif current_version == 14:
        cursor.execute("ALTER TABLE reminders RENAME TO reminders_backup")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY,
                creator_id INTEGER NOT NULL,
                creator_guild_id INTEGER,
                content TEXT NOT NULL,
                reminder_date DATETIME NOT NULL,
                public BOOLEAN NOT NULL,
                interval INTEGER,
                reminder_type TEXT NOT NULL,
                repeats_left INTEGER
            )
        """)
        cursor.execute("""
            INSERT INTO reminders (
                id, creator_id, creator_guild_id, content, reminder_date,
                public, interval, reminder_type, repeats_left
            )
            SELECT
                id, creator_id, creator_guild_id, content, reminder_date,
                public, interval, 'weekday', repeats_left
            FROM reminders_backup
        """)
        cursor.execute("DROP TABLE IF EXISTS reminders_backup")

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 15")
        print("Updated database to version 15")
        return False
    elif current_version == 15:
        cursor.execute("ALTER TABLE user_reminders RENAME TO user_reminders_backup")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_reminders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                reminder_id INTEGER NOT NULL,
                FOREIGN KEY (reminder_id) REFERENCES reminders (id) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            INSERT INTO user_reminders (
                id, user_id, reminder_id
            )
            SELECT
                id, user_id, reminder_id
            FROM user_reminders_backup
        """)
        cursor.execute("DROP TABLE IF EXISTS user_reminders_backup")

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 16")
        print("Updated database to version 16")
        return False
    elif current_version == 16:
        cursor.execute("ALTER TABLE verification_answers RENAME TO verification_answers_backup")
        cursor.execute("ALTER TABLE guild_roles RENAME TO guild_roles_backup")
        cursor.execute("ALTER TABLE unverified_reminder_history RENAME TO unverified_reminder_history_backup")
        cursor.execute("ALTER TABLE user_currencies RENAME TO user_currencies_backup")
        cursor.execute("ALTER TABLE store_products RENAME TO store_products_backup")
        cursor.execute("ALTER TABLE user_products RENAME TO user_products_backup")
        cursor.execute("ALTER TABLE guild_settings RENAME TO guild_settings_backup")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verification_answers (
            id INTEGER PRIMARY KEY,
            question_id INTEGER NOT NULL,
            answer TEXT,
            FOREIGN KEY (question_id) REFERENCES verification_questions (id) ON DELETE CASCADE
        );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guild_roles (
            id INTEGER PRIMARY KEY,
            role_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES guild_role_categories (id) ON DELETE CASCADE
        );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS unverified_reminder_history (
            id INTEGER PRIMARY KEY,
            reminder_message_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (reminder_message_id) REFERENCES unverified_reminder_messages (id) ON DELETE CASCADE
        );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_currencies (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            currency_id INTEGER NOT NULL,
            amount INTEGER,
            FOREIGN KEY (currency_id) REFERENCES currencies (id) ON DELETE CASCADE
        );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS store_products (
            id INTEGER PRIMARY KEY,
            guild_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            price_currency_id INTEGER NOT NULL,
            price INTEGER,
            FOREIGN KEY (price_currency_id) REFERENCES currencies (id),
            FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
        );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_products (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
        );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guild_settings (
            id INTEGER PRIMARY KEY,
            guild_id INTEGER NOT NULL,
            setting_id INTEGER NOT NULL,
            setting_value TEXT NOT NULL,
            FOREIGN KEY (setting_id) REFERENCES settings (id) ON DELETE CASCADE,
            CONSTRAINT unq UNIQUE (guild_id, setting_id)
        );
        """)
        cursor.execute("""
            INSERT INTO verification_answers (
                id, question_id, answer
            )
            SELECT
                id, question_id, answer
            FROM verification_answers_backup
        """)
        cursor.execute("""
            INSERT INTO guild_roles (
                id, role_id, category_id
            )
            SELECT
                id, role_id, category_id
            FROM guild_roles_backup
        """)
        cursor.execute("""
            INSERT INTO unverified_reminder_history (
                id, reminder_message_id, user_id
            )
            SELECT
                id, reminder_message_id, user_id
            FROM unverified_reminder_history_backup
        """)
        cursor.execute("""
            INSERT INTO user_currencies (
                id, user_id, currency_id, amount
            )
            SELECT
                id, user_id, currency_id, amount
            FROM user_currencies_backup
        """)
        cursor.execute("""
            INSERT INTO store_products (
                id, guild_id, product_id, price_currency_id, price
            )
            SELECT
                id, guild_id, product_id, price_currency_id, price
            FROM store_products_backup
        """)
        cursor.execute("""
            INSERT INTO user_products (
                id, user_id, product_id
            )
            SELECT
                id, user_id, product_id
            FROM user_products_backup
        """)
        cursor.execute("""
            INSERT INTO guild_settings (
                id, guild_id, setting_id, setting_value
            )
            SELECT
                id, guild_id, setting_id, setting_value
            FROM guild_settings_backup
        """)
        cursor.execute("DROP TABLE IF EXISTS verification_answers_backup")
        cursor.execute("DROP TABLE IF EXISTS guild_roles_backup")
        cursor.execute("DROP TABLE IF EXISTS unverified_reminder_history_backup")
        cursor.execute("DROP TABLE IF EXISTS user_currencies_backup")
        cursor.execute("DROP TABLE IF EXISTS store_products_backup")
        cursor.execute("DROP TABLE IF EXISTS user_products_backup")
        cursor.execute("DROP TABLE IF EXISTS guild_settings_backup")

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 17")
        print("Updated database to version 17")
        return False
    elif current_version == 17:
        cursor.execute("""
            CREATE TRIGGER update_price_currency_to_null
            BEFORE DELETE ON currencies
            FOR EACH ROW
            BEGIN
                UPDATE store_products
                SET price_currency_id = NULL
                WHERE price_currency_id = OLD.id;
            END;
        """)

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 18")
        print("Updated database to version 18")
        return False
    elif current_version == 18:
        # Set the new user_version
        cursor.execute("PRAGMA user_version = 19")
        print("Updated database to version 19")
        return False
    elif current_version == 19:
        cursor.execute("ALTER TABLE user_reminders RENAME TO user_reminders_backup")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_reminders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            reminder_id INTEGER NOT NULL,
            FOREIGN KEY (reminder_id) REFERENCES reminders (id) ON DELETE CASCADE,
            CONSTRAINT unq UNIQUE (user_id, reminder_id)
        );
        """)
        cursor.execute("""
            INSERT INTO user_reminders (
                id, user_id, reminder_id
            )
            SELECT
                id, user_id, reminder_id
            FROM user_reminders_backup
        """)
        cursor.execute("DROP TABLE IF EXISTS user_reminders_backup")

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 20")
        print("Updated database to version 20")
        return False
    elif current_version == 20:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS global_names (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            global_name TEXT NOT NULL,
            time DATETIME
        );
        """)

        # Set the new user_version
        cursor.execute("PRAGMA user_version = 21")
        print("Updated database to version 21")
        return False
    elif current_version == 21:
        cursor.execute("ALTER TABLE punishments RENAME TO punishments_backup")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS punishments (
            id INTEGER PRIMARY KEY,
            user_id TEXT NOT NULL,
            issuer_id INTEGER NOT NULL,
            guild_id INTEGER NOT NULL,
            type TEXT, /*BAN, KICK, TIMEOUT, WARN*/
            reason TEXT,
            time DATETIME,
            deleted BOOLEAN
        );
        """)
        cursor.execute("""
        INSERT INTO punishments (
            id, user_id, issuer_id, guild_id, type, reason, time, deleted
        )
        SELECT id, user_id, issuer_id, guild_id, type, reason, time, deleted
        FROM punishments_backup
        """)
        cursor.execute("DROP TABLE punishments_backup")
        rows = cursor.execute("SELECT * FROM punishments")
        for row in rows:
            user_id = row["user_id"]
            h = hashlib.new("sha256")
            h.update(repr(user_id).encode())
            cursor.execute("UPDATE punishments SET user_id=? WHERE id=?", (h.hexdigest(), row["id"]))
            conn.commit()

        # Set the new new user_version
        cursor.execute("PRAGMA user_version = 22")
        print("Updated database to version 22")
        return True
    else:
        print("No new updates found for your database version")
        return True
    return True

def main():
    # Setup
    current_version = 0
    db_addr = str(sys.argv[1])

    # Connect to the database
    conn = sqlite3.connect(db_addr)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get the current user_version
    cursor.execute("PRAGMA user_version")
    current_version = cursor.fetchone()[0]

    up_to_date = False

    while not up_to_date:
        up_to_date = updater(cursor, current_version)
        cursor.execute("PRAGMA user_version")
        current_version = cursor.fetchone()[0]

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
