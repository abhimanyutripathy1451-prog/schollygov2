INSERT INTO curriculums
    (code, name, board, stream, medium, grade, type,
     is_active, sequence_order, created_at, updated_at)
VALUES
    ('CBSE_G5', 'CBSE Grade 5', 'CBSE', NULL, 'English', '5', 'school_board', 1, 50, UTC_TIMESTAMP(6), UTC_TIMESTAMP(6)),
    ('CBSE_G6', 'CBSE Grade 6', 'CBSE', NULL, 'English', '6', 'school_board', 0, 60, UTC_TIMESTAMP(6), UTC_TIMESTAMP(6)),
    ('CBSE_G7', 'CBSE Grade 7', 'CBSE', NULL, 'English', '7', 'school_board', 0, 70, UTC_TIMESTAMP(6), UTC_TIMESTAMP(6)),
    ('CBSE_G8', 'CBSE Grade 8', 'CBSE', NULL, 'English', '8', 'school_board', 0, 80, UTC_TIMESTAMP(6), UTC_TIMESTAMP(6)),
    ('CBSE_G9', 'CBSE Grade 9', 'CBSE', NULL, 'English', '9', 'school_board', 0, 90, UTC_TIMESTAMP(6), UTC_TIMESTAMP(6)),
    ('CBSE_G10', 'CBSE Grade 10', 'CBSE', NULL, 'English', '10', 'school_board', 0, 100, UTC_TIMESTAMP(6), UTC_TIMESTAMP(6)),
    ('CBSE_G11_SCI', 'CBSE Grade 11 Science', 'CBSE', 'Science', 'English', '11', 'school_board', 0, 111, UTC_TIMESTAMP(6), UTC_TIMESTAMP(6)),
    ('CBSE_G11_COM', 'CBSE Grade 11 Commerce', 'CBSE', 'Commerce', 'English', '11', 'school_board', 1, 112, UTC_TIMESTAMP(6), UTC_TIMESTAMP(6)),
    ('CBSE_G11_HUM', 'CBSE Grade 11 Humanities', 'CBSE', 'Humanities', 'English', '11', 'school_board', 0, 113, UTC_TIMESTAMP(6), UTC_TIMESTAMP(6)),
    ('CBSE_G12_SCI', 'CBSE Grade 12 Science', 'CBSE', 'Science', 'English', '12', 'school_board', 0, 121, UTC_TIMESTAMP(6), UTC_TIMESTAMP(6)),
    ('CBSE_G12_COM', 'CBSE Grade 12 Commerce', 'CBSE', 'Commerce', 'English', '12', 'school_board', 0, 122, UTC_TIMESTAMP(6), UTC_TIMESTAMP(6)),
    ('CBSE_G12_HUM', 'CBSE Grade 12 Humanities', 'CBSE', 'Humanities', 'English', '12', 'school_board', 0, 123, UTC_TIMESTAMP(6), UTC_TIMESTAMP(6))
ON DUPLICATE KEY UPDATE code=code;
