from flask import Flask, request, render_template

app = Flask(__name__)


def main(board):
    word_set = get_boggle_words()
    words = find_words(board)
    valid_words = check_words(words, word_set)
    print(valid_words)
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


def get_boggle_words():
    words = set()
    with open("word-list.txt", "r") as file:
        for line in file:
            if "\n" in line:
                word = line.rstrip('\n')
            else:
                word = line
            words.add(word)
    return words

# Return words in english language - words that have numbers in them may not work as well
def check_words(word_list, word_set):
    valid = set()
    for word in word_list:
        word = word.lower()
        if word in word_set:
            word = word.capitalize()
            valid.add(word)
    return valid


def dfs(grid, i, j, visited, word, words):
    # Mark the current cell as visited
    visited[i][j] = True

    # Append the current character to the word
    word += grid[i][j]

    # Add the word to the list of words if it exists in the dictionary
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