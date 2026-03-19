from api.ai_routes import predict

# Sample patient data
data = [6, 148, 72, 35, 0, 33.6, 0.627, 50]

# Call prediction
result = predict(data)

print("Prediction Result:")
print(result)