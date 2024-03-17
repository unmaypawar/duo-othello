# duo-othello

## Description

<p>This project brings the classic game of Othello to life in a digital format. Developed using Python and leveraging the power of Tkinter for the user interface, Duo-Othello offers players a gaming experience where they can challenge themselves against a formidable AI opponent.</p>

<p>The Minimax algorithm forms the backbone of the AI agent, enabling it to explore the game tree efficiently by considering all possible moves and their subsequent outcomes. By strategically implementing Alpha-Beta Pruning, the agent significantly reduces the search space, focusing on the most promising branches while disregarding less favorable ones. This optimization allows the agent to make informed decisions within reasonable time constraints, crucial for real-time gameplay scenarios.</p>

<p>Agent's decision relies on comprehensive evaluation function tailored specifically for Duo Othello, encompassing various crucial factors to accurately assess board states and guide the AI agent's decision-making process. This function serves as the cornerstone of the agent's strategic analysis, considering disc stability, player mobility, frontier discs, number of discs, corner occupancy, and more.</p>

<p>Finally the project has a simple user interface made using Tkinter, allowing players to engage directly with the AI agent in Duo Othello matches.</p>

## Visuals

### User Interface

![alt text](https://github.com/unmaypawar/duo-othello/blob/main/ui.jpg?raw=true)

## Installation Instructions

```
conda create --name duo-othello --file requirements.txt
```

## Usage Instructions

```
python3 main.py
```

## Contribution Guidelines

Fork the repository to your GitHub account and please create a new branch for each feature or bug fix.

## Support Information

Please raise an issue or a pull request.