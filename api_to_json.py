import os
import requests
import json


def traverse_directory_and_make_api_call(root_dir, api_url, output_file):
    """Traverses a directory and makes an API call for each image file.

    Args:
        root_dir (str): Root directory to traverse.
        api_url (str): URL of the API to call.
        output_file (str): Path to the output JSON file.
    """
    results = {}

    # Loop through all directories and subdirectories
    for root, dirs, files in os.walk(root_dir):
        # Check if this is one of the ripe, rotten, or unripe directories
        fruit_state = os.path.basename(root)
        if fruit_state in ["ripe", "rotten", "unripe"]:
            # Get the fruit name from the parent directory
            fruit_name = os.path.basename(os.path.dirname(root))

            # Initialize fruit in results if not already present
            if fruit_name not in results:
                results[fruit_name] = {}
            if fruit_state not in results[fruit_name]:
                results[fruit_name][fruit_state] = []

            # Loop through all the files in the current directory
            for file in files:
                # Construct full path to the file
                file_path = os.path.join(root, file)

                # Make API call
                with open(file_path, "rb") as image_file:
                    files = {
                        "fruit_name": (None, fruit_name),
                        "image": (file, image_file),
                    }
                    response = requests.post(api_url, files=files)

                    # Store results
                    entry = {"image": file, "api_response": response.text}
                    results[fruit_name][fruit_state].append(entry)
                    print(
                        f"Processed {file_path} with response: {response.status_code}"
                    )

    # Save the results to a JSON file
    with open(output_file, "w") as json_file:
        json.dump(results, json_file, indent=4)


# Main execution
if __name__ == "__main__":
    # Define root directory, API URL, and output file
    ROOT_DIR = "./Frutas"
    API_URL = "https://ggnxc6nf-17992.use2.devtunnels.ms/get_ripeness"
    OUTPUT_FILE = "results.json"

    traverse_directory_and_make_api_call(ROOT_DIR, API_URL, OUTPUT_FILE)
