# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
      """
            A reflex agent chooses an action at each choice point by examining
            its alternatives via a state evaluation function.
            The code below is provided as a guide.  You are welcome to change
            it in any way you see fit, so long as you don't touch our method
            headers.
      """


      def getAction(self, gameState):
            """
            You do not need to change this method, but you're welcome to.
            getAction chooses among the best options according to the evaluation function.
            Just like in the previous project, getAction takes a GameState and returns
            some Directions.X for some X in the set {North, South, West, East, Stop}
            """
            # Collect legal moves and successor states
            legalMoves = gameState.getLegalActions()

            # Choose one of the best actions
            scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
            bestScore = max(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            chosenIndex = random.choice(bestIndices) # Pick randomly among the best

            "Add more of your code here if you want to"

            return legalMoves[chosenIndex]

      def evaluationFunction(self, currentGameState, action):
            """
            Design a better evaluation function here.
            The evaluation function takes in the current and proposed successor
            GameStates (pacman.py) and returns a number, where higher numbers are better.
            The code below extracts some useful information from the state, like the
            remaining food (newFood) and Pacman position after moving (newPos).
            newScaredTimes holds the number of moves that each ghost will remain
            scared because of Pacman having eaten a power pellet.
            Print out these variables to see what you're getting, then combine them
            to create a masterful evaluation function.
            """
            # Useful information you can extract from a GameState (pacman.py)
            successorGameState = currentGameState.generatePacmanSuccessor(action)
            newPos = successorGameState.getPacmanPosition()
            newFood = successorGameState.getFood()
            newGhostStates = successorGameState.getGhostStates()
            newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

            "*** YOUR CODE HERE ***"

            # print "successorGameState: ", successorGameState
            # print "newPos: ", newPos
            # print "newFood:\n", newFood    #newFood : grid
            # print "newGhostPosition:", newGhostStates[0]
            # print "newScaredTimes:", newScaredTimes[0]
            
            evaluation = 0
            ghost = []
            food = []
            distance = 0
            position = (0,0)
            longest = newFood.height + newFood.width

            if newPos in currentGameState.getCapsules():
                  return 10000
            if currentGameState.getFood()[newPos[0]][newPos[1]]:
                  # print "enter"
                  return 10000
            for ghostState in newGhostStates:
                  position = ghostState.getPosition()
                  distance = manhattanDistance(newPos,position)
                  # print newScaredTimes[0]
                  if newScaredTimes[0] > distance:
                        # print "enter"
                        ghost.append(-distance)
                  else:
                        ghost.append(distance)
            
            for x in range(newFood.width):
                  for y in range(newFood.height):
                        if newFood[x][y] == True:
                              food.append(manhattanDistance(newPos,(x,y)))

            if len(food) == 0:
                  food.append(max(ghost)+1)
                  
            if min(ghost) < 0:
                  evaluation = 10000+1.0/(-min(ghost)+1)
            else:
                  nearghost = min(ghost)
                  nearfood = min(food)
                  evaluation = 1.0/(nearfood+1)
                  if nearghost < 15:
                        # print ghost
                        evaluation = -100.0/(nearghost+1) + 1/(nearfood+1)
                        # print evaluation

            # print evaluation
            return evaluation

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.
      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
      """
            This class provides some common elements to all of your
            multi-agent searchers.  Any methods defined here will be available
            to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
            You *do not* need to make any changes here, but you can if you want to
            add functionality to all your adversarial search agents.  Please do not
            remove anything, however.
            Note: this is an abstract class: one that should not be instantiated.  It's
            only partially specified, and designed to be extended.  Agent (game.py)
            is another abstract class.
      """

      def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
            self.index = 0 # Pacman is always agent index 0
            self.evaluationFunction = util.lookup(evalFn, globals())
            self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
      """
            Your minimax agent (question 2)
      """

      def getAction(self, gameState):
            """
            Returns the minimax action from the current gameState using self.depth
            and self.evaluationFunction.
            Here are some method calls that might be useful when implementing minimax.
            gameState.getLegalActions(agentIndex):
                  Returns a list of legal actions for an agent
                  agentIndex=0 means Pacman, ghosts are >= 1
            gameState.generateSuccessor(agentIndex, action):
                  Returns the successor game state after an agent takes an action
            gameState.getNumAgents():
                  Returns the total number of agents in the game
            """
            "*** YOUR CODE HERE ***"
            finalState = self.minimax(gameState,0,0)

            # print "complete minimax-------------------------------------", finalState
            return finalState[1]

      def minimax(self,gameState,depth,agentIndex):
            # print "the", depth, "ply"
            totalAgent = gameState.getNumAgents()
            if depth == self.depth:
                  # print "call evaluationFunction: ", (self.evaluationFunction(gameState),'Stop')
                  return (self.evaluationFunction(gameState),'Stop')
            else:
                  if agentIndex == 0:
                        # print "now pacman"
                        legalMoves = gameState.getLegalActions(agentIndex)
                        # print "legalmoves:", legalMoves
                        if len(legalMoves)==0:
                              # print "call evaluationFunction: ", (self.evaluationFunction(gameState),'Stop')
                              return (self.evaluationFunction(gameState),'Stop')
                        return max((self.minimax(gameState.generateSuccessor(agentIndex, action),depth,(agentIndex+1)%totalAgent)[0],action) for action in legalMoves)
                  elif agentIndex != totalAgent-1:
                        # print "now the ghost", agentIndex
                        legalMoves = gameState.getLegalActions(agentIndex)
                        # print "legalmoves:", legalMoves
                        if len(legalMoves)==0:
                              # print "call evaluationFunction: ", (self.evaluationFunction(gameState),'Stop')
                              return (self.evaluationFunction(gameState),'Stop')
                        return min((self.minimax(gameState.generateSuccessor(agentIndex, action),depth,(agentIndex+1)%totalAgent)[0],action) for action in legalMoves)
                  else:
                        # print "now the last ghost"
                        legalMoves = gameState.getLegalActions(agentIndex)
                        # print "legalmoves:", legalMoves
                        if len(legalMoves)==0:
                              # print "call evaluationFunction: ", (self.evaluationFunction(gameState),'Stop')
                              return (self.evaluationFunction(gameState),'Stop')
                        return min((self.minimax(gameState.generateSuccessor(agentIndex, action),depth+1,(agentIndex+1)%totalAgent)[0],action) for action in legalMoves)
         
          

class AlphaBetaAgent(MultiAgentSearchAgent):
      """
            Your minimax agent with alpha-beta pruning (question 3)
      """

      def getAction(self, gameState):
            """
            Returns the minimax action using self.depth and self.evaluationFunction
            """
            "*** YOUR CODE HERE ***"
            finalState = self.alphabeta(gameState,0,0,-9999999999,9999999999)

            # print "complete alphabeta-------------------------------------", finalState
            return finalState[1]
      def alphabeta(self,gameState,depth,agentIndex,a,b):
            # print "the", depth, "ply"
            totalAgent = gameState.getNumAgents()
            if depth == self.depth:
                  # print "call evaluationFunction: ", (self.evaluationFunction(gameState),'Stop')
                  return (self.evaluationFunction(gameState),'Stop')
            else:
                  if agentIndex == 0:
                        # print "now pacman"
                        legalMoves = gameState.getLegalActions(agentIndex)
                        # print "legalmoves:", legalMoves
                        if len(legalMoves)==0:
                              # print "call evaluationFunction: ", (self.evaluationFunction(gameState),'Stop')
                              return (self.evaluationFunction(gameState),'Stop')
                        v = (-9999999999,'Stop')
                        for action in legalMoves:
                              v = max(v,(self.alphabeta(gameState.generateSuccessor(agentIndex, action),depth,(agentIndex+1)%totalAgent,a,b)[0],action))
                              if v[0] >= b:
                                    return v
                              a = max(a,v[0])
                        return v
                  elif agentIndex != totalAgent-1:
                        # print "now the ghost", agentIndex
                        legalMoves = gameState.getLegalActions(agentIndex)
                        # print "legalmoves:", legalMoves
                        if len(legalMoves)==0:
                              # print "call evaluationFunction: ", (self.evaluationFunction(gameState),'Stop')
                              return (self.evaluationFunction(gameState),'Stop')
                        v = (9999999999,'Stop')
                        for action in legalMoves:
                              v = min(v,(self.alphabeta(gameState.generateSuccessor(agentIndex, action),depth,(agentIndex+1)%totalAgent,a,b)[0],action))
                              if a >= v[0]:
                                    return v
                              b = min(b,v[0])
                        return v
                  else:
                        # print "now the last ghost"
                        legalMoves = gameState.getLegalActions(agentIndex)
                        # print "legalmoves:", legalMoves
                        if len(legalMoves)==0:
                              # print "call evaluationFunction: ", (self.evaluationFunction(gameState),'Stop')
                              return (self.evaluationFunction(gameState),'Stop')
                        v = (9999999999,'Stop')
                        for action in legalMoves:
                              v = min(v,(self.alphabeta(gameState.generateSuccessor(agentIndex, action),depth+1,(agentIndex+1)%totalAgent,a,b)[0],action))
                              if a >= v[0]:
                                    return v
                              b = min(b,v[0])
                        return v
            

class ExpectimaxAgent(MultiAgentSearchAgent):
      """
            Your expectimax agent (question 4)
      """

      def getAction(self, gameState):
            """
            Returns the expectimax action using self.depth and self.evaluationFunction
            All ghosts should be modeled as choosing uniformly at random from their
            legal moves.
            """
            "*** YOUR CODE HERE ***"
            finalState = self.expectimax(gameState,0,0)

            # print "complete expectimax-------------------------------------", finalState
            return finalState[1]
      def expectimax(self,gameState,depth,agentIndex):
            # print "the", depth, "ply"
            totalAgent = gameState.getNumAgents()
            if depth == self.depth:
                  # print "call evaluationFunction: ", (self.evaluationFunction(gameState),'Stop')
                  return (self.evaluationFunction(gameState),'Stop')
            else:
                  if agentIndex == 0:
                        # print "now pacman"
                        legalMoves = gameState.getLegalActions(agentIndex)
                        # legalMoves.reverse()
                        # print "legalmoves:", legalMoves
                        if len(legalMoves)==0:
                              # print "call evaluationFunction: ", (self.evaluationFunction(gameState),'Stop')
                              return (self.evaluationFunction(gameState),'Stop')
                        templist = [(self.expectimax(gameState.generateSuccessor(agentIndex, action),depth,(agentIndex+1)%totalAgent)[0],action) for action in legalMoves]
                        # print templist
                        v = -99999999
                        index = 0
                        for i in range(len(templist)):
                              if templist[i][0] > v:
                                    v = templist[i][0]
                                    index = i
                              if templist[i][0] == v and templist[index][1] == 'Stop':
                                    v = templist[i][0]
                                    index = i
                        temp = templist[index]
                        # print temp
                        return temp
                  elif agentIndex != totalAgent-1:
                        # print "now the ghost", agentIndex
                        legalMoves = gameState.getLegalActions(agentIndex)
                        # print "legalmoves:", legalMoves
                        if len(legalMoves)==0:
                              # print "call evaluationFunction: ", (self.evaluationFunction(gameState),'Stop')
                              return (self.evaluationFunction(gameState),'Stop')
                        children = [(self.expectimax(gameState.generateSuccessor(agentIndex, action),depth,(agentIndex+1)%totalAgent)[0],action) for action in legalMoves]
                        totalevaluation = 0
                        for child in children:
                              totalevaluation += child[0]
                        expectation = totalevaluation/len(children)
                        index = self.findnearest(expectation,children)
                        return (expectation,children[index][1])
                  else:
                        # print "now the last ghost"
                        legalMoves = gameState.getLegalActions(agentIndex)
                        # print "legalmoves:", legalMoves
                        if len(legalMoves)==0:
                              # print "call evaluationFunction: ", (self.evaluationFunction(gameState),'Stop')
                              return (self.evaluationFunction(gameState),'Stop')
                        children = [(self.expectimax(gameState.generateSuccessor(agentIndex, action),depth+1,(agentIndex+1)%totalAgent)[0],action) for action in legalMoves]
                        totalevaluation = 0
                        for child in children:
                              totalevaluation += child[0]
                        expectation = totalevaluation/len(children)
                        index = self.findnearest(expectation,children)
                        # print "children[index]: ", children[index]
                        return (expectation,children[index][1])
      def findnearest(self,element,list):
            temp = []
            for i in range(len(list)):
                  temp.append(abs(list[i][0]-element)) 
            return temp.index(min(temp))                      
                                  
def betterEvaluationFunction(currentGameState):
      """
            Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
            evaluation function (question 5).
            DESCRIPTION: <write something here so we know what you did>
            if ghoast is close enough to the pacman(manhatten distance < 2), evaluation = score()+evaluation += -100.0/(nearghost+1)
            else,  evaluation = -1.0/(nearghost+1.0) + 50.0/(nearscaredghost+1) +50.0/(nearcapsule+1.0) + 10.0/(nearfood+1.0)+score

            near means the nearest object's manhatten distance to pacman
      """
      "*** YOUR CODE HERE ***"


      # successorGameState = currentGameState.generatePacmanSuccessor(currentGameState.getLegalActions(0)[0])
      # newPos = successorGameState.getPacmanPosition()
      # newFood = successorGameState.getFood()
      # newGhostStates = successorGameState.getGhostStates()
      # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

      # print "successorGameState: ", successorGameState
      # print "newPos: ", newPos
      # print "newFood:\n", newFood    #newFood : grid
      # print "newGhostPosition:", newGhostStates[0]
      # print "newScaredTimes:", newScaredTimes[0]
            
      Pos = currentGameState.getPacmanPosition()
      Food = currentGameState.getFood()
      GhostStates = currentGameState.getGhostStates()
      ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
      Capsules = currentGameState.getCapsules()

      
      evaluation = 0.0
      food = []
      ghost = []
      scaredghost = []
      capsule = []

      longest = Food.height + Food.width
      nearfood = 0
      nearghost = 0
      nearscaredghost = 0
      nearcapsule = 0

          
      distance = 0
      position = (0,0)

      for ghostState in GhostStates:
            position = ghostState.getPosition()
            distance = manhattanDistance(Pos,position)
            # print newScaredTimes[0]
            if ScaredTimes[0] > 0:
                  # print "enter"
                  scaredghost.append(distance)
            else:
                  ghost.append(distance)
      
      for x in range(Food.width):
            for y in range(Food.height):
                  if Food[x][y] == True:
                        food.append(manhattanDistance(Pos,(x,y)))
      for cap in Capsules:
            capsule.append(manhattanDistance(Pos,cap))
      

      scaredghost.append(9999999999999)
      ghost.append(99999999999)
      capsule.append(99999999999)


      if len(food) == 0:
            food.append(0)
      # print ghost
      if len(scaredghost) > 0:
            nearscaredghost = min(scaredghost)
            # print scaredghost
      if len(ghost) > 0:
            nearghost = min(ghost)
      if len(Capsules) > 0:
            nearcapsule = min(capsule)

      # if Pos in Capsules:
      #       print "bingo"
      #       return 100000


      nearfood = min(food)

      if len(ghost) > 0 and nearghost < 2:
            # print "avoid ghost:", nearghost
            evaluation += -100.0/(nearghost+1)
            # print evaluation

      else:
            # print "nearghost:", nearghost, "nearscaredghost:", nearscaredghost
            # print "nearcapsule:", nearcapsule, "nearfood:", nearfood
            evaluation = -1.0/(nearghost+1.0) + 50.0/(nearscaredghost+1) +50.0/(nearcapsule+1.0) + 10.0/(nearfood+1.0)

      # print "evaluation: ", evaluation
      return currentGameState.getScore() + evaluation

# Abbreviation
better = betterEvaluationFunction