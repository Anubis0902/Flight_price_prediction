import streamlit as st
import joblib
import pandas as pd
from datetime import date

preprocessor = joblib.load("preprocessing_pipeline.pkl")
model = joblib.load("final_model.pkl")

st.title("✈ Flight Price Prediction App")

airline = st.selectbox(
    "Airline", 
    ['IndiGo', 'Air India', 'SpiceJet', 'Vistara', 'GO_FIRST', 'AirAsia']
)

source_city = st.selectbox(
    "Source City", 
    ['Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai', 'Delhi']
)

destination_city = st.selectbox(
    "Destination City", 
    ['Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai', 'Delhi']
)

departure_time = st.selectbox(
    "Departure Time", 
    ['Early_Morning', 'Morning', 'Afternoon', 'Evening', 'Night', 'Late_Night']
)

arrival_time = st.selectbox(
    "Arrival Time", 
    ['Early_Morning', 'Morning', 'Afternoon', 'Evening', 'Night', 'Late_Night']
)

stops_map = {
    0: "zero",
    1: "one",
    2: "two_or_more"
}
stops_num = st.selectbox("Total Stops", [0, 1, 2])
stops = stops_map[stops_num]

Class = st.selectbox("Class", ["Economy", "Business"])


travel_date = st.date_input("Travel Date")
today = date.today()
days_left = (travel_date - today).days

if days_left < 0:
    st.error("❌ Travel date cannot be in the past")

elif source_city == destination_city:
    st.error("❌ Source and Destination city cannot be the same")

else:
    if st.button("Predict Price"):

        route_duration_map = {
            ("Mumbai", "Delhi"): 120,
            ("Delhi", "Mumbai"): 120,
            ("Mumbai", "Bangalore"): 110,
            ("Bangalore", "Mumbai"): 110,
            ("Delhi", "Chennai"): 150,
            ("Chennai", "Delhi"): 150
        }

        route_avg_duration = route_duration_map.get(
            (source_city, destination_city), 
            130
        )

        input_df = pd.DataFrame([{
            "airline": airline,
            "source_city": source_city,
            "departure_time": departure_time,
            "stops": stops,
            "arrival_time": arrival_time,
            "destination_city": destination_city,
            "class": Class,
            "days_left": days_left,
            "route_avg_duration": route_avg_duration
        }])

        transformed_input = preprocessor.transform(input_df)
        prediction = model.predict(transformed_input)

        price = float(prediction[0])
        st.success(f"💰 Estimated Flight Price: ₹{price:,.2f}")
## Can include range pricing error