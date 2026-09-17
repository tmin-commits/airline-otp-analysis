import pandas as pd
import matplotlib.pyplot as plt

# STEP 1: Load the data
# This assumes daily.csv is sitting in the SAME folder as this script.
df = pd.read_csv("daily.csv")

# STEP 2: Parse the date and tag each row with a season
df["Date"] = pd.to_datetime(df["Date"])


def get_season(month):
    if month in [6, 7, 8, 9]:
        return "Monsoon"
    elif month in [12, 1]:
        return "Fog"
    else:
        return "Other"


df["Season"] = df["Date"].dt.month.apply(get_season)

# STEP 3: Pull out just the On-Time-Performance columns
otp_cols = [c for c in df.columns if c.startswith("On Time Performance")]
airline_names = [c.replace("On Time Performance (", "").replace(")", "") for c in otp_cols]

clean_df = df[["Date", "Season"] + otp_cols].copy()
clean_df.columns = ["Date", "Season"] + airline_names

# STEP 4: Convert "99.8%" style text into real numbers
for col in airline_names:
    clean_df[col] = clean_df[col].astype(str).str.replace("%", "", regex=False)
    clean_df[col] = pd.to_numeric(clean_df[col], errors="coerce")

# STEP 5: Drop days where every airline is missing data
clean_df = clean_df.dropna(subset=airline_names, how="all")

# Save the cleaned table so you can open it in Excel if you want to look at it
clean_df.to_csv("otp_clean.csv", index=False)
print(f"Step 1 done: cleaned {len(clean_df)} rows of data")

# STEP 6: Build the chart
airlines_to_plot = ["Indigo", "Air India", "Spicejet", "Akasa Air"]
clean_df["YearMonth"] = clean_df["Date"].dt.to_period("M")
monthly = clean_df.groupby("YearMonth")[airlines_to_plot].mean().reset_index()
monthly["YearMonth"] = monthly["YearMonth"].dt.to_timestamp()

fig, ax = plt.subplots(figsize=(12, 6))
for airline in airlines_to_plot:
    ax.plot(monthly["YearMonth"], monthly[airline], label=airline, linewidth=2)

start_year = monthly["YearMonth"].dt.year.min()
end_year = monthly["YearMonth"].dt.year.max()
for year in range(start_year, end_year + 1):
    ax.axvspan(pd.Timestamp(f"{year}-06-01"), pd.Timestamp(f"{year}-09-30"), color="blue", alpha=0.07)
    ax.axvspan(pd.Timestamp(f"{year}-12-01"), pd.Timestamp(f"{year + 1}-01-31"), color="gray", alpha=0.07)

ax.set_title("On-Time Performance by Indian Airline\nBlue = Monsoon (Jun-Sep) | Gray = Fog Season (Dec-Jan)")
ax.set_xlabel("Month")
ax.set_ylabel("On-Time Performance (%)")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("otp_trend.png", dpi=150, bbox_inches="tight")

print("Step 2 done: chart saved as otp_trend.png -- open it from your folder to view it")
