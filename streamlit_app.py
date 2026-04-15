# Code written was written/assisted by Google Gemini
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Maternal Health Data Analysis", layout="wide")

# 2. Dataset Construction
data = {
    'Year': [1841, 1842, 1843, 1844, 1845, 1846, 1847, 1848, 1849] * 2,
    'Birth': [3036, 3287, 3060, 3157, 3492, 4010, 4010, 3742, 3500,
              2442, 2659, 2739, 2956, 3241, 3754, 3754, 3600, 3400],
    'Deaths': [237, 518, 274, 260, 241, 459, 122, 47, 46,
               86, 202, 164, 68, 66, 105, 48, 48, 36],
    'Clinic': ['Clinic 1'] * 9 + ['Clinic 2'] * 9
}
df = pd.DataFrame(data)
df['Mortality Rate'] = df['Deaths'] / df['Birth']

# 3. Header & Project Context
st.title("The Impact of Antiseptics on Maternal Mortality")
st.write("""
This dashboard looks at clinic birth and death data over time. Compared are two clinics that Dr. Ignaz Semmelweis investigated to 
figure out why childbed fever affected onw more that the other in the 1840s. After further investigation, Dr. Semmelweis discovered 
that the clinic with higher mortality rates had doctors and medical students who would perform autopsies on dead patients and then 
deliver babies without washing their hands. The other clinic was staffed by midwives who didn't perform autopsies and had much lower
mortality rates . Dr. Semmelweis's suggested intervention was handwashing which saved maternal lives after introduction in 1847.
""")

# 4. Interactive Year Slider
st.divider()
years = st.slider(
    "Select Year Range for Analysis",
    min_value=1841, max_value=1849, value=(1841, 1847)
)

# Filtering logic (Clinics are no longer filtered)
filtered_df = df[df['Year'].between(years[0], years[1])]

# 5. Main Visualization
st.subheader("Historical Mortality Trends")

fig = px.line(
    filtered_df, x='Year', y='Mortality Rate', color='Clinic',
    color_discrete_map={'Clinic 1': '#0072B2', 'Clinic 2': '#89CFF0'},
    markers=True
)

if years[0] <= 1847 <= years[1]:
    fig.add_vline(x=1847, line_dash="dot", line_color="red", 
                  annotation_text="Handwashing Policy Enacted")

fig.update_layout(
    yaxis_tickformat='.1%', 
    template='plotly_white', 
    hovermode="x unified",
    xaxis=dict(dtick=1)
)
st.plotly_chart(fig, use_container_width=True)

# 6. Comparative Metrics
st.subheader(f"Statistical Change: {years[0]} vs {years[1]}")
m_col1, m_col2 = st.columns(2)

def calculate_delta(name):
    clinic_data = df[df['Clinic'] == name]
    try:
        start_rate = clinic_data[clinic_data['Year'] == years[0]]['Mortality Rate'].values[0]
        end_rate = clinic_data[clinic_data['Year'] == years[1]]['Mortality Rate'].values[0]
        change = (end_rate - start_rate) / start_rate
        return end_rate, change
    except IndexError:
        return None, None

# Clinic 1 Metric
rate1, delta1 = calculate_delta('Clinic 1')
if rate1 is not None:
    m_col1.metric("Clinic 1 Mortality", f"{rate1:.2%}", f"{delta1:.1%}", delta_color="inverse")

# Clinic 2 Metric
rate2, delta2 = calculate_delta('Clinic 2')
if rate2 is not None:
    m_col2.metric("Clinic 2 Mortality", f"{rate2:.2%}", f"{delta2:.1%}", delta_color="inverse")

# 7. Summary Observations (Updated Section)
st.divider()
st.subheader("Short Explanation of Findings")
st.write("""
The data shows that Clinic 1, which was the hospital, had much higher death rates from childbed fever 
than Clinic 2, which was the midwife-led clinic, despite similar numbers of births. Following the introduction of handwashing 
in 1847, the mortality rate in Clinic 1 fell immensely and started to follow Clinic 2’s levels. 
This showed strong evidence that implementation of handwashing was significant in reducing maternal deaths.
""")

# 8. Data Inspection
with st.expander("Explore Dataset"):
    st.table(filtered_df.sort_values(['Year', 'Clinic']))