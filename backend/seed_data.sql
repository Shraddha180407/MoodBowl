-- Sample Data for MoodBowl

-- Moods
INSERT INTO moods (mood_name, description) VALUES 
('Happy', 'Feeling positive, energetic and balanced'),
('Stressed', 'Feeling overwhelmed or under pressure'),
('Sad', 'Feeling low, lonely or in need of comfort'),
('Energetic', 'Feeling enthusiastic and ready for physical activity'),
('Tired', 'Feeling low on energy or exhausted');

-- Restaurants
INSERT INTO restaurants (name, location, cuisine_type, rating, delivery_time) VALUES 
('Comfort Kitchen', 'Downtown', 'American', 4.5, 25),
('Green Bowl', 'Uptown', 'Healthy', 4.8, 20),
('Spicy Thai', 'Main St', 'Thai', 4.2, 35),
('Sweet Delights', 'Second Ave', 'Bakery', 4.7, 15),
('Protein Palace', 'West End', 'Grill', 4.4, 30);

-- Food Items (30+ items with mood_type mapping and images)
INSERT INTO food_items (restaurant_id, name, description, price, calories, category, mood_type, dietary_tag, preparation_time, image_url) VALUES 
(1, 'Mac & Cheese Bowl', 'Creamy elbow pasta with four cheeses', 12.99, 850, 'Main', '["stressed", "comfort", "sad"]', '["vegetarian"]', 15, 'https://images.unsplash.com/photo-1543339308-43e59d6b73a6?w=600&q=80'),
(1, 'Chicken Pot Pie', 'Flaky crust with chicken and vegetables', 14.50, 720, 'Main', '["comfort", "tired"]', '[]', 20, 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=600&q=80'),
(1, 'Grilled Cheese & Tomato Soup', 'Classic comfort duo', 10.99, 600, 'Combo', '["stressed", "comfort"]', '["vegetarian"]', 12, 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=600&q=80'),
(2, 'Kale & Quinoa Power Salad', 'Fresh kale, quinoa, avocado and lemon tahini', 15.00, 450, 'Salad', '["happy", "energetic"]', '["vegan", "gluten-free"]', 10, 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80'),
(2, 'Açaí Berry Bowl', 'Organic açaí topped with granola and honey', 11.50, 380, 'Breakfast', '["happy", "energetic"]', '["vegetarian"]', 8, 'https://images.unsplash.com/photo-1494597564530-871f2b93ac55?w=600&q=80'),
(2, 'Superfood Green Smoothie', 'Spinach, apple, ginger and spirulina', 8.99, 180, 'Drink', '["tired", "energetic"]', '["vegan"]', 5, 'https://images.unsplash.com/photo-1558160074-4d7d8bdf4256?w=600&q=80'),
(3, 'Pad Thai with Shrimp', 'Rice noodles with shrimp and peanuts', 16.50, 650, 'Main', '["happy", "stressed"]', '["contains-nuts"]', 18, 'https://images.unsplash.com/photo-1559314809-0d155014e29e?w=600&q=80'),
(3, 'Green Curry', 'Spicy coconut milk curry with vegetables', 15.99, 580, 'Main', '["sad", "comfort"]', '["spicy", "gluten-free"]', 22, 'https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=600&q=80'),
(3, 'Tom Yum Soup', 'Hot and sour soup with lemongrass', 7.99, 120, 'Soup', '["tired", "low-energy"]', '["spicy"]', 15, 'https://images.unsplash.com/photo-1548943487-a2e4142f4cd4?w=600&q=80'),
(4, 'Double Chocolate Cake Slice', 'Rich dark chocolate layer cake', 8.50, 550, 'Dessert', '["sad", "comfort", "celebration"]', '["vegetarian"]', 5, 'https://images.unsplash.com/photo-1578985545062-69928b1ea39d?w=600&q=80'),
(4, 'Red Velvet Cupcake', 'Soft cupcake with cream cheese frosting', 4.50, 320, 'Dessert', '["happy", "celebration"]', '["vegetarian"]', 0, 'https://images.unsplash.com/photo-1614707267537-b85aaf00c4b7?w=600&q=80'),
(4, 'Warm Apple Pie', 'Cinnamon spiced apples in a buttery crust', 7.99, 410, 'Dessert', '["comfort", "sad"]', '["vegetarian"]', 10, 'https://images.unsplash.com/photo-1568571780765-9276ac8b75a2?w=600&q=80'),
(5, 'Ribeye Steak', '12oz grass-fed ribeye grill-charred', 28.00, 950, 'Main', '["energetic", "tired"]', '["high-protein"]', 25, 'https://images.unsplash.com/photo-1600891964092-4316c288032e?w=600&q=80'),
(5, 'Grilled Chicken Breast', 'Herb marinated chicken with seasonal veg', 18.99, 420, 'Main', '["happy", "energetic"]', '["high-protein", "gluten-free"]', 15, 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=600&q=80'),
(5, 'Quinoa & Black Bean Burger', 'Plant-based patty with sweet potato fries', 14.50, 520, 'Main', '["happy", "neutral"]', '["vegetarian"]', 12, 'https://images.unsplash.com/photo-1520072959219-c595dc870360?w=600&q=80'),
(1, 'Mashed Potatoes', 'Whisked with butter and roasted garlic', 5.99, 320, 'Side', '["comfort", "stressed"]', '["vegetarian"]', 10, 'https://images.unsplash.com/photo-1644704381831-2db47bd81dbe?w=600&q=80'),
(1, 'Beef Stew', 'Slow-cooked beef with root vegetables', 13.99, 540, 'Main', '["sad", "tired"]', '[]', 15, 'https://images.unsplash.com/photo-1548943487-a2e4142f4cd4?w=600&q=80'),
(2, 'Zucchini Noodle Pesto', 'Zoodles with fresh basil pesto', 14.00, 240, 'Main', '["happy", "energetic"]', '["vegetarian", "gluten-free"]', 12, 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=600&q=80'),
(3, 'Mango Sticky Rice', 'Traditional Thai sweet rice with fresh mango', 9.50, 380, 'Dessert', '["happy", "celebration"]', '["vegan"]', 15, 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=600&q=80'),
(5, 'Salmon Fillet', 'Pan-seared Atlantic salmon', 21.00, 420, 'Main', '["happy", "tired"]', '["high-protein", "pescatarian"]', 18, 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=600&q=80'),
(4, 'Almond Croissant', 'Flaky butter croissant with almond filling', 5.50, 480, 'Bakery', '["happy", "relaxed"]', '["contains-nuts"]', 0, 'https://images.unsplash.com/photo-1509365465985-25d11c17e812?w=600&q=80'),
(1, 'Chicken Wings', '10pcs with buffalo sauce', 12.99, 820, 'Appetizer', '["happy", "energetic"]', '["spicy"]', 15, 'https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?w=600&q=80'),
(2, 'Hummus & Veggie Plate', 'Creamy hummus with cucumber and carrots', 9.99, 210, 'Appetizer', '["neutral", "healthy"]', '["vegan"]', 5, 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=600&q=80'),
(3, 'Spring Rolls', 'Crispy vegetable spring rolls with sweet chili', 6.99, 280, 'Appetizer', '["happy", "neutral"]', '["vegetarian"]', 10, 'https://images.unsplash.com/photo-1541529086526-db283c563270?w=600&q=80'),
(4, 'Blueberry Muffin', 'Baked fresh with wild blueberries', 3.99, 310, 'Bakery', '["happy", "tired"]', '["vegetarian"]', 0, 'https://images.unsplash.com/photo-1605333396914-25618848c48a?w=600&q=80'),
(5, 'Mixed Grill Platter', 'Chicken kebab, lamb chops and steak tips', 32.00, 1100, 'Main', '["energetic", "celebration"]', '["high-protein"]', 30, 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80'),
(2, 'Tuna Poke Bowl', 'Fresh tuna with avocado and seaweed', 17.50, 520, 'Main', '["happy", "energetic"]', '["pescatarian"]', 15, 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&q=80'),
(4, 'Artisan Sourdough Loaf', 'Standard sourdough loaf', 7.00, 1100, 'Bakery', '["comfort", "neutral"]', '["vegan"]', 0, 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80'),
(1, 'Truffle Fries', 'Crispy fries with truffle oil and parmesan', 8.50, 480, 'Side', '["happy", "stressed"]', '["vegetarian"]', 10, 'https://images.unsplash.com/photo-1623653387945-2fd25214f8fc?w=600&q=80'),
(3, 'Chicken Satay', 'Grilled skewers with peanut sauce', 11.99, 450, 'Appetizer', '["happy", "energetic"]', '["contains-nuts"]', 15, 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80');
