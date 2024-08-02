import pandas as pd
import matplotlib.pyplot as plt

# Read the JSON file
df = pd.read_json('amazon_uk_shoes_dataset.json')

# Clean empty cells
new_df = df.dropna(subset=['price', 'brand']).copy()

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

# Sort and select top 10 rows for max_price
top_10_luxury_items = new_df.nlargest(10, 'max_price')

# Sort and select top 10 rows for min_price
top_10_affordable_items = new_df.nsmallest(10, 'min_price')

# Save the top 10 reports to CSV files
top_10_luxury_items.to_csv('top_10_luxury_items_report.csv', index=False)
top_10_affordable_items.to_csv('top_10_affordable_items_report.csv', index=False)

print("Reports generated: 'top_10_luxury_items_report.csv' and 'top_10_affordable_items_report.csv'")

# Calculate the median price for each brand
# Here, we consider both min_price and max_price for the median calculation
new_df['price'] = new_df[['min_price', 'max_price']].mean(axis=1)
median_prices_by_brand = new_df.groupby('brand')['price'].median().reset_index()

# Save the median prices report to a CSV file
median_prices_by_brand.to_csv('median_prices_by_brand_report.csv', index=False)

print("Report generated: 'median_prices_by_brand_report.csv'")

# Optional: Print the report
print(median_prices_by_brand)

# Scatter plot of min_price vs. max_price
x = new_df['min_price']
y = new_df['max_price']

plt.scatter(x, y)
plt.xlabel("MIN")
plt.ylabel("MAX")
plt.title("Scatter plot of Min Price vs Max Price")
plt.show()
