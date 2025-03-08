# Sales Prediction Using Advertising Data

## Introduction
This project predicts sales revenue based on advertising budgets across different media platforms. By leveraging machine learning models, we aim to understand the relationship between **TV, Radio, and Newspaper** advertising expenditures and **sales performance**.

## Dataset
The dataset, **Advertising.csv**, consists of:
- **TV Advertising:** Budget spent on TV ads
- **Radio Advertising:** Budget spent on radio ads
- **Newspaper Advertising:** Budget spent on newspaper ads
- **Sales:** Revenue generated

## Project Goals
- Develop a predictive model for sales based on advertising spending.
- Analyze the impact of different media on sales.
- Evaluate model performance using standard metrics.

## Methodology
1. **Data Preprocessing:** Clean data, handle missing values, and remove outliers.
2. **EDA:** Analyze the relationship between advertising budgets and sales.
3. **Model Development:** Train multiple regression models including:
   - Linear Regression
   - Decision Trees
   - Random Forest
   - XGBoost Regressor
4. **Evaluation:** Assess performance using RMSE, MAE, and R² score.

## Observations
- **TV Advertising:** Strongest correlation with sales.
- **Radio Advertising:** Moderate impact on sales.
- **Newspaper Advertising:** Weakest correlation, indicating low impact.
- **Interaction Effects:** Combining TV and Radio budgets enhances sales predictions.

## Conclusion
This project demonstrates how advertising budgets impact sales and how machine learning can improve revenue forecasting. The best-performing model, **XGBoost Regressor**, achieved the lowest RMSE, making it the most reliable predictor.

## Technologies Used
- Python, Pandas, NumPy
- Scikit-learn, XGBoost
- Matplotlib, Seaborn

## How to Use
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sales-prediction.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python train_model.py
   ```

## Future Enhancements
- Include additional marketing channels.
- Implement deep learning models for improved accuracy.
- Develop an interactive dashboard for sales forecasting.
