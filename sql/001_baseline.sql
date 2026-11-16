CREATE TABLE IF NOT EXISTS curriculums (
 id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, code VARCHAR(50) COLLATE utf8mb4_bin NOT NULL UNIQUE,
 name VARCHAR(100) NOT NULL, board VARCHAR(100) NOT NULL, stream VARCHAR(50) NULL,
 medium VARCHAR(100) NOT NULL, grade VARCHAR(20) NOT NULL, type VARCHAR(50) NOT NULL,
 is_active BOOLEAN NOT NULL DEFAULT TRUE, sequence_order INT NOT NULL DEFAULT 0,
 created_at DATETIME(6) NOT NULL, updated_at DATETIME(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
CREATE TABLE IF NOT EXISTS users (
 id CHAR(36) NOT NULL PRIMARY KEY, mobile_e164 VARCHAR(16) NOT NULL UNIQUE,
 pin_hash VARCHAR(100) NOT NULL, mobile_verified_at DATETIME(6) NULL,
 status ENUM('active','disabled') NOT NULL DEFAULT 'active',
 login_failures INT UNSIGNED NOT NULL DEFAULT 0, locked_until DATETIME(6) NULL,
 full_name VARCHAR(120) NOT NULL, avatar_seed VARCHAR(100) NULL,
 curriculum_code VARCHAR(50) COLLATE utf8mb4_bin NOT NULL,
 school_name VARCHAR(150) NULL, guardian_name VARCHAR(120) NULL,
 guardian_mobile_e164 VARCHAR(16) NULL, guardian_email VARCHAR(254) NULL,
 timezone VARCHAR(64) NOT NULL DEFAULT 'Asia/Kolkata',
 created_at DATETIME(6) NOT NULL, updated_at DATETIME(6) NOT NULL,
 CONSTRAINT fk_users_curriculum FOREIGN KEY (curriculum_code) REFERENCES curriculums(code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
CREATE TABLE IF NOT EXISTS auth_sessions (
 id CHAR(36) NOT NULL PRIMARY KEY, user_id CHAR(36) NOT NULL,
 token_hash CHAR(64) NOT NULL UNIQUE, remember_me BOOLEAN NOT NULL,
 created_at DATETIME(6) NOT NULL, expires_at DATETIME(6) NOT NULL,
 revoked_at DATETIME(6) NULL,
 INDEX ix_sessions_user (user_id), INDEX ix_sessions_expiry (expires_at),
 CONSTRAINT fk_sessions_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
CREATE TABLE IF NOT EXISTS otp_challenges (
 id CHAR(36) NOT NULL PRIMARY KEY, mobile_e164 VARCHAR(16) NOT NULL,
 purpose ENUM('signup','recovery') NOT NULL, verifier CHAR(64) NOT NULL,
 attempts_remaining INT UNSIGNED NOT NULL, expires_at DATETIME(6) NOT NULL,
 verified_at DATETIME(6) NULL, consumed_at DATETIME(6) NULL,
 grant_hash CHAR(64) NULL UNIQUE, grant_expires_at DATETIME(6) NULL,
 created_at DATETIME(6) NOT NULL, request_ip_hash CHAR(64) NOT NULL,
 INDEX ix_otp_throttle (mobile_e164,purpose,created_at),
 INDEX ix_otp_ip (request_ip_hash,created_at), INDEX ix_otp_expiry (expires_at), INDEX ix_otp_grant_expiry (grant_expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
