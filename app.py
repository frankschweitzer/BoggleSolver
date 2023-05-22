from flask import Flask, request, render_template

app = Flask(__name__)


def main(board):
    print("Main called")
    words = find_words(board)
    print("Words found")
    english_words, word_map = get_english_words()
    print("Got english words")
    valid_words = check_words(words, word_map)
    print("Retrieved valid words")
    return valid_words
    

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
def get_english_words():
    map = {}
    word_list = []
    with open("OxfordDictionary.txt", "r") as file:
        for line in file:
            sentence = line.strip()
            words = sentence.split(" ")
            if len(words) > 1: 
                if "abbr." not in words: 
                    word = words[0].upper()
                    if word[-1].isdigit():
                        word = word[0:-1]
                    map.update({word:sentence})
                    word_list.append(word)
    return word_list, map

# Return words in english language - words that have numbers in them may not work as well
def check_words(word_list, english_words):
    valid = set()
    for word in word_list:
        if word in english_words:
            valid.add(word)
    return valid


# Function to perform DFS on the grid
def dfs(grid, i, j, visited, word, words):
    # Mark the current cell as visited
    visited[i][j] = True

    # Append the current character to the word
    word += grid[i][j]

    # Add the word to the list of words
    if len(word) > 2:
        words.append(word)

    # Define the possible moves in the grid
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    # Explore all possible neighboring cells
    for move in moves:
        new_i = i + move[0]
        new_j = j + move[1]

        # Check if the neighboring cell is within the grid boundaries and not visited
        if 0 <= new_i < len(grid) and 0 <= new_j < len(grid) and not visited[new_i][new_j]:
            dfs(grid, new_i, new_j, visited, word, words)

    # Mark the current cell as unvisited for future iterations
    visited[i][j] = False

# Function to find all possible words in the grid
def find_words(grid):
    words = []
    visited = [[False for _ in range(len(grid))] for _ in range(len(grid))]

    # Iterate over each cell in the grid and start the DFS
    for i in range(len(grid)):
        for j in range(len(grid)):
            dfs(grid, i, j, visited, '', words)

    return words


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)