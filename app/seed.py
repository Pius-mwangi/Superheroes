from app import app, db, Hero, Power, HeroPower

# Create an application context
app_ctx = app.app_context()
app_ctx.push()

# Create all tables in the database
with app.app_context():
    db.create_all()

# Seed the database with sample heroes
heroes_data = [
    {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
    {"name": "Doreen Green", "super_name": "Squirrel Girl"},
    {"name": "Gwen Stacy", "super_name": "Spider-Gwen"}
]

for hero_data in heroes_data:
    hero = Hero(**hero_data)
    db.session.add(hero)

# Seed the database with sample powers
powers_data = [
    {"name": "super strength", "description": "gives the wielder super-human strengths"},
    {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"}
]

for power_data in powers_data:
    power = Power(**power_data)
    db.session.add(power)

# Seed the database with sample hero-powers associations
hero_powers_data = [
    {"strength": "Strong", "hero_id": 1, "power_id": 1},
    {"strength": "Weak", "hero_id": 1, "power_id": 2},
    {"strength": "Average", "hero_id": 2, "power_id": 1},
]

for hero_power_data in hero_powers_data:
    hero_power = HeroPower(**hero_power_data)
    db.session.add(hero_power)

# Commit the changes to the database
db.session.commit()

# Pop the application context
app_ctx.pop()

print("Database seeded successfully!")
