"""PostgreSQL trigger scripts for automatic timestamp updates."""

UPDATED_AT_FUNCTION = """
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

UPDATED_AT_TRIGGER = """
CREATE TRIGGER update_{table_name}_updated_at
BEFORE UPDATE ON {table_name}
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
"""
