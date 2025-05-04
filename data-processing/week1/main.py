import pandas as pd
import datetime

today = datetime.date.today()
#print(today)

df = pd.read_csv('/Users/franklin/Documents/git/data-eng/data-processing/storage/data2.csv')

df = pd.DataFrame(df)
#df.notnull().sum()
columns_to_keep = ['Duration', 'Date', 'Pulse', 'Maxpulse']


# Lower case the columns
df = df[columns_to_keep]
df.columns = df.columns.str.lower()

# Replace the incorrect value 450 with 45
df['duration'] = df['duration'].apply(lambda x: int(str(x)[:2]) if isinstance(x, int) and len(str(x)) == 3 else x)

# Remove quotes in the date format
df['date'] = df['date'].str.replace("'", "")

# Fill missing dates with a default value
df['date'] = df['date'].fillna(today.strftime('%Y/%m/%d'))

# Normalize date formats
def normalize_date(date):
    date = str(date)
    if len(date) == 8 and date.isdigit():  # Handle 'YYYYMMDD' format
        return f"{date[:4]}/{date[4:6]}/{date[6:]}"
    return date

df['date'] = df['date'].apply(normalize_date)

# Convert to standard date format
df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d', errors='coerce').dt.strftime('%Y-%m-%d')

print(df.value_counts())
df.drop_duplicates(inplace=True)

#print(df)

print(df.value_counts())
print(df.notnull().sum())
