## Setup
For setting up mutmut, we needed to edit the setup.cfg file. [insert more info here]

## Mutation Tests
Initially, we had 376 mutations that survived. After our added tests, we had 373. 

## Analysis
- We fixed the issue inside of shorten path where mutating a list to "none" had no effect, by creating a test to ensure that the function could not return none, therefore killing the mutant.

## Group Contributions
- Jose: did setup and the [] test
- Ursula: helped with setup debugging and did the shorten path test
- Michael: did the [] test
