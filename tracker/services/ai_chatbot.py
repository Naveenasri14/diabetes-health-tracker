def get_bot_response(message):
    message = message.lower()

    greeting = "👋 Hello! I'm your AI Health Assistant.\n\n"

    # =========================
    # DIABETES MEANING
    # =========================
    if "diabetes" in message and "what" in message:
        return greeting + """🩺 What is Diabetes?

Diabetes is a chronic health condition where your body is unable to properly control blood sugar (glucose) levels.

🔹 Types of Diabetes:
1️⃣ Type 1 – Body does not produce insulin  
2️⃣ Type 2 – Body does not use insulin properly  
3️⃣ Gestational – Occurs during pregnancy  

⚠️ Effects:
• Heart disease ❤️  
• Kidney damage 🧠  
• Vision problems 👁️  
• Nerve damage 🦵  

✅ Management:
• Healthy diet  
• Regular exercise  
• Medication (if required)
"""

    # =========================
    # EXERCISE + YOGA
    # =========================
    elif "exercise" in message or "workout" in message:
        return greeting + """🏃 Exercise for Diabetes

Regular exercise helps control blood sugar and improves health.

🔥 Best Exercises:
• Walking 🚶‍♂️ (30 mins daily)
• Cycling 🚴
• Swimming 🏊
• Light weight training 🏋️

🧘‍♀️ Recommended Yoga:
• Surya Namaskar ☀️
• Pranayama 🌬️
• Bhujangasana 🐍
• Tadasana 🏔️

💡 Tips:
• Check sugar before exercise  
• Stay hydrated 💧  
• Avoid over-exercising
"""

    # =========================
    # FOOD / DIET
    # =========================
    elif "food" in message or "diet" in message:
        return greeting + """🥗 Diet for Diabetes

Eating the right food helps control sugar levels.

✅ Foods to Eat:
• Brown rice 🍚  
• Oats & whole grains 🌾  
• Green vegetables 🥦  
• Fruits (limited) 🍎  
• Lean protein 🍗  

❌ Avoid:
• Sugary drinks 🥤  
• Junk food 🍔  
• White bread 🍞  

💡 Tips:
• Eat small frequent meals  
• Avoid skipping meals  
• Drink plenty of water 💧
"""

    # =========================
    # FOOD SCHEDULE
    # =========================
    elif "schedule" in message or "meal plan" in message:
        return greeting + """📅 Weekly Food Schedule

🍽️ Monday:
Breakfast: Oats + Milk  
Lunch: Brown rice + Veg curry  
Dinner: Chapati + Dal  

🍽️ Tuesday:
Breakfast: Idli + Sambar  
Lunch: Rice + Vegetable  
Dinner: Salad + Soup  

🍽️ Wednesday:
Breakfast: Fruits + Nuts  
Lunch: Roti + Curry  
Dinner: Light salad  

🍽️ Thursday:
Breakfast: Upma  
Lunch: Rice + Dal  
Dinner: Chapati + Veg  

🍽️ Friday:
Breakfast: Oats  
Lunch: Brown rice  
Dinner: Soup + Salad  

🍽️ Saturday:
Breakfast: Idli  
Lunch: Veg meals  
Dinner: Light food  

🍽️ Sunday:
Balanced diet (avoid junk)

💡 Always maintain portion control!
"""

    # =========================
    # FRUITS
    # =========================
    elif "fruit" in message:
        return greeting + """🍎 Fruits for Diabetes

✅ Safe Fruits:
• Apple 🍏  
• Guava  
• Orange 🍊  
• Papaya  

⚠️ High Sugar Fruits (limit):
• Mango 🥭  
• Banana 🍌  
• Grapes 🍇  

💡 Eat fruits in moderation!
"""

    # =========================
    # VEGETABLES
    # =========================
    elif "vegetable" in message or "veggies" in message:
        return greeting + """🥦 Vegetables for Diabetes

✅ Best Vegetables:
• Spinach 🥬  
• Broccoli 🥦  
• Carrot 🥕  
• Cucumber 🥒  

💡 Benefits:
• Low sugar  
• High fiber  
• Improves digestion  

👉 Eat more green vegetables daily!
"""

    # =========================
    # CALCULATION
    # =========================
    elif "calculate" in message:
        return greeting + """🧮 How to Calculate Diabetes?

Diabetes is measured using blood sugar levels.

📊 Normal Values:
• Fasting: 70–99 mg/dL  
• After food: <140 mg/dL  

⚠️ Diabetes:
• Fasting ≥126 mg/dL  
• After food ≥200 mg/dL  

🧪 Tests:
• Fasting Blood Sugar  
• HbA1c Test  
• Oral Glucose Test  

💡 Always consult a doctor for proper diagnosis.
"""

    # =========================
    # DETAILED MODE
    # =========================
    elif "detail" in message:
        return greeting + """📘 Detailed Diabetes Guide

Diabetes affects how your body uses glucose.

🔬 Causes:
• Genetics  
• Poor diet  
• Lack of exercise  

🛡️ Prevention:
• Healthy eating  
• Regular workouts  
• Maintain weight  

💊 Treatment:
• Insulin therapy  
• Medication  
• Lifestyle changes  

🌟 Tip:
Early diagnosis = better control!
"""

    # =========================
    # DEFAULT
    # =========================
    else:
        return greeting + """❓ I can help you with:

• What is diabetes  
• Exercise & yoga  
• Diet & food  
• Weekly meal plan  
• Fruits & vegetables  
• Diabetes calculation  

👉 Please ask related questions 😊
"""