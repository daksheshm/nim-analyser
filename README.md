

# Nim Analyser

A command-line tool to analyse a variant of the game of Nim using the **Sprague-Grundy theorem**. Given a set of piles, this tool determines whether the current position is a winning or losing one, and if it's a winning position, it suggests a winning move.

## The Game Rules

This analyser solves a specific impartial game with the following rules:
1.  The game starts with one or more piles of stones.
2.  A move consists of choosing one pile and splitting it into two smaller, non-empty piles.
3.  The game ends when a player cannot make a move (i.e., all piles have a size of 1 or 2, which cannot be split further).
4.  The player who cannot make a move loses (Normal Play convention).

## Core Concept: The Sprague-Grundy Theorem

This program's logic is entirely based on the Sprague-Grundy theorem, a fundamental result in combinatorial game theory. The theorem states that every impartial game is equivalent to a Nim pile of a certain size. This equivalent "size" is called the **Grundy number** (or **g-number**, or **nim-value**).

### Key Concepts

#### 1. Grundy Number (g-number)
The g-number of a game position is calculated using the **mex** function (Minimum Excluded value). The mex of a set of non-negative integers is the smallest non-negative integer not present in the set.
-   `mex({0, 1, 3, 4}) = 2`
-   `mex({}) = 0`

The g-number of a game position `P` is defined recursively:
`g(P) = mex({ g(P') | P' is a position reachable from P in one move })`

A terminal position (a position from which no moves can be made) has a g-number of 0.

#### 2. Nim-Sum (XOR Sum)
For a game composed of several independent sub-games (like Nim with multiple piles), the g-number of the entire game state is the bitwise XOR sum of the g-numbers of its sub-games. This is called the **Nim-Sum**.
`Nim-Sum = g(pile_1) ^ g(pile_2) ^ ... ^ g(pile_n)`

#### 3. Winning and Losing Positions
The Nim-Sum tells us everything about the game state:
-   **Losing Position (P-position):** If the Nim-Sum is **0**. The *previous* player to move is in a winning position. Any move from this state will lead to a state with a non-zero Nim-Sum.
-   **Winning Position (N-position):** If the Nim-Sum is **non-zero**. The *next* player to move can make a move to a state with a Nim-Sum of 0, thus forcing a win.

### How This Script Applies the Theorem

This script applies the theorem by breaking the problem down:

1.  **`grundy(n)` function**: This function calculates the g-number for a *single pile* of size `n`.
    -   It considers every possible move from a pile of size `n`: splitting it into two piles of size `i` and `n-i`.
    -   The new state is a game composed of these two smaller piles. Its g-number is `grundy(i) ^ grundy(n-i)`.
    -   The function collects the g-numbers of all possible next states.
    -   Finally, it calculates the `mex` of this set to find `grundy(n)`.
    -   It uses memoization (a dictionary) to store previously computed g-numbers, which drastically speeds up computation.

2.  **`main()` function**: This function analyzes the overall game state.
    -   It takes the initial piles as input (e.g., 10, 12, 15).
    -   It calculates the g-number for each individual pile using the `grundy()` function.
    -   It computes the **Nim-Sum** of the entire game by XORing the g-numbers of all the piles.

3.  **Determining the Outcome**:
    -   If the Nim-Sum is 0, it declares the state a **Losing Position**.
    -   If the Nim-Sum is non-zero, it declares it a **Winning Position**.

4.  **Finding a Winning Move**:
    -   If the position is winning, the goal is to make a move that results in a new game state with a Nim-Sum of 0.
    -   The script iterates through each pile `p_i` with its g-number `g_i`.
    -   For each pile, it calculates a *target g-number*: `target_g = g_i ^ Nim-Sum`.
    -   It then searches for a split of pile `p_i` into `j` and `p_i-j` such that `grundy(j) ^ grundy(p_i-j)` equals this `target_g`.
    -   The first such move it finds is a guaranteed winning move, which it prints for the user.

## Installation

No special installation is required. The script uses only standard Python libraries. Simply clone the repository or download the `nim_analyser.py` file.

```bash
git clone https://github.com/daksheshm/nim-analyser.git
cd nim-analyser
```

## Usage

Run the script from your terminal, providing the sizes of the piles as command-line arguments.

```bash
python nim_analyser.py <pile1_size> <pile2_size> ...
```

### Examples

#### Example 1: A Winning Position

Let's analyze a game with two piles of size 7 and 8.

```bash
$ python nim_analyser.py 7 8

Initial Piles: [7, 8]
g-values: [g(7)=2, g(8)=1]
Nim-Sum (2 ^ 1): 3

This is a Winning Position.
Searching for a winning move...
A winning move is to split pile 7 into piles of size 3 and 4.
New state: [8, 3, 4]
```
The script correctly identifies this as a winning position and suggests a move that will leave the opponent in a state with a Nim-Sum of 0.

#### Example 2: A Losing Position

A single pile of size 5 is a losing position.

```bash
$ python nim_analyser.py 5

Initial Piles: [5]
g-values: [g(5)=0]
Nim-Sum (0): 0

This is a Losing Position.
```
Any move you make from this position will result in a winning position for your opponent.

## Code Breakdown

-   **`mex(s)`**: A helper function that takes a set of integers `s` and returns the Minimum Excluded non-negative integer.
-   **`grundy(n)`**: The core recursive function that calculates the g-number for a single pile of size `n`. It is memoized for efficiency.
-   **`main()`**: The entry point of the script. It handles command-line arguments, orchestrates the analysis, and prints the results.
