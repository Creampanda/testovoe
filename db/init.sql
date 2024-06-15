CREATE TABLE meme (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    minio_bucket VARCHAR(255) NOT NULL,
    minio_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO meme (title, minio_bucket, minio_path) VALUES
('First Meme', 'memes', 'Cat01.jpg'),
('Second Meme', 'memes', 'Cat02.jpg'),
('Third Meme', 'memes', 'Cat03.jpg');