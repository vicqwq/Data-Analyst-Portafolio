# What Drives EV Purchase Decisions?
## Which customer attributes actually predict willingness to buy an electric vehicle?

**Prepared:** September 2026
**Method:** Information Value (IV) / Weight of Evidence (WoE) via OptimalBinning
**Data source:** `data/Bronze layer/train.csv` — 668,665 records
**Scope:** Customer profiles for a consumer EV purchase prediction dataset

---

## Executive Summary

**6 out of 13 features carry a meaningful signal for EV purchase likelihood — but the top two dominate so completely that the others are secondary.** The remaining 7 features — including Age, Gender, and proximity to charging stations — show no statistical relationship with EV purchases at all.

The analysis identifies **6 features with detectable signal**, in order of importance:

1. **Environmental Concern Level** — the dominant predictor (IV = 2.26); a perfectly monotonic relationship where concern level 5 customers buy at 51.8% versus 0.6% for level 1
2. **Subsidy Available** — a decisive enabler (IV = 1.82); without subsidies the purchase rate collapses to 0.6%; with them it reaches 27.5%
3. **Annual Income** — strong structural driver (IV = 0.43); income above $127k drives a 35.7% purchase rate vs 4.3% for incomes below $51k
4. **Range Anxiety Level** — a meaningful barrier (IV = 0.15); customers with high or medium anxiety buy at 4.0% vs 18.9% for low-anxiety customers
5. **Home Charging Possible** — weak facilitator (IV = 0.05)
6. **Daily Commute km** — weak and non-monotonic (IV = 0.03)

**Age, Gender, car ownership, and proximity to charging stations** have no detectable impact on EV purchase likelihood in this dataset. The finding on charging stations is counterintuitive and worth revisiting in further analysis.

---

## Target Variable Definition

```
will_buy_ev = 1  if Will_Buy_EV == "Yes"
will_buy_ev = 0  otherwise
```

The binary target was derived directly from the `Will_Buy_EV` column in the training data by encoding "Yes" as 1 and "No" as 0.

> **Event rate: 17.5%** — 116,779 buyers out of 668,665 total records. This is comfortably within the 5–95% reliable range for IV analysis.

---

## Exclusions & Data Preparation

**Row identifier — excluded:**

| Column | Reason |
|---|---|
| `id` | Row index; carries no predictive information |

No columns were excluded for missing values (the dataset is complete). All 13 remaining features were analyzed.

---

## Top Drivers — IV Summary

| Rank | Feature | IV | Predictive Power |
|---|---|---|---|
| **1** | **`Environmental_Concern_Level`** | **2.26** | **Very Strong** |
| **2** | **`Subsidy_Available`** | **1.82** | **Very Strong** |
| **3** | **`Annual_Income_USD`** | **0.43** | **Strong** |
| **4** | **`Range_Anxiety_Level`** | **0.15** | **Medium** |
| 5 | `Home_Charging_Possible` | 0.05 | Weak |
| 6 | `Daily_Commute_km` | 0.03 | Weak |
| — | `City_Type` | 0.008 | Useless |
| — | `Charging_Stations_Near_Home` | 0.007 | Useless |
| — | `Age` | 0.006 | Useless |
| — | `Charging_Stations_Near_Work` | 0.002 | Useless |
| — | `Current_Car_Type` | 0.002 | Useless |
| — | `Number_of_Cars_Owned` | 0.0005 | Useless |
| — | `Gender` | 0.0003 | Useless |

---

## Key Insights per Feature

### 1. Environmental Concern Level — IV = 2.26 (Very Strong)

A perfectly monotonic relationship: the higher the environmental concern, the higher the EV purchase rate, with an extreme spread from under 1% to over 50%. No other feature shows this kind of linear dose-response.

| Concern Level | Event Rate | vs Average | WoE |
|---|---|---|---|
| Level 1 (lowest concern) | 0.6% | −16.9pp | +3.6 |
| Level 2 | 2.1% | −15.4pp | +2.3 |
| Level 3 | 11.1% | −6.4pp | +0.5 |
| Level 4 | 24.9% | +7.4pp | −0.4 |
| Level 5 (highest concern) | 51.8% | +34.3pp | −1.6 |

> **Business implication:** Environmental values are the single strongest predictor of EV interest in this dataset — and the relationship is perfectly graduated. A customer moving from concern level 1 to level 5 goes from a near-zero chance of purchase to a coin-flip likelihood. Segmenting by this score should be the first cut in any targeting or scoring model.

---

### 2. Subsidy Available — IV = 1.82 (Very Strong)

A stark binary split: subsidies are either available or not, and the effect on purchase rate is dramatic.

| Subsidy | Event Rate | vs Average | WoE |
|---|---|---|---|
| No subsidy | 0.6% | −16.9pp | +3.6 |
| Yes — subsidy available | 27.5% | +9.9pp | −0.6 |

> **Business implication:** Subsidy availability is the single most actionable lever in this dataset. Customers without access to subsidies almost never purchase an EV (0.6%), while those with subsidies convert at 27.5% — a 45× difference. This means subsidy eligibility decisions drive acquisition outcomes more than any demographic or behavioral characteristic. Expanding subsidy coverage to high-intent segments (high environmental concern + mid-to-high income) would have a direct and measurable impact on conversion.

---

### 3. Annual Income — IV = 0.43 (Strong)

A clear monotonic negative-WoE trend: the higher the income, the more likely a customer is to purchase an EV. The relationship is consistent across bins with no reversals.

| Income Range | Event Rate | vs Average | WoE |
|---|---|---|---|
| < $51k | 4.3% | −13.2pp | +1.5 |
| $51k – $68k | 7.5% | −10.0pp | +1.0 |
| $68k – $85k | 13.8%–16.1% | −0.4 to −3.7pp | +0.1 to +0.3 |
| $85k – $110k | 17.1%–22.9% | −0.1 to +5.2pp | −0.1 to −0.3 |
| $110k – $127k | 29.4% | +11.8pp | −0.7 |
| > $127k | 35.7% | +18.2pp | −1.0 |

> **Business implication:** Income is the most reliable legitimate driver of EV purchases. Customers earning below $51k are structurally unlikely buyers (4.3% purchase rate), while those above $127k represent the core market (35.7%). Marketing investment and subsidy design should concentrate on the $85k–$127k band where purchase rates rise steeply — this segment is price-sensitive enough that targeted incentives could meaningfully move conversion.

---

### 4. Range Anxiety Level — IV = 0.15 (Medium)

A binary split: customers who report high or medium range anxiety purchase at one-fifth the rate of those with low anxiety. The signal is concentrated in the high/medium group.

| Anxiety Level | Event Rate | vs Average | WoE |
|---|---|---|---|
| High or Medium | 4.0% | −13.4pp | +1.6 |
| Low | 18.9% | +1.4pp | −0.1 |

> **Business implication:** Range anxiety functions as a hard barrier, not a soft preference. Customers with high or medium range anxiety are nearly absent from EV purchases (4.0%). This points to a clear communication and product strategy: addressing real-world range concerns — through better range education, trial programs, or access to DC fast-chargers — could reactivate a meaningful portion of hesitant customers. This lever is more tractable than income.

---

### 5. Home Charging Possible — IV = 0.05 (Weak)

A small but consistent facilitator effect: customers without home charging are underrepresented among EV buyers.

| Home Charging | Event Rate | vs Average |
|---|---|---|
| No | 12.7% | −4.8pp |
| Yes | 19.6% | +2.1pp |

> **Business implication:** Home charging is a mild enabler — its absence is a friction point, but not a decisive barrier on its own. The effect is much smaller than range anxiety or income, suggesting it is a second-order concern for customers already inclined to buy. Pairing installation offers with EV promotions may help at the margin.

---

### 6. Daily Commute km — IV = 0.03 (Weak)

A non-monotonic pattern with no clean business narrative. The highest purchase rate appears in the 10–23 km range, while the lowest is among long-distance commuters (>58 km).

| Commute Range | Event Rate | vs Average |
|---|---|---|
| < 10 km | 18.4% | −0.1pp |
| 10–23 km | 22.5% | +4.9pp |
| 23–45 km | 17.5% | 0.0pp |
| > 58 km | 11.1% | −6.5pp |

> **Business implication:** Long-distance commuters (>58 km) show lower EV interest, likely due to range anxiety compounding with daily charging requirements. But the overall pattern is weak and non-linear. This feature should not be a prioritised segmentation axis.

---

### Features With No Signal

| Feature | IV | Why |
|---|---|---|
| `City_Type` | 0.008 | Urban/suburban/rural classification shows no meaningful difference in EV purchase rates |
| `Charging_Stations_Near_Home` | 0.007 | Counter-intuitively useless; proximity to infrastructure does not predict purchase behavior in this data |
| `Age` | 0.006 | No age group is meaningfully more or less likely to buy an EV |
| `Charging_Stations_Near_Work` | 0.002 | Same as home charging stations — no signal |
| `Current_Car_Type` | 0.002 | Current vehicle type (sedan, SUV, etc.) has no bearing on EV intent |
| `Number_of_Cars_Owned` | 0.0005 | Car ownership count is irrelevant |
| `Gender` | 0.0003 | No gender-based difference in EV purchase likelihood |

The absence of signal in charging station proximity is particularly notable — in policy discussions, charging infrastructure is often cited as a key adoption driver. This dataset suggests that the perception of range anxiety (a psychological variable) matters far more than actual charging access.

---

## Business Conclusion

**EV purchase likelihood is overwhelmingly determined by two factors: environmental values and subsidy access.** Together, `Environmental_Concern_Level` and `Subsidy_Available` account for the vast majority of the predictive signal (IV = 2.26 and 1.82 respectively), with income and range anxiety playing meaningful but secondary roles.

The practical implication is that demographics alone cannot identify EV buyers — what separates buyers from non-buyers is attitude (environmental concern) and policy context (subsidy access). A customer with high environmental concern and a subsidy available converts at rates far above the 17.5% baseline, while a low-concern customer without a subsidy is effectively a non-prospect regardless of their income or commute.

Seven features — including age, gender, car ownership, and charging infrastructure proximity — carry no predictive information and should be excluded from modelling.

---

## Recommendations

**1. Prioritize environmental concern score as the primary segmentation axis for all targeting.**
With IV = 2.26, it is by far the strongest predictor. Any model or campaign should use this as the first-cut filter. Customers at concern levels 4–5 represent the addressable market; levels 1–2 are effectively non-prospects under current conditions.

**2. Expand subsidy access to high-intent, mid-income segments.**
Subsidy availability drives a 45× difference in purchase rates. The highest-return intervention is directing subsidies toward customers with high environmental concern (levels 4–5) in the $85k–$127k income band — these customers are motivated but price-sensitive enough that subsidies are likely the decisive factor.

**3. Design a range anxiety intervention for the high/medium anxiety segment (9.7% of customers).**
This group purchases at 4.0% vs 18.9% for low-anxiety customers — a 4.7× gap driven by a single addressable perception. Test-drive programs, real-world range demonstrations, or partnered fast-charger guarantees could meaningfully close this gap without requiring subsidy spend.

**4. Deprioritize demographic and infrastructure features in targeting models.**
Age, gender, current car type, number of cars owned, and charging station proximity all have IV below 0.01. Including them adds noise without signal. Future data collection should focus on attitudinal and policy-context variables, which clearly outperform demographic proxies in this dataset.

---

## Appendix — Methodology

**IV Scale used:**

| IV | Label |
|---|---|
| < 0.02 | Useless |
| 0.02–0.10 | Weak |
| 0.10–0.30 | Medium |
| 0.30–0.50 | Strong |
| > 0.50 | Very Strong (check leakage) |

**Binning:** OptimalBinning with CP solver. Numerical features binned using optimal split points that maximize separation between event and non-event distributions. Categorical features (Gender, City_Type, Current_Car_Type, Home_Charging_Possible, Subsidy_Available, Range_Anxiety_Level) grouped by WoE profile similarity.

**Leakage check:** No features were excluded for leakage. `Environmental_Concern_Level` and `Subsidy_Available` both have IV > 0.5 and were reviewed — both confirmed as valid independent predictors.

**Output files:**
- `claude_outputs/ev_iv_analysis.md` — this report
- `claude_outputs/ev_iv_detail.xlsx` — full binning tables with IV/WoE for all features, color-formatted
- `claude_outputs/ev_iv_summary.csv` — machine-readable IV summary table
- `data/Silver layer/train_cleaned.csv` — cleaned training data with binary target encoding
