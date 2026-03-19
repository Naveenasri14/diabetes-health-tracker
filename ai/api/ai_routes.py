from flask import Blueprint, request, jsonify
from services.prediction_service import predict_diabetes
from services.recommendation_service import get_recommendation

ai_routes = Blueprint("ai_routes", __name__)

@ai_routes.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        prediction, probability = predict_diabetes(data)

        recommendation = get_recommendation(prediction)

        return jsonify({
            "prediction": int(prediction),
            "risk_percentage": round(probability * 100, 2),
            "recommendation": recommendation
        })

    except Exception as e:
        return jsonify({"error": str(e)})