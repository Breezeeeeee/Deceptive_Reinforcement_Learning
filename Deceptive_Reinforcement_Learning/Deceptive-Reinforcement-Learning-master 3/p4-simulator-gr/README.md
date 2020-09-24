irrational model
When we implemented our irrational model we had several concerns. 
The first one was that we found that  if we added the real goal when calculating delta r prime, the actions of the agent would be different from the one excluding real goal. With very limited experiments, we thought it would be better excluding the real goal when we did the calculation of formula shown below. Including the real goal would make the agent less deceptive.








The second one was that certainly with higher α, the agent would act more irrational, but if α is more than 0.5, sometimes the agent would never go to the goal and stuck in a deadlock. We do not know if this should be fixed by a single deadlock breaker or it was just normal due to irrationality overwhelms by a high α. Or it could caused by some bugs that we did not concerned about :(


Here are some figures that show different results with different alpha.

when alpha = 0:



















when alpha = 0.3:

















when alpha = 0.6(notice the white dot at lower right corner is where deadlock happened)

