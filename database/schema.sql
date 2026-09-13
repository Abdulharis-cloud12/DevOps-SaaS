CREATE TABLE pipelines (
    pipeline_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (name, provider)
);


CREATE TABLE builds (
    build_id SERIAL PRIMARY KEY,
    pipeline_id INTEGER NOT NULL,
    build_number INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL,
    duration_seconds DOUBLE PRECISION NOT NULL DEFAULT 0,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    url TEXT,

    CONSTRAINT fk_build_pipeline
        FOREIGN KEY (pipeline_id)
        REFERENCES pipelines(pipeline_id),

    CONSTRAINT unique_pipeline_build
        UNIQUE (pipeline_id, build_number)
);
