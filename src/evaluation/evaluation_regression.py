from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
def evaluate_regression(model, X_test, y_test):
    y_pred_log = model.predict(X_test)

    #We use it, becaue we compare the predicted log values with the actual log values of the target variable.
    #It will give us a more accurate evaluation of the model's performance in terms of how well it predicts the actual target variable, rather
    y_test_actual = np.expm1(y_test) 
    y_pred_actual = np.expm1(y_pred_log)  

    mse = mean_squared_error(y_test_actual, y_pred_actual)
    mae = mean_absolute_error(y_test_actual, y_pred_actual)
    r2 = r2_score(y_test_actual, y_pred_actual)

    print("Mean Squared Error:", mse)
    print("Mean Absolute Error:", mae)
    print("R^2 Score:", r2)

    return {
        "mean_squared_error": mse,
        "mean_absolute_error": mae,
        "r2_score": r2
    }