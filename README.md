# CISC 489: PA 1 - Simulation of Cooperative Agents in Tileworld

## Usage

To run the simulation:

```bash
python main.py
```

To benchmark:

```bash
python benchmark.py -r N
```

where N is the number of runs.

## Description

### Agent v0.1: Reactive, Partitioned, Jiggly

The first class created, `PlayerReactivePartJiggle`, employs a reactive architecture.

Coins are inserted into a priority min-queue which maintained order according to the distance and coin value. Popping a coin from the queue yields the "best", closest coin. A relative bearing is determines the agent's movement direction. If the direction is blocked, the agent jiggles (moves randomly in an unblocked direction) in the hopes of either finding an alternate path or discovering an alternative coin.

This hierarchy is partitioned into two sub-types, top and bottom, where the agent is responsible for its corresponding half of the map. This results in no need for inter-agent communication. Initial separation is achieved with the highest priority directive, which moves an agent into their half of the map.

This approach is primarily a proof-of-concept, but has the capability to perform well. Over forty runs, the combined score could reach 360 in the demo environment. However, it was not uncommon to see scores of less than 100. The high level of variance makes this approach undesirable.

### Agent v0.2: Hybrid, Partitioned, Pathfinding

The second class, `PlayerHybridPartPath`, was similar to the first, but implemented Dijkstra's algorithm for pathfinding. The result was horrible.

The reactive architecture did so little calculation that duplication of work was insignificant. Moreover, the pathfinding algorithm was so burdensome that the agents spend most of their time frozen, thinking about what to do.

Overhauling v0.2 meant implementing inter-agent communication, minimizing thinking, and maximizing moving.

### Agent v0.3: Hybrid, Partitioned, Pathfinding

Improvements to `PlayerHybridPartPath` were made in key areas.

Inter-agent communication was implemented via class-level variables. These variables track the following information:

- `HALF_HEIGHT`: the vertical midpoint of the map, used for responsibility partitioning
- `HALF_WIDTH`: the vertical midpoint of the map, used for responsibility partitioning
- `is_init_sep`: a boolean indicating whether the initial separation of the agents has been completed
- `p_top_pos`: the position of the top player
- `p_bot_pos`: the position of the bottom player
- `coin_dict`: a dictionary of mapping coin locations to values
- `wall_pos`: a list of wall locations

That they are class-level variables implies an ability to reduce the amount of work done by the agents. In this case, the agent responsible for the top half of the map is responsible for updating these variables, save `p_bot_pos`.

Each agent uses the class-level variables to construct a coin queue, a priority queue, that yields their target coin.

During initial separation, the agent responsible for the top half of the map is restricted to coins in the top right quarter of the map. Meanwhile, the agent responsible for the bottom half of the map is restricted to coins on the left half of the map and below its current location. To ensure that the agents do not collide, the top agent stops moving if it gets too close to the bottom agent.

After initial separation, the agents are move within their half of the map.

By passing the coin distance and location to the pathfinding algorithm, Dijkstra's algorithm could be updated to a-star. Multiple checks are used to minimize the amount of time an agent spends thinking.

Once a path is found, the agent follows the path so long as the target coin still exists. If the target coin is no longer on the map, the whole process of identifying a target coin and finding a path is repeated.

This approach yielded the best results in the demo environment. Over forty runs, the combined score reached a mean of 368.8 and a median of 388.0, with a standard deviation of 3.29.

### Agent v0.3+: Failures and the Loss of Utility

It should be noted that the demo environment seems to contain more coins than the agent's are capable of picking up. For this reason, limited time was spent implementing a non-partitioned approach. The level of complexity increased significantly and a considerable amount of movement time was lost to thinking.

Most alternative approaches, within a partitioned map paradigm, employed modifications to the coin queue. None of these alternatives yielded better results. As the priority favors increasingly distant coins, thinking time increased significantly. Moreover, movement time was largely spent on the journey to the target coin and not on increasing the agent's score. Several times, I observed coins disappearing while the agent was en-route. However, it's possible I wasn't able to come up with the correct balance of considerations.

## Conclusion

It was surprising how much the approach needs to be tuned to the environment. I spent time trying to implement a generic approach, but optimizations are largely dependent on the environment. For instance, changes in the agent's movement speed alter the values of movement and thinking times. If an agent was capable of moving significantly faster, more time could be spent on deliberation. Likewise, if an agent was so "smart" that any complex thought was trivial, more intricate planning could be implemented.

Further, if the coins followed a different distribution, the agent's type of cooperation would need to change. In the demo environment, coins seem to appear in, roughly, a uniform distribution. However, if it were Gaussian, there would be greater benefit to the agent's both operating in the middle of the map and employing a higher degree of coordination.

## Note

Aliases for PlayerA and PlayerB classes were implemented for compatibility.

```python
PlayerA = PlayerHybridPartPath(true)
PlayerB = PlayerHybridPartPath(false)
```
