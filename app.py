from flask import Flask, request, render_template

app = Flask(__name__)


def main(board):
    words = find_words(board)
    # word_map, eng_words = get_english_words()
    word_set = get_boggle_words()
    words = find_words(board, word_set)
    # valid_words = check_words(words, eng_words)
    # return valid_words
    return words
    

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    grid = [[request.form.get(f'row-{i}-col-{j}') for j in range(4)] for i in range(4)]
    # Process the grid or perform any required operations
    
    # Example: Print the grid
    for row in grid:
        print(row)
        
    valid_words = main(grid)
    # Return a response or redirect as needed
    return render_template('results.html', valid_words=valid_words)


# Obtain list of all english words
# def get_english_words():
#     map = {}
#     eng_words = set()
#     word_list = []
#     with open("OxfordDictionary.txt", "r") as file:
#         for line in file:
#             sentence = line.strip()
#             words = sentence.split(" ")
#             if len(words) > 1: 
#                 if "abbr." not in words: 
#                     word = words[0].upper()
#                     if word[-1].isdigit():
#                         word = word[0:-1]
#                     map.update({word:sentence})
#                     eng_words.add(word)
#                     word_list.append(word)
#     # took out map to be returned
#     return map, eng_words

def get_boggle_words():
    words = set()
    with open("words-list.txt", "r") as file:
        for line in file:
            words.add(line)
            print(line)
    return words

# Return words in english language - words that have numbers in them may not work as well
# def check_words(word_list, english_words):
#     valid = set()
#     for word in word_list:
#         if word in english_words:
#             valid.add(word)
#     return valid


def dfs(grid, i, j, visited, word, words, word_map):
    # Mark the current cell as visited
    visited[i][j] = True

    # Append the current character to the word
    word += grid[i][j]

    # Add the word to the list of words if it exists in the dictionary
    if len(word) > 2 and word in word_map:
        words.append(word)

    # Define the possible moves in the grid
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    # Explore all possible neighboring cells
    for move in moves:
        new_i = i + move[0]
        new_j = j + move[1]

        # Check if the neighboring cell is within the grid boundaries and not visited
        if 0 <= new_i < len(grid) and 0 <= new_j < len(grid) and not visited[new_i][new_j]:
            dfs(grid, new_i, new_j, visited, word, words, word_map)

    # Mark the current cell as unvisited for future iterations
    visited[i][j] = False


# Function to find all possible words in the grid
def find_words(grid, word_map):
    words = []
    visited = [[False for _ in range(len(grid))] for _ in range(len(grid))]

    # Iterate over each cell in the grid and start the DFS
    for i in range(len(grid)):
        for j in range(len(grid)):
            dfs(grid, i, j, visited, '', words, word_map)

    return words


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)