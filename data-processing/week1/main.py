import pandas as pd
import datetime

today = datetime.date.today()
#print(today)

df = pd.read_csv('/Users/franklin/Documents/git/data-eng/data-processing/storage/data2.csv')

#df.isnull().sum()
columns_to_keep = ['Duration', 'Date', 'Pulse', 'Maxpulse']


# Lower case the columns
df = df[columns_to_keep]
df.columns = df.columns.str.lower()

def clean_duration(x):
    # Fix values for example, 450 which should be 45. Less than 1 minute.
    if isinstance(x, int) and len(str(x)) > 3:
        return int(str(x)[:2])
    return x

# Normalize date formats
def normalize_date(date):
    if pd.isnull(date):
        return today.strftime('%Y/%m/%d')
    date = str(date).replace("'", "")
    if len(date) == 8 and date.isdigit():
        return f"{date[:4]}/{date[4:6]}/{date[6:]}"
    return date

# Replace the incorrect value 450 with 45
df['duration'] = df['duration'].apply(clean_duration)

# Normalize the date format
df['date'] = df['date'].apply(normalize_date)

# Convert the date to datetime format and then to string
df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d', errors='coerce').dt.strftime('%Y-%m-%d')

# Check for duplicates
duplicates = df.duplicated()
print(f"Number of duplicates: {duplicates.sum()}")

# Remove duplicates
df.drop_duplicates(inplace=True)

# Recalculate duplicates after dropping them
duplicates = df.duplicated()
print(f"Number of duplicates after drop: {duplicates.sum()}")


# Check for missing values
print(df.isnull().sum())

print(df)
