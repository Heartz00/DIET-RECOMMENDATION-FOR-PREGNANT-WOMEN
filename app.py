import pandas as pd
import dill as pickle
import streamlit as st
from PIL import Image
import base64
def main():
    def add_bg_from_local(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    add_bg_from_local('background.png') 
    

    #loading the recommendation dataframe
    df = pd.read_csv('recommend_data.csv')
    def recommend(caloric_level, caloric_value, n=10):
        # Filter the dataset based on the caloric level
        filtered_data = df[df['caloric level'] == caloric_level]

        # Sort the diets based on some criteria (e.g., nutrients)
        sorted_diets = filtered_data.sort_values(by=['Energ_Kcal'], ascending=False)

        # Return the top n recommended diets
        dff = sorted_diets
        recommended_diets = dff[(dff['Energ_Kcal'] >= caloric_value) & (dff['Energ_Kcal'] <= caloric_value + 100)]

        return recommended_diets.head(n)

    def nutrient(age, height, weight, preg_stage, active):
        if active.lower() == 'sedentary':
            active = 1.2
        elif active.lower() == "light active":
            active = 1.375
        elif active.lower() == "moderately active":
            active = 1.55
        elif active.lower() == "very active":
            active = 1.75

        bmi = weight / (height * height)
        if bmi < 18.5:
            person = 'Underweight'
            if preg_stage.lower() == "firsttrimester":
                goal = 2
            elif preg_stage.lower() == "secondtrimester":
                goal = 10
            elif preg_stage.lower() == "thirdtrimester":
                goal = 18
        elif bmi >= 18.5 and bmi <= 25:
            person = 'Health in Weight'
            if preg_stage.lower() == "firsttrimester":
                goal = 2
            elif preg_stage.lower() == "secondtrimester":
                goal = 10
            elif preg_stage.lower() == "thirdtrimester":
                goal = 16
        elif bmi > 25:
            person = 'Overweight'
            if preg_stage.lower() == "firsttrimester":
                goal = 2
            elif preg_stage.lower() == "secondtrimester":
                goal = 7
            elif preg_stage.lower() == "thirdtrimester":
                goal = 11

        # Mifflin-St Jeor BMR equation to get the BMR formula
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

        # Needed calories = BMR multiplied by the activity level
        caloric_intake = bmr * float(active)

        return caloric_intake

    def calorie_classify(caloric_intake):
        if caloric_intake < 300:
            classification = "low"
        elif caloric_intake >= 300 and caloric_intake <= 350:
            classification = "mid"
        else:
            classification = "high"

        return classification




    st.title("Pregnant Women Diet Recommender")

    # Collect user input using Streamlit input elements
    age = st.number_input("Enter your age in years:", min_value=0, value=25)
    height = st.number_input("Enter your height in meters:", min_value=0.0, value=1.6, step=0.01)
    weight = st.number_input("Enter your weight in kilograms:", min_value=0.0, value=60.0, step=0.1)
    preg_stage = st.selectbox("Enter your pregnancy stage:", ("FirstTrimester", "SecondTrimester", "ThirdTrimester"))
    active = st.selectbox("Enter your activity level:", ("Sedentary", "Light Active", "Moderately Active", "Very Active"))

    # Calculate caloric intake
    caloric_intake = nutrient(age, height, weight, preg_stage, active)

    # Classify caloric intake
    caloric_classification = calorie_classify(caloric_intake)

    # Display the result using Streamlit components
    st.write("Your recommended caloric intake is:", caloric_intake, "calories per day.")
    st.write("Caloric Intake Classification:", caloric_classification)

    # Recommend diets based on caloric classification and caloric intake
    result = recommend(caloric_classification, caloric_intake, n=5)
    st.write("Top 5 Recommended Diets:")
    st.dataframe(result[['Shrt_Desc', 'Energ_Kcal']].set_index([pd.Index(['1', '2', '3', '4', '5'])]))

if __name__ == "__main__":
    main()
 
