### llama-3.1-8b pass@1
---
eval file: positive_search_with_previous_code_2025_11_15_12_18_54.json

passed: {'definition': 4, 'lemma': 3, 'theorem': 1}, categories: {'definition': 83, 'lemma': 7, 'theorem': 29}


eval file: positive_search_without_previous_code_2025_11_15_02_01_07.json
passed: {'definition': 10, 'lemma': 3, 'theorem': 1}, categories: {'definition': 94, 'lemma': 24, 'theorem': 44, 'corollary': 1, 'claim': 1}


### llama-3.1-8b pass@5
eval file: positive_search_with_previous_code_2025_11_15_12_18_54.json
passed: {'definition': 13, 'lemma': 5, 'theorem': 2}, categories: {'definition': 83, 'lemma': 7, 'theorem': 29}


eval file: positive_search_without_previous_code_2025_11_15_02_01_07.json
passed: {'definition': 43, 'theorem': 8, 'lemma': 6}, categories: {'definition': 94, 'lemma': 24, 'theorem': 44, 'corollary': 1, 'claim': 1}


### Gpt-oss-20b pass@1
eval file: positive_search_with_previous_code_2025_11_15_12_18_54.json
passed: {'definition': 29, 'lemma': 2, 'theorem': 8}, categories: {'definition': 83, 'lemma': 7, 'theorem': 29}

eval file: positive_search_without_previous_code_2025_11_15_02_01_07.json
passed: {'definition': 32, 'theorem': 14, 'lemma': 7}, categories: {'definition': 94, 'lemma': 24, 'theorem': 44, 'corollary': 1, 'claim': 1}

### Gpt-oss-20b pass@5
log file: 2025_11_17_17_11_46.log
eval file: positive_search_with_previous_code_2025_11_15_12_18_54.json
passed: {'definition': 64, 'lemma': 7, 'theorem': 10}, categories: {'definition': 83, 'lemma': 7, 'theorem': 29}

eval file: positive_search_without_previous_code_2025_11_15_02_01_07.json
passed: {'definition': 68, 'lemma': 17, 'theorem': 34, 'corollary': 1}, categories: {'definition': 94, 'lemma': 24, 'theorem': 44, 'corollary': 1, 'claim': 1}

### GPT-5.1-nano pass@1
eval file: positive_search_with_previous_code_2025_11_15_12_18_54.json
passed: {'definition': 20, 'lemma': 5, 'theorem': 1}, categories: {'definition': 83, 'lemma': 7, 'theorem': 29}

eval file: positive_search_without_previous_code_2025_11_15_02_01_07.json
passed: {'definition': 26, 'lemma': 9, 'theorem': 8, 'corollary': 1}, categories: {'definition': 94, 'lemma': 24, 'theorem': 44, 'corollary': 1, 'claim': 1}

### GPT-5.1-nano pass@5
log file: 2025_11_17_17_41_13.log
eval file: positive_search_with_previous_code_2025_11_15_12_18_54.json
passed: {'definition': 36, 'lemma': 6, 'theorem': 4}, categories: {'definition': 83, 'lemma': 7, 'theorem': 29}

eval file: positive_search_without_previous_code_2025_11_15_02_01_07.json
passed: {'definition': 62, 'lemma': 18, 'theorem': 35, 'corollary': 1, 'claim': 1}, categories: {'definition': 94, 'lemma': 24, 'theorem': 44, 'corollary': 1, 'claim': 1}

### Gemini-2.5-flash-lite pass@1
log file: 2025_11_17_17_50_56.log
eval file: positive_search_with_previous_code_2025_11_15_12_18_54.json
passed: {'lemma': 5, 'definition': 9}, categories: {'definition': 83, 'lemma': 7, 'theorem': 29}

eval file: positive_search_without_previous_code_2025_11_15_02_01_07.json
passed: {'definition': 8, 'lemma': 1}, categories: {'definition': 94, 'lemma': 24, 'theorem': 44, 'corollary': 1, 'claim': 1}

### Gemini-2.5-flash-lite pass@5
log file: 2025_11_17_17_54_28.log
eval file: positive_search_with_previous_code_2025_11_15_12_18_54.json

passed: {'lemma': 6, 'definition': 20}, categories: {'definition': 83, 'lemma': 7, 'theorem': 29}

eval file: positive_search_without_previous_code_2025_11_15_02_01_07.json
passed: {'definition': 23, 'lemma': 4, 'theorem': 3}, categories: {'definition': 94, 'lemma': 24, 'theorem': 44, 'corollary': 1, 'claim': 1}

## This is the base model on which I am going to run fine tuning:
### deepseek-coder-v2-16b pass@1
eval file: positive_search_with_previous_code_2025_11_15_12_18_54.json
passed: {'definition': 16, 'lemma': 4, 'theorem': 1}, categories: {'definition': 83, 'lemma': 7, 'theorem': 29}

eval file: positive_search_without_previous_code_2025_11_15_02_01_07.json
{'definition': 31, 'theorem': 8, 'lemma': 3, 'corollary': 1}, categories: {'definition': 94, 'lemma': 24, 'theorem': 44, 'corollary': 1, 'claim': 1}

### deepseek-coder-v2-16b pass@5
eval file: positive_search_with_previous_code_2025_11_15_12_18_54.json
passed {'definition': 33, 'lemma': 4, 'theorem': 4}, categories: {'definition': 83, 'lemma': 7, 'theorem': 29}

eval file: positive_search_without_previous_code_2025_11_15_02_01_07.json
passed: {'definition': 63, 'theorem': 20, 'lemma': 9, 'corollary': 1, 'claim': 1}, categories: {'definition': 94, 'lemma': 24, 'theorem': 44, 'corollary': 1, 'claim': 1}


### Trained llama pass@1
2025_11_17_20_00_32.log

### baseline gpt-5.1-nano test pass@1
2025_11_17_20_47_46.log
passed {'theorem': 7, 'lemma': 3, 'definition': 5, 'claim': 1}, total {'definition': 20, 'theorem': 21, 'lemma': 8, 'corollary': 1, 'claim': 1}

### baseline gpt-5.1-nano train pass@1
2025_11_17_20_49_07.log
passed {'definition': 14, 'theorem': 8, 'lemma': 6, 'claim': 3, 'corollary': 1}, total {'definition': 72, 'claim': 16, 'lemma': 18, 'theorem': 38, 'formula': 1, 'corollary': 2}

### baseline gemini-2.5-flash-lite test pass@1
2025_11_17_20_49_42.log
passed {'definition': 1}, total {'definition': 20, 'theorem': 21, 'lemma': 8, 'corollary': 1, 'claim': 1}

### baseline gemini-2.5-flash-lite train pass@1
2025_11_17_20_52_01.log
passed {'definition': 5}, total {'definition': 72, 'claim': 16, 'lemma': 18, 'theorem': 38, 'formula': 1, 'corollary': 2}

