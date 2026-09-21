import pandas as pd
import matplotlib.pyplot as plt

# STEP 1: Load the data
# This assumes carrier.csv is sitting in the SAME folder as this script.
df = pd.read_csv("carrier.csv")

# STEP 2: Build a proper date column from the separate Year and Month columns
df["Date"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2) + "-01")

# STEP 3: Chart 1 -- how full flights are (load factor), by airline
# Keep only regular scheduled domestic flights (excludes charters and industry totals)
airlines = ["IndiGo", "Air India", "SpiceJet", "Akasa Air", "Vistara"]
airline_df = df[(df["Type"] == "ScheduledDomestic") & (df["Airline"].isin(airlines))]

pivot_load = airline_df.pivot_table(index="Date", columns="Airline", values="Passenger Load Factor")

fig1, ax1 = plt.subplots(figsize=(12, 6))
for airline in airlines:
    if airline in pivot_load.columns:
        ax1.plot(pivot_load.index, pivot_load[airline], label=airline, linewidth=2)
ax1.set_title("Domestic Passenger Load Factor by Airline\n(% of seats filled on average, per month)")
ax1.set_xlabel("Year")
ax1.set_ylabel("Load Factor (%)")
ax1.legend()
ax1.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("load_factor_trend.png", dpi=150, bbox_inches="tight")
print("Step 1 done: load_factor_trend.png saved")

# STEP 4: Chart 2 -- total industry-wide passenger traffic over time
# "Total Domestic" is a single row DGCA reports covering the whole industry, not one airline
industry_df = df[(df["Type"] == "ScheduledDomestic") & (df["Airline"] == "Total Domestic")].sort_values("Date")

fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.plot(industry_df["Date"], industry_df["Passenger Number"], color="darkred", linewidth=2)
ax2.set_title("Total Domestic Air Passengers in India, 2015-2026\n(Shows the COVID-19 crash and recovery)")
ax2.set_xlabel("Year")
ax2.set_ylabel("Passengers per Month")
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("industry_growth_trend.png", dpi=150, bbox_inches="tight")
print("Step 2 done: industry_growth_trend.png saved")
