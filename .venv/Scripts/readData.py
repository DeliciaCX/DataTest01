import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Read the JSON file
df = pd.read_json('amazon_uk_shoes_dataset.json')

# Clean empty cells
new_df = df.dropna(subset=['price'])

# Print the DataFrame columns to confirm column names
print("Columns in DataFrame:", new_df.columns)

# Check if 'price' column exists
if 'price' in new_df.columns:
    # Print first few rows to understand the data format
    print(new_df['price'].head())

    # Function to extract min and max prices
    def extract_min_max(price_range):
        if price_range is None:
            return None, None
        # Check if it contains a hyphen
        if ' - ' in price_range:
            # Split the string on ' - '
            min_price_str, max_price_str = price_range.split(' - ')
        else:
            # Single price, set both min and max to the same value
            min_price_str = max_price_str = price_range

        # Remove pound signs and commas, then convert to floats
        min_price = float(min_price_str.replace('£', '').replace(',', '').strip())
        max_price = float(max_price_str.replace('£', '').replace(',', '').strip())

        return min_price, max_price

    # Apply the function to extract min and max prices
    new_df[['min_price', 'max_price']] = new_df['price'].apply(lambda x: pd.Series(extract_min_max(x)))

    print(new_df[['price', 'min_price', 'max_price']])
else:
    print("The 'price' column is not found in the DataFrame.")

# Filter rows where max_price > 2000
luxury_items = new_df[new_df['max_price'] > 2000]

# Print details of luxury items
for index, row in luxury_items.iterrows():
    print("Luxury Item details:")
    print(row)

# Scatter plot of min_price vs. max_price
x = new_df['min_price']
y = new_df['max_price']

plt.scatter(x, y)
plt.xlabel("MIN")
plt.ylabel("MAX")
plt.title("Scatter plot of Min Price vs Max Price")
plt.show()
