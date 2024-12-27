import json
import os
import openai
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


def extract_titles_from_items(items, category, title_data):
    print(f'Extracting titles from category: {category}')

    if not items:
        raise ValueError(f"No items found for category: {category}")

    # Lưu tiêu đề mà không tải ảnh
    category_key = f"category-{category}"
    if category_key not in title_data:
        title_data[category_key] = {}

    for item in items:
        asin = item['asin']
        title = item.get('title', 'Unknown Title')
        concise_title = generate_concise_title_gpt4o(title)
        title_data[category_key][asin] = concise_title

    print(f"Extracted {len(items)} titles for category: {category}")
    return title_data

def save_category_titles(output_dir, category, items):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    category_data = {}
    category_data[category] = {}

    for item in items:
        asin = item.get('asin')
        title = item.get('title', 'Unknown Title')
        concise_title = generate_concise_title_gpt4o(title)
        category_data[category][asin] = concise_title

    output_file = os.path.join(output_dir, f"{category}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(category_data, f, indent=4, ensure_ascii=False)

    print(f"Saved concise titles for category {category} to {output_file}")