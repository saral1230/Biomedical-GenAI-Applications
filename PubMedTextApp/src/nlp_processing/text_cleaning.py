import re
import json

json_file = '/Users/xuying/App/literature_graph_tool/scripts/pubmed_articles.json'

# Load the JSON file
with open(json_file, "r") as f:
    data = json.load(f)



# Extract abstracts from all articles
def abstract_generator(data):
    """Yield abstracts from the JSON data one by one."""
    for article in data:
        if "abstract" in article:
            yield article["abstract"]

# Create a generator
abstracts_gen = abstract_generator(data)

# Get the first 3 abstracts
for _ in range(3):
    print(next(abstracts_gen))
    print("---")

def clean_text(text):
    """Remove special characters, multiple spaces, and normalize case."""
    text = re.sub(r'\s+', ' ', text)  # Remove multiple spaces
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text.strip().lower()

'''
# Check the structure (print first entry)
print(json.dumps(data[0], indent=2))

# Example usage
if __name__ == "__main__":
    raw_text = "This is an example!  Multiple    spaces & special characters."
    print(clean_text(raw_text))  # Output: "this is an example multiple spaces special characters"'''