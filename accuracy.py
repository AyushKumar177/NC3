import json
from difflib import SequenceMatcher
from main import info, get_chain

def load_test_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def similarity_ratio(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

def compute_accuracy(test_data, chain):
    correct_count = 0
    total_count = len(test_data)
    
    for item in test_data:
        question = item['question']
        expected_answer = item['expected_answer']
        
        try:
            generated_answer = info(question) 
            if generated_answer:
                ratio = similarity_ratio(expected_answer, generated_answer)
                if ratio >= 0.8:
                    correct_count += 1
        except Exception as e:
            print(f"Error processing question '{question}': {e}")

    accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0
    return accuracy

if __name__ == "__main__":
    test_file_path = 'data/check.json'
    test_data = load_test_data(test_file_path)
    file_location = 'vectorDB'
    chain = get_chain(file_location)
    
    accuracy = compute_accuracy(test_data, chain)
    print(f"Accuracy: {accuracy:.2f}%")
