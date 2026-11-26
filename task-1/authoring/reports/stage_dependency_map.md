# Dependency map

```mermaid
flowchart TD
  S1[1 Exact normal rank] --> S2[2 Smith factors]
  S2 --> S3[3 Primary powers]
  S1 --> S4[4 Infinity filtration]
  S1 --> S5[5 Right filtration]
  S1 --> S6[6 Left filtration]
  S3 --> S7[7 Constant Kronecker frames]
  S4 --> S7
  S5 --> S7
  S6 --> S7
  S7 --> S8[8 Saturated bases and duals]
  S7 --> S9[9 Reflexive resolvent]
  S2 --> S9
  S8 --> S10[10 Projector factorization]
  S9 --> S10
  S8 --> S11[11 Forcing compatibility]
  S11 --> S12[12 Particular minimum denominator]
  S9 --> S12
  S10 --> S12
  S12 --> S13[13 Prime-power lower bounds]
  S3 --> S13
  S9 --> S13
```

The longest displayed scientific dependency path contains eight nodes. Some oracle computations can run in parallel or bypass a displayed constructive route; the contract requires valid connected certificates rather than a specific execution sequence. Constant frames validate the full classification independently, while projectors connect the chosen (possibly different) bases to the chosen inverse. The lower-bound rows may also be independently constructed rather than extracted from that inverse.
