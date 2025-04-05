
-- Create table for raw simulator state per tick
CREATE TABLE IF NOT EXISTS state_raw (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    simulation_time VARCHAR(20) NOT NULL,
    season VARCHAR(10) NOT NULL,
    is_daytime BOOLEAN NOT NULL,
    temperature FLOAT NOT NULL,
    weather VARCHAR(20) NOT NULL,
    state_json JSON NOT NULL,
    processed_by_core BOOLEAN DEFAULT FALSE
);

-- Table for processed sensor outputs
CREATE TABLE IF NOT EXISTS sensor_outputs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state_id INT NOT NULL,
    sensor_id VARCHAR(50) NOT NULL,
    value VARCHAR(100) NOT NULL,
    timestamp DATETIME NOT NULL,
    FOREIGN KEY (state_id) REFERENCES state_raw(id)
);

-- Table for triggered rules
CREATE TABLE IF NOT EXISTS rule_triggers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state_id INT NOT NULL,
    rule_id VARCHAR(50) NOT NULL,
    device_id VARCHAR(50),
    timestamp DATETIME NOT NULL,
    FOREIGN KEY (state_id) REFERENCES state_raw(id)
);

-- Table for resulting device states
CREATE TABLE IF NOT EXISTS device_states (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state_id INT NOT NULL,
    device_id VARCHAR(50) NOT NULL,
    status VARCHAR(100) NOT NULL,
    timestamp DATETIME NOT NULL,
    FOREIGN KEY (state_id) REFERENCES state_raw(id)
);
