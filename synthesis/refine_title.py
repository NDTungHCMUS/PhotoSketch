import os
import json
import openai

# Directory containing the JSON files
DATA_DIR = "amazon"

# Configure OpenAI API key
openai.api_key = "hidden"

def generate_concise_title_gpt4o(product_title):
    """
    Sends a product title to OpenAI GPT-4o API to generate a concise user-friendly version.
    """
    prompt = f"""
    You are a helpful assistant that generates concise and user-friendly versions of detailed product titles for search optimization. Your goal is to make the title shorter and more relevant to what a user might type into a search bar. Below are examples:

    Example 1:
    Original Title: "Ninja Griddle and Indoor Grill, 14’’, Electric Grill, For Steak, Burgers, Salmon, Veggies, and More, Pancake Griddle, Nonstick, Dishwasher Safe, 500F, Even Cooking, Silver, GR101"
    Concise Search Content: "griddle and indoor grill"

    Example 2:
    Original Title: "Vacuum Sealer Machine, 80Kpa Food Vacuum Sealer Machine with Double Pump, Dry/Moist, Pulse Mode, Handle Locked Design, LED Indicator Light & Cutter,12MM Widened Heating Strip"
    Concise Search Content: "vacuum sealer machine"

    Now, generate a concise and user-friendly version for the following title:

    Original Title: "{product_title}"

    Concise Search Content:
    """
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=50,
            temperature=0.5,
            n=1,
        )

        # Extract and return the concise title
        concise_title = response.choices[0].text.strip().strip('"')
        return concise_title
    except Exception as e:
        print(f"Error during API call: {e}")
        return None

def process_json_file(file_path):
    """
    Process a single JSON file to generate concise search content for product titles.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        for product in data:
            if "title" in product:
                original_title = product["title"]
                concise_title = generate_concise_title_gpt4o(original_title)
                product["concise_title"] = concise_title  # Add the concise title to the product
            
        # Save updated data back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
            print(f"Updated file: {file_path}")
    
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def main():
    """
    Main function to process all JSON files in the specified directory.
    """
    for file_name in os.listdir(DATA_DIR):
        if file_name.endswith('.json'):
            file_path = os.path.join(DATA_DIR, file_name)
            print(f"Processing file: {file_path}")
            process_json_file(file_path)

if __name__ == "__main__":
    main()
