-- MoodBowl Production Schema (PostgreSQL)

-- Users
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    dietary_preferences JSONB, -- list of strings
    language VARCHAR(50) DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Moods
CREATE TABLE moods (
    mood_id SERIAL PRIMARY KEY,
    mood_name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Mood History
CREATE TABLE mood_history (
    mood_history_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    mood_id INTEGER REFERENCES moods(mood_id),
    intensity INTEGER CHECK (intensity >= 1 AND intensity <= 10),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Restaurants
CREATE TABLE restaurants (
    restaurant_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location TEXT,
    cuisine_type VARCHAR(100),
    rating DECIMAL(2,1),
    delivery_time INTEGER -- in minutes
);

-- Food Items
CREATE TABLE food_items (
    food_id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants(restaurant_id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    calories INTEGER,
    category VARCHAR(100),
    mood_type JSONB, -- array of strings for AI mapping
    dietary_tag JSONB, -- array of strings (vegan, nut-free, etc.)
    preparation_time INTEGER, -- in minutes
    image_url TEXT
);

-- Orders
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    total_price DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Order Items
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    food_id INTEGER REFERENCES food_items(food_id),
    quantity INTEGER NOT NULL DEFAULT 1,
    price DECIMAL(10,2) NOT NULL
);

-- Favorites
CREATE TABLE favorites (
    favorite_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    food_id INTEGER REFERENCES food_items(food_id),
    UNIQUE(user_id, food_id)
);

-- Voice Samples
CREATE TABLE voice_samples (
    voice_sample_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    detected_mood VARCHAR(100),
    confidence_score DECIMAL(3,2),
    audio_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Recommendations
CREATE TABLE recommendations (
    recommendation_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    mood_id INTEGER REFERENCES moods(mood_id),
    food_id INTEGER REFERENCES food_items(food_id),
    score DECIMAL(3,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
