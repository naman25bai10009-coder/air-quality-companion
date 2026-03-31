import pandas as pd
import numpy as np
import time
from sklearn.ensemble import RandomForestRegressor 
# You know, I was thinking about air quality the other day
# and how we never really pay attention to it until it's really bad
# So I put together this little thing to help make sense of the numbers

def get_that_air_data_file():
    """
    Trying to find that air quality file I was working with
    I think I saved it around here somewhere...
    """
    print("Hey, let me look for that air quality data...")
    time.sleep(1.2)
    
    # I remember downloading this dataset a while back
    try:
        the_data = pd.read_csv('city_day.csv')
        print(f"Oh good, found it! There's {len(the_data)} different air readings here.")
        print(f"Looks like this goes from {the_data['Date'].min()} to {the_data['Date'].max()} - that's a lot of days!")
        
        cities_in_data = the_data['City'].unique()
        print(f"And wow, there's {len(cities_in_data)} different cities! Like {cities_in_data[0]}, {cities_in_data[1]}, {cities_in_data[2]}...")
        
        return the_data
        
    except:
        print("Hmm, I can't seem to find that file right now.")
        print("You know that Indian cities air quality dataset from Kaggle?")
        print("If you grab that and save it as 'city_day.csv' here, that would be great.")
        return None

def clean_up_the_air_numbers(raw_air_readings):
    """
    This data needs some cleaning up - lots of missing numbers here and there
    Gotta fill in the blanks with reasonable guesses
    """
    print("Just cleaning up some missing numbers in the data...")
    
    # These are the columns we actually care about
    columns_we_need = ['City', 'Date', 'PM2.5', 'PM10', 'AQI']
    cleaner_readings = raw_air_readings[columns_we_need].copy()
    
    # For each city, fill missing numbers with that city's average
    for number_type in ['PM2.5', 'PM10', 'AQI']:
        cleaner_readings[number_type] = cleaner_readings.groupby('City')[number_type].transform(
            lambda x: x.fillna(x.mean()) if not pd.isna(x.mean()) else x
        )
    
    # Get rid of any rows that still don't have AQI numbers
    cleaner_readings = cleaner_readings.dropna(subset=['AQI'])
    
    print(f"Okay, much better! Now we have {len(cleaner_readings)} good records to work with.")
    return cleaner_readings

def find_days_with_similar_air(your_tiny_particles, your_dust_particles, historical_air_data):
    """
    Let me look through past air quality data and find days that were similar to what you're seeing
    It helps to compare with real historical situations
    """
    # Looking for days where air quality was in the same ballpark as yours
    similar_air_days = historical_air_data[
        (historical_air_data['PM2.5'] >= your_tiny_particles * 0.7) & 
        (historical_air_data['PM2.5'] <= your_tiny_particles * 1.3) &
        (historical_air_data['PM10'] >= your_dust_particles * 0.7) & 
        (historical_air_data['PM10'] <= your_dust_particles * 1.3)
    ]
    
    if len(similar_air_days) > 0:
        print(f"Nice! I found {len(similar_air_days)} days that had air quality pretty close to yours.")
        
        # Show a couple examples so you can see what I mean
        some_example_days = similar_air_days.sample(min(2, len(similar_air_days)))
        for _, example_day in some_example_days.iterrows():
            air_quality_type = what_kind_of_air_is_this(example_day['AQI'])
            print(f"   Like in {example_day['City']} on {example_day['Date']}: AQI was {example_day['AQI']:.0f} - {air_quality_type}")
        
        # Use the average from these similar days
        average_aqi_reading = similar_air_days['AQI'].mean()
        return average_aqi_reading, similar_air_days
    
    else:
        print("Hmm, your air situation seems pretty unusual - not finding close matches.")
        print("Let me estimate an AQI based on standard calculation methods...")
        calculated_aqi = calculate_aqi_based_on_particles(your_tiny_particles)
        return calculated_aqi, None

def calculate_aqi_based_on_particles(tiny_particle_count):
    """
    This is basically how they calculate AQI from PM2.5 levels
    Different number ranges mean different things for air quality
    """
    if tiny_particle_count <= 30:
        return (tiny_particle_count / 30) * 50
    elif tiny_particle_count <= 60:
        return 50 + ((tiny_particle_count - 30) / 30) * 50
    elif tiny_particle_count <= 90:
        return 100 + ((tiny_particle_count - 60) / 30) * 50
    elif tiny_particle_count <= 120:
        return 200 + ((tiny_particle_count - 90) / 30) * 100
    elif tiny_particle_count <= 250:
        return 300 + ((tiny_particle_count - 120) / 130) * 100
    else:
        return 400 + ((tiny_particle_count - 250) / 250) * 100

def what_kind_of_air_is_this(aqi_value):
    """Turn that AQI number into plain English that makes sense"""
    if aqi_value <= 50:
        return "really great air"
    elif aqi_value <= 100:
        return "pretty good air"
    elif aqi_value <= 200:
        return "okay air, not terrible"
    elif aqi_value <= 300:
        return "not so great air"
    elif aqi_value <= 400:
        return "pretty bad air"
    else:
        return "really dangerous air"

def what_should_you_do_about_this_air(aqi_level):
    """Give practical advice about what to do with this air quality"""
    if aqi_level <= 50:
        return {
            'emoji': '😊',
            'label': 'Fantastic air quality!',
            'advice': 'This is about as good as air gets - perfect for being outside!',
            'suggestions': '• Outdoor exercise is great\n• Perfect for picnics\n• Open those windows wide',
            'health_info': 'No health concerns at all with air this clean'
        }
    elif aqi_level <= 100:
        return {
            'emoji': '🙂',
            'label': 'Good air quality',
            'advice': 'The air is totally fine for pretty much everything.',
            'suggestions': '• Normal outdoor activities\n• Walking and light exercise\n• Nothing to worry about really',
            'health_info': 'Might bother extremely sensitive people just a bit'
        }
    elif aqi_level <= 200:
        return {
            'emoji': '😐',
            'label': 'Moderate air quality',
            'advice': 'People with breathing issues might want to take it a bit easier.',
            'suggestions': '• Maybe take outdoor breaks\n• Sensitive folks should rest more\n• Keep windows closed sometimes',
            'health_info': 'Could bother people with asthma or allergies'
        }
    elif aqi_level <= 300:
        return {
            'emoji': '😷',
            'label': 'Poor air quality',
            'advice': 'Most people will notice the air quality is not great.',
            'suggestions': '• Better to stay inside mostly\n• Air filters help if you have them\n• Masks are a good idea outside',
            'health_info': 'Might cause breathing issues for many people'
        }
    elif aqi_level <= 400:
        return {
            'emoji': '😨',
            'label': 'Very poor air quality',
            'advice': 'This air could seriously affect everyone.',
            'suggestions': '• Definitely stay indoors\n• Keep air purifiers running\n• Avoid being outside much',
            'health_info': 'Even healthy people might feel some effects'
        }
    else:
        return {
            'emoji': '💀',
            'label': 'Dangerous air quality',
            'advice': 'This is emergency-level air quality - be careful.',
            'suggestions': '• Absolutely stay inside\n• Use good air purifiers\n• Consider temporary relocation',
            'health_info': 'Serious health risk for everyone exposed'
        }

def show_some_air_examples():
    """Show what air quality looks like in different situations"""
    print("\n" + "~" * 45)
    print("Just to give you an idea, here's how air quality varies:")
    print("~" * 45)
    
    # Some typical air quality scenarios
    different_air_scenarios = [
        {"situation": "Clean mountain area", "tiny_particles": 12, "dust_particles": 22},
        {"situation": "Average suburban area", "tiny_particles": 28, "dust_particles": 52},
        {"situation": "Busy urban area", "tiny_particles": 55, "dust_particles": 95},
        {"situation": "Industrial zone", "tiny_particles": 110, "dust_particles": 185}
    ]
    
    for scenario in different_air_scenarios:
        estimated_aqi = calculate_aqi_based_on_particles(scenario['tiny_particles'])
        air_details = what_should_you_do_about_this_air(estimated_aqi)
        print(f"\n{scenario['situation']}:")
        print(f"  {air_details['emoji']} {air_details['label']}")
        print(f"  (PM2.5 around {scenario['tiny_particles']}, PM10 around {scenario['dust_particles']})")
    
    time.sleep(1.5)

def ask_about_current_air():
    """Ask about the air quality where you are right now"""
    print("\n" + "=" * 48)
    print("So what's the air like around you today?")
    print("=" * 48)
    
    print("\nCan you tell me about the particle levels in your area?")
    print("(You can usually find these on weather apps or air quality websites)")
    
    # Get PM2.5 reading
    while True:
        try:
            current_pm25 = float(input("\nWhat's the PM2.5 level where you are? "))
            if current_pm25 < 0:
                print("That doesn't seem right - particle levels can't be negative!")
                continue
            if current_pm25 > 500:
                print("Wow, that's extremely high! Are you sure about that number?")
                continue
            break
        except:
            print("Just type a number please, like 25 or 40?")
    
    # Get PM10 reading
    while True:
        try:
            current_pm10 = float(input("And what about PM10 level? "))
            if current_pm10 < 0:
                print("Dust levels can't be negative either...")
                continue
            if current_pm10 > 600:
                print("That's seriously dusty! Maybe double-check that?")
                continue
            break
        except:
            print("Maybe try something like 50 or 75?")
    
    return current_pm25, current_pm10

def create_personal_air_report(your_pm25, your_pm10, calculated_aqi, air_advice, past_comparisons=None):
    """Create a personalized report about your air quality situation"""
    print("\n" + "💫" * 20)
    print("   YOUR AIR QUALITY SUMMARY")
    print("💫" * 20)
    
    print(f"\n{air_advice['emoji']} {air_advice['label']}")
    print(f"Estimated AQI: {calculated_aqi:.0f}")
    print(f"PM2.5 level: {your_pm25:.1f} μg/m³")
    print(f"PM10 level: {your_pm10:.1f} μg/m³")
    
    print(f"\nWhat this means health-wise:")
    print(f"   {air_advice['health_info']}")
    
    print(f"\nMy suggestions:")
    print(f"   {air_advice['advice']}")
    
    print(f"\nThings to consider doing today:")
    print(f"   {air_advice['suggestions']}")
    
    if past_comparisons is not None and len(past_comparisons) > 0:
        print(f"\nFor context:")
        worst_comparison = past_comparisons.loc[past_comparisons['AQI'].idxmax()]
        best_comparison = past_comparisons.loc[past_comparisons['AQI'].idxmin()]
        
        print(f"   Similar to air in {worst_comparison['City']} back in {worst_comparison['Date']}")
        print(f"   Better than {best_comparison['City']} in {best_comparison['Date']}")

def train_ml_model(cleaned_data):
    """Trains a Random Forest ML model on the historical data"""
    print("\n[ML] Training Random Forest model on historical data...")
    X = cleaned_data[['PM2.5', 'PM10']]
    y = cleaned_data['AQI']
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    
    # This actually trains the machine learning model
    model.fit(X, y)
    print("[ML] Model trained successfully!")
    return model

def main_air_quality_check():
    """The main air quality checking process"""
    print("🌤️  Machine Learning Air Quality Checker")
    print("Let's see what the air is like for you today...")
    
    # Try to load the data file
    air_data_file = get_that_air_data_file()
    if air_data_file is None:
        print("Sorry, I really need that data file to help you out properly.")
        return
    
    # Clean up the data
    cleaned_air_data = clean_up_the_air_numbers(air_data_file)
    
    # --- THIS IS THE NEW ML PART ---
    aqi_model = train_ml_model(cleaned_air_data)
    
    # Show some examples first
    show_some_air_examples()
    
    # Get current air quality info
    user_pm25, user_pm10 = ask_about_current_air()
    
    # Analyze the situation
    print("\nLet the ML model analyze this for a second...")
    time.sleep(1.5)
    
    # --- USE THE ML MODEL TO PREDICT ---
    # Need to pass as a DataFrame with valid feature names to avoid warnings
    input_data = pd.DataFrame([[user_pm25, user_pm10]], columns=['PM2.5', 'PM10'])
    ml_predicted_aqi = aqi_model.predict(input_data)[0]
    
    _, similar_historical_days = find_days_with_similar_air(user_pm25, user_pm10, cleaned_air_data)
    air_recommendations = what_should_you_do_about_this_air(ml_predicted_aqi)
    
    # Provide the personalized report
    create_personal_air_report(user_pm25, user_pm10, ml_predicted_aqi, air_recommendations, similar_historical_days)
    
    # Final thoughts
    print("\n" + "🌬️" * 18)
    print("Remember: Air quality changes throughout the day!")
    print("Hope the air treats you well today!")


def quick_air_lookup(small_particles, large_particles):
    """
    Quick air quality check if you just want a fast answer
    """
    air_data = get_that_air_data_file()
    if air_data is None:
        return "Need that data file to help you"
    
    cleaned_data = clean_up_the_air_numbers(air_data)
    aqi_estimate, _ = find_days_with_similar_air(small_particles, large_particles, cleaned_data)
    recommendations = what_should_you_do_about_this_air(aqi_estimate)
    
    return {
        'aqi': round(aqi_estimate),
        'air_quality': recommendations['label'],
        'suggestion': recommendations['advice'],
        'symbol': recommendations['emoji'],
        'health_note': recommendations['health_info']
    }

# This runs when you start the script directly
if __name__ == "__main__":
    try:
        main_air_quality_check()
    except KeyboardInterrupt:
        print("\n\nOkay, no problem! Come back anytime you want to check air quality! 👋")
    except Exception as e:
        print(f"\nWell that didn't work properly: {e}")
        print("Let's try again another time!")