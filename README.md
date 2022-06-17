# chess-opening-analysis

> "Openings dont matter. It's irrelevant." - Grandmaster Benjamin Finegold [[source]](https://www.youtube.com/watch?v=WPIMRMl0guA)

In the chess community, great emphasis is put on the study of openings.
Players memorize the moves that are thought to be best for all possible situations in the first few turns.
This leads to a situation where new players find themselves in need of studying countless moves in endless lines, hoping to gain an advantage in the game by playing precalculated moves they learned by heart.

However, there are also people voicing contrary believes: openings don't matter and studying them is a waste of time.

In this work, we want to mathematically analyze if this is actually true: 
- What is mathematically proven to be the best or the worst opening?
- What is the worst that can happen if you play poorly into a well-prepared players opening preparation?
- Do openings matter at all or are we really just wasting our time learning them?

## Approach
We use a game theoretical approach in studying the openings, namely the [Extensive-form game](https://en.wikipedia.org/wiki/Extensive-form_game).
A game tree is build from the openings, and every state (= chess position) in the tree is evaluated by the chess computer stockfish.
After that, the annotated game tree allows judging player decisions.

We have a tree where the state of the game can move from the root to the leafs.
Each node represents a possible move (that is "from the books", so we have to stay within defined openings).
Moving the state through the layers is making a move, one at a time
(and only one player moves per layer, white at evenly numbered layers starting from 0).
As the state is moved, it follows one of the openings that are possible in this specific game-tree.
The leafs each have a payoff represented by the rating that the specific opening, that is being formed, has.
for their turn, players are presented with a choice to move down one of the possible sub-branches of their position in the tree.
Out of all child nodes they can choose the node that will have the best payoff in the end, keeping in mind their opponents ability to strategically counteract.
That means, it makes sense to aim for the opening that has not the highest end rating, but the opening that is the best no matter what the opponent does.

## (TLDR) Results


## Installation
- clone the repo
- install [stockfish](https://stockfishchess.org/download/#)
- copy the stockfish exe path into STOCKFISH_EXE_PATH in analysis.py 
- tweak the constants at the top of analysis.py to your liking, higher depth yields better results but takes longer
- > pip install -r requirements.txt

## Usage
Run analysis.py to start the analysis with default parameters.

The resulting game tree is saved into game_tree.pdf

## FAQ
- Q: How are the numbers of the ratings to be read? A: They are in [centipawn](https://chess.fandom.com/wiki/Centipawn). That means that in a position rated with 100, the position is as advantageous for the player as having a single additional pawn over their opponent would be like. Positive ratings indicate a advantage for white, while negative numbers are better for black.
- Q: Which chess computer is used to evaluate the positions? A: stockfish, we consider it state of the art and powerful enough to make the results believable
- Q: How are the openings analyzed using game Theory? A: using an Extensive-form game
- Q: What is this notation for the moves? A: The short [Algebraic notation](https://en.wikipedia.org/wiki/Algebraic_notation_(chess)) generally, but the position evaluator component also uses [Forsyth-Edwards-Notation (FEN)](https://de.wikipedia.org/wiki/Forsyth-Edwards-Notation) at some point.
- Q: How many openings are analyzed? A: around 700 individual lines, new ones can be easily added into the data file
- Q: Where do you get the openings from? A: The Encyclopedia of Chess Openings (ECO-Code) systematically lists the 500 most important openings, a lot of them with additional lines and variations

## Sources
- Source for the openings is the [german Wikipedia article for the ECO-Code](https://de.wikipedia.org/wiki/ECO-Schl%C3%BCssel), because it lists everything neatly in a easily parsable table.