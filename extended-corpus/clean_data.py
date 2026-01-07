
import os
import json
import glob

SOURCE_DIR = r"f:\Corpus\extended-corpus"
OUTPUT_DIR = os.path.join(SOURCE_DIR, "cleaned_data")

def clean_data():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

    # Find all json files
    json_files = glob.glob(os.path.join(SOURCE_DIR, "*.json"))
    
    global_id_counter = 1
    total_count = 0
    
    for json_file in json_files:
        filename = os.path.basename(json_file)
        # Skip package.json or other non-data files if they exist (though list_dir only showed project jsons)
        if filename == "package.json": 
            continue
            
        print(f"Processing {filename}...")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            cleaned_items = []
            
            # Data is expected to be a list of objects
            if not isinstance(data, list):
                print(f"Warning: {filename} does not contain a list of objects. Skipping.")
                continue
                
            for item in data:
                # Extract required fields. Use .get() to handle potential missing fields gracefully, 
                # though schema suggests they should be there.
                
                # Construct the cleaned object
                oracle = item.get("oracle", {})
                cleaned_item = {
                    "case_id": global_id_counter,
                    "project_name": item.get("projectName"),
                    "filename": item.get("filename"),
                    "class_name": item.get("host_class_name"),
                    "function_name": item.get("host_functionName"),
                    "function_start_line": item.get("host_start_line"),
                    "function_end_line": item.get("host_end_line"),
                    "oracle_start_line": oracle.get("line_start") if oracle else None,
                    "oracle_end_line": oracle.get("line_end") if oracle else None,
                    "sha_before_ef": f"https://github.com/{item.get('projectName')}/tree/{item.get('sha_before_ef')}",
                    "sha_ef": f"https://github.com/{item.get('projectName')}/tree/{item.get('sha_ef')}"
                }
                
                cleaned_items.append(cleaned_item)
                global_id_counter += 1
            
            total_count += len(cleaned_items)
            
            if not cleaned_items:
                print(f"Skipping {filename} (0 items)")
                continue

            # Save cleaned data
            output_path = os.path.join(OUTPUT_DIR, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(cleaned_items, f, indent=4)
                
            print(f"Saved {len(cleaned_items)} items to {output_path}")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print("-" * 30)
    print(f"Total extracted items: {total_count}")
    print("-" * 30)

if __name__ == "__main__":
    clean_data()
