# CS321H Activity 1

1. Construct a **DFA** that accepts all strings on {0,1} with length four or greater in which the leftmost three symbols are all the same, but different from the rightmost symbol.

> JFLAP File: [ex-1.jff](ex-1.jff)

2. Convert the following NFA to a DFA

NFA JFLAP File: [ex-2-1.jff](ex-2-1.jff)

> NOTE: I used the convert function in JFLAP to convert this to DFA.

> DFA JFLAP File: [ex-2-2.jff](ex-2-2.jff)

3. Let L be a regular language on some alphabet X, and let X1 ⊂ X be a smaller alphabet. Let L1 be the subset of L whose elements are made up only of symbols from X1. Show that L1 is also a regular language

> Defnine some NFA, say NFA_L for language L. Also define alphabet X0 such that X0 = X \ X1. If an edge in NFA_L ∈ X0, remove that edge. This will create a new NFA, NFA_L1, which will accept L1. Because NFA_L1 accepts L1, L1 is a regular language.

4. Prove that regular languages are closed under union. That is, if L1 and L2 are regular languages, then L1 ∪ L2 is a regular language. 

> Define A1 and A2 as NFAs/DFAs that accept languages L1 and L2 respectively. Now define a new NFA that branches to each acceptor A1 and A2 from the initial state. This acceptor will accept the language L1 ∪ L2.