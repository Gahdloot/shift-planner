-- Initialize the shift_planner database
-- This script creates the database and sets up initial permissions

-- Create database if it doesn't exist
SELECT 'CREATE DATABASE shift_planner'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'shift_planner')\gexec

-- Connect to the shift_planner database
\c shift_planner;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions to the shift_user
GRANT ALL PRIVILEGES ON DATABASE shift_planner TO shift_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO shift_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO shift_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO shift_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO shift_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO shift_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO shift_user; 