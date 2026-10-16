# Research Gap Matrix v0.1

| Research axis | Prior work already does this? | What is still scientifically interesting for us? | Status |
|---|---|---|---|
| Apply ensemble to NIDS | Yes, extensively | Not a contribution by itself | CLOSED as novelty |
| Feature selection + ensemble | Yes | Compare performance–cost and stability under fair pipeline | POSSIBLE |
| Voting/stacking | Yes | Explain ensemble gain through complementary error patterns rather than “top models only” | POSSIBLE, needs more search |
| Class imbalance handling | Yes | Test whether gains occur in minority recall/Macro-F1 without distorting traffic | POSSIBLE |
| CIC-IDS2017 high accuracy | Extremely common | Audit dataset quality and avoid blindly trusting random-split scores | STRONG motivation |
| Leakage / split validity | Increasingly recognized | Compare ordinary split vs defensible temporal/day/scenario-aware evaluation where dataset permits | STRONG candidate |
| Cross-dataset generalization | Yes, recent evidence shows severe degradation | Full cross-dataset study may be too broad; can use it as motivation or optional extension | OPTIONAL |
| Feature-selection stability | Emerging and active, including 2026 work | Useful secondary analysis, probably not sufficient as sole novelty | SECONDARY |
| Statistical comparison | Often inconsistent across papers | Repeated evaluation + CI/paired tests can make conclusions more defensible | STRONG methodology contribution |
| Computational cost | Sometimes reported | Treat feature count, train time, inference time, model size as first-class outcomes | PRACTICAL contribution |

## Current candidate contribution

A reproducible, leakage-aware experimental framework for evaluating whether a heterogeneous ensemble provides a statistically credible **performance–cost and minority-detection advantage** over individual learners, with feature selection and base-learner error diversity treated as experimental factors rather than fixed preprocessing choices.

This is a candidate contribution, not a “novel” claim yet.
