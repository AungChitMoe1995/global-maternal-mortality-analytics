# Limitations

1. **Modeled-outcome dependence:** GDP and general fertility help generate MMEIG estimates. GDP associations are not independent confirmation of economic effects. See [WHO methods](https://pmnch.who.int/docs/librariesprovider9/meeting-reports/9789240108462-web-final.pdf?sfvrsn=db2a572e_3), printed pages 20 and 24.
2. **Ecological inference:** National rates do not measure individual exposures, parity, spacing or clinical risk. National averages conceal subnational inequalities.
3. **Uncertainty:** Country posterior medians and marginal 80% limits do not provide joint posterior draws. Conditional regression CIs and endpoint sensitivity fits do not propagate all upstream uncertainty.
4. **Selection:** The balanced sample excludes 18 countries, including several conflict-affected settings. The unbalanced complete-case fit still excludes missing rows. No claim of representativeness follows from a high fraction of countries alone.
5. **Changing confounding and dependence:** Fixed effects do not remove changing conflict, service access, institutions or reverse causation. Cluster SE assume suitable independence between country clusters, which upstream shared modeling may weaken. Smooth modeled annual series contain less independent information than their row count suggests.
6. **Financing measurement:** CHE/GDP combines financing sources and is sensitive to its denominator. It cannot identify government commitment or maternal-care efficiency.
7. **Classification:** Income groups use the snapshot metadata for every historical year. Changing composition and historic income mobility are not studied.
8. **Diagnostics:** VIF, residual plots and country-omission checks reveal instability without curing confounding. Subgroup models have fewer clusters. No pre-registered causal design or out-of-sample prediction study is claimed.
9. **Data vintage:** WDI revisions can change values. The checked-in processed snapshot supports reproduction of this release; re-downloading is a new data version. Hashes verify identity, not correctness.
10. **Further work:** A defensible CRVS-quality sensitivity analysis needs country-period metadata. Full MMEIG uncertainty propagation requires appropriate joint posterior draws. These remain open methodological tasks rather than completed analyses.
