# Global Maternal Mortality, 2000–2023
## Trends, inequalities and exploratory associations

**Author:** Dr. Aung Chit Moe, MBBS. Secondary analysis of public country aggregates.

## Question

How did estimated national maternal mortality change, how unequal were those trends, and what associations appeared with economic and demographic indicators?

## Data and approach

The study integrates the MMEIG 2025 estimation round with WDI. Descriptive analyses retain 195 countries and territories (4,680 country-years). The balanced regression uses 177 countries (4,248 rows). An unbalanced model includes 4,406 complete rows. [Methods](methodology.md) explain estimands, source dependence and conditional inference.

## Descriptive results

|   year |   median_mmr |   mean_mmr |   aggregate_mmr |
|-------:|-------------:|-----------:|----------------:|
|   2000 |        70.99 |     235.48 |          325.24 |
|   2010 |        56.14 |     185.89 |          251.57 |
|   2015 |        51.87 |     155.75 |          223.83 |
|   2023 |        46.65 |     116.62 |          188.67 |

Mean and median weight countries equally. The derived aggregate uses country median death estimates and births and may differ from the official global posterior result. Income trajectories use one fixed classification. They do not describe historical income mobility.

## Selection

|   year | group    |   n_countries |   median_mmr |   mean_mmr |
|-------:|:---------|--------------:|-------------:|-----------:|
|   2000 | Included |           177 |        67.64 |     217.74 |
|   2000 | Excluded |            18 |       137.24 |     409.93 |
|   2023 | Included |           177 |        42.11 |     109.57 |
|   2023 | Excluded |            18 |        92.65 |     186.02 |

Included and excluded countries differ. Several excluded settings have substantial conflict or data gaps. Neither sample provides an unbiased representation merely because many countries remain.

## Exploratory regressions

The balanced-panel GDP slope is -0.496 (95% CI -0.648 to -0.344). Corresponding slopes are -0.494 (95% CI -0.636 to -0.352) for all complete rows, -0.527 (95% CI -0.698 to -0.355) before 2020, and -0.201 (95% CI -0.303 to -0.099) for consecutive first differences. These are model coefficients, not estimated intervention effects. All predictors, uncertainty intervals, income subset fits and diagnostics appear in the [statistical report](statistical_analysis.md).

The apparent GDP relationship requires special caution: the MMEIG model already uses GDP, general fertility and skilled birth attendance. These regressions do not independently discover an economic effect on maternal mortality. Replacing modeled outcomes by their marginal lower/upper limits does not fully propagate posterior uncertainty.

## Interpretation

The project demonstrates persistent country-level differences and explores specification sensitivity. It cannot identify clinical pathways, individual pregnancy risk or the effects of government spending. National fertility does not establish individual parity or spacing. CHE/GDP does not isolate government priority. The research can inform better questions and further data collection without supplying an intervention recommendation.

## Contribution and next work

The portfolio contribution is the reproducible integration of public data, explicit handling of coverage and estimands, and consistent communication of methodological limits. Additional work should prioritize source-quality metadata and uncertainty propagation before stronger etiological claims. See [limitations](limitations.md) and the retrospective [analysis-plan amendment](research_protocol.md).

Sources: [WHO/UN MMEIG](https://www.who.int/publications/i/item/9789240108462), [World Bank WDI](https://databank.worldbank.org/source/world-development-indicators), and the [source register](source_register.md). AI tools assisted implementation and review. The author directed the project questions and reviewed outputs within his current technical understanding.
