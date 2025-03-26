from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Initialize the Flask application
app = Flask(__name__)

# Configure Gemini API
genai.configure(
    api_key="AIzaSyBATgziNhrFFuCb72gKY-ONPBmfpfb86mY"
)  # Replace with your actual Gemini API key

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-002")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_meal():
    # Retrieve form data
    carbs = request.form.get("carbs")
    protein = request.form.get("protein")
    fat = request.form.get("fat")
    meal_type = request.form.get("meal_type")
    cuisine_type = request.form.get("cuisine_type")

    # Create the prompt
    prompt = f"""Create a detailed {meal_type} meal plan with approximately:
    - {carbs}g carbohydrates
    - {protein}g protein
    - {fat}g fat
    The meal should be inspired by {cuisine_type} cuisine.
    
    Please include:
    1. Meal name
    2. Ingredients list
    3. Preparation instructions
    4. Nutritional breakdown"""

    try:
        # Call Gemini API with updated safety settings
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.7, top_p=0.8),
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
            ],
        )

        if response.text:
            meal_plan = response.text
            return jsonify({"meal_plan": meal_plan.strip()})
        else:
            return jsonify({"error": "No response generated"}), 500

    except Exception as e:
        return jsonify({"error": f"Error generating meal plan: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
