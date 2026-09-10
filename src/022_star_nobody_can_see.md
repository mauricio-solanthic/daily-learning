---
seq: 22
date: 2026-09-10
category: Economics
title: The Star Nobody Can See
slug: StarNobodyCanSee
deck: Trillions of dollars of bonds are repriced on quarterly wiggles in a number that no instrument measures and that its own machinery is built to move slowly.
slack: The neutral real interest rate, r-star, is the number central banks use to decide whether policy is tight or loose, and it is not measured but filtered — which makes it a moving average whose centre of mass sits about six years in the past. The sting is that the same estimator, re-run on samples the length of the one the New York Fed actually uses, returns exactly zero time variation in one sample out of seven: the single most likely finding is that the natural rate never moved at all. For 2024 Q2 four published models put it at 0.55, 0.74, 1.22 and 2.6 per cent, which makes the same federal funds rate anywhere from 0.8 to 2.8 percentage points restrictive.
burned:
  - The natural rate of interest r-star, the Laubach-Williams state-space model, and the uncertainty of estimating an unobservable
  - Wicksell's 1898 Geldzins und Guterpreise and the natural-versus-money rate distinction
  - The HLW decomposition r* = 4g + z and the uninterpretability of the z residual
  - The local level model as the canonical signal-extraction problem, and the Riccati fixed point p^2 - qp - q = 0
  - The steady-state Kalman gain K = p/(p+1), and K = 1/phi = 0.618 at unit signal-to-noise
  - The identity K approximately equals lambda for small signal-to-noise ratios (0.9802 at lambda = 0.040)
  - The filtered estimate as an exponentially weighted moving average with weights K(1-K)^j
  - Mean lag (1-K)/K - 24.5 quarters at HLW's lambda_z = 0.040, 76.4 at Buncic's corrected 0.013
  - Only 14.8 per cent of the weight on the most recent four quarters, 55 per cent on the most recent twenty
  - Inverting a smoothed estimate - the 2025-2026 LW move of 1.36 to 1.65 per cent implying a 1.6-point underlying shift
  - The pile-up problem - Gaussian MLE of a random-walk variance with an atom of probability at zero
  - Shephard and Harvey 1990's 0.96-versus-0.66 result for fixed versus diffuse initial level
  - The Monte Carlo reproducing 0.66 as 65.0 per cent, and 13.6 per cent zeros at HLW's own lambda on 250 quarters
  - The pile-up vanishing at 1,000 quarters, which is 250 years of quarterly data
  - Stock and Watson 1998 median-unbiased estimation by inverting a stability-test quantile function
  - Buncic's misspecified Stage 2 - lambda_z falling from 0.040 to 0.013 and r* rising by up to 100 basis points
  - Berger and Kempa 2019 finding time variation in trend growth but not in the other determinants
  - Real-time filtered uncertainty as sqrt(K) times the observation scale, confirmed at 0.1977 against 0.1980
  - Real-time error 1.40 times the final error, and RMS revision 0.65 to 1.28 times the true state's own variation
  - Orphanides and van Norden's finding that output-gap revisions are the same order as the gap
  - The four-model table for 2024 Q2 and the 0.78-to-2.83-point spread in measured policy stance
  - The Cleveland Fed's 3.7 per cent nominal neutral rate with a 68 per cent band of 2.9 to 4.5
  - The reported 95 per cent band on two-sided LW estimates running from about +5.5 to -4.5 per cent
  - The November 2020 suspension of LW and HLW publication and the May 2023 resumption
  - Orphanides on real-time potential-output mismeasurement as a cause of the Great Inflation
  - Orphanides and Williams's difference rules as the robust response to unknown natural rates
  - Openings now used up - the bond-market selloff read as news about an unobservable
next:
  - Potential output and the production-function approach to measuring capacity
  - Seasonal adjustment as a policy-relevant modelling choice rather than a technicality
  - The Beveridge curve, the natural rate of unemployment, and how a shifting curve is diagnosed
---

## Wicksell's Ghost in the Bond Market

In the autumn of 2026 the price of long-dated United States government debt fell, and the explanation offered by the people doing the selling was not about inflation, or deficits, or the Federal Reserve's next meeting. It was about a quantity called r-star: the real short-term interest rate that would prevail if output sat at potential and inflation were stable. The New York Fed had just published its Laubach-Williams estimate for the second quarter, 1.65 per cent, down from 1.73 in the first quarter and up from 1.36 a year and a bit earlier [1]. Analysts read the rise as evidence that heavy government borrowing and a wave of capital spending on artificial-intelligence infrastructure had permanently raised the rate at which capital clears, and priced bonds accordingly.

There is nothing wrong with the idea. Knut Wicksell introduced it in 1898, distinguishing the money rate observable in the capital market from what he called the natural rate — the return that would obtain in an imaginary economy with no money at all, where the supply and demand for goods clear directly [2]. If the money rate sits below the natural rate, credit is cheap relative to the return on real projects and prices climb cumulatively; above it, they fall. Every modern central bank runs on a version of this. The policy rate is judged tight or loose not against zero but against r-star.

What is strange is the epistemic status of the number being traded. No instrument measures r-star. It is not collected by a statistical agency, does not appear in any survey, and leaves no direct trace in any market price. It is an *estimate produced by a filter* — a statistical machine that takes observable series and infers a latent trend it assumes to be there. And when you look at what that machine actually does with the data, the quarterly movements everyone reads as news turn out to be nearly the last thing the machine is built to produce.

## What the Machine Actually Does

The workhorse is the model Thomas Laubach and John Williams published in 2003 [3], extended to several countries by Kathryn Holston with the same two authors in 2017 [4]. It is small and semi-structural. An IS curve relates the output gap to its own lags and to the gap between the real interest rate and r-star. A Phillips curve relates inflation to the output gap and to lagged inflation. Neither the output gap nor r-star is observed, so both are treated as unobserved states and the whole system is run through a Kalman filter, which is the optimal way to extract a hidden signal from noisy observations when you are willing to specify how much the signal moves.

The natural rate is then defined by construction as

$$ r^{*}_{t} = 4 g_{t} + z_{t} $$

where $g_t$ is the quarterly trend growth rate of potential output, annualised by the factor of four, and $z_t$ absorbs everything else — demographics, the demand for safe assets, whatever depresses or raises the equilibrium return that trend growth does not explain. Both $g$ and $z$ are modelled as random walks. That choice is what makes the estimate possible and what makes it fragile, because a random walk has no level to revert to; the filter can only ever say where the walk has drifted, never where it belongs.

The critical parameters are not the interest-rate coefficients but two ratios of standard deviations, written $\lambda_g$ and $\lambda_z$, which govern how much of the innovation in the data the filter is willing to attribute to a genuine shift in the trend rather than to noise. Holston, Laubach and Williams estimate $\lambda_z$ at 0.040 for the United States. That single small number does more to determine the shape of the published series than any other quantity in the model, and its consequences can be worked out exactly.

## The Arithmetic of a Deliberately Slow Number

Strip the model to its skeleton and you get the canonical signal-extraction problem, the local level model:

$$ x_{t} = x_{t-1} + \eta_{t}, \qquad y_{t} = x_{t} + \varepsilon_{t} $$

with $\eta$ and $\varepsilon$ independent and the ratio of their standard deviations equal to $\lambda$, so that the ratio of variances is $q = \lambda^2$. In steady state the filter's prior variance $p$, measured in units of the noise variance, satisfies $p = p/(p+1) + q$, which rearranges to $p^{2} - qp - q = 0$, so

$$ p = \frac{q + \sqrt{q^{2} + 4q}}{2}, \qquad K = \frac{p}{p+1} $$

where $K$ is the Kalman gain: the fraction of each period's surprise that gets written into the estimate. Iterating the recursion numerically for two hundred thousand steps reproduces the closed form to machine precision. At unit signal-to-noise the arithmetic is charming — $p$ is exactly the golden ratio 1.6180 and $K$ is its reciprocal, 0.6180 — and for small $q$ the gain collapses to something more useful: $K$ is within two per cent of $\lambda$ itself. Holston, Laubach and Williams's $\lambda_z$ of 0.040 therefore implies a gain of 0.0392.

That is the whole story, because a constant-gain filter is an exponentially weighted moving average. The estimate at any date is

$$ \hat{x}_{t} = K \sum_{j \ge 0} (1-K)^{j} y_{t-j}, \qquad \text{mean lag} = \frac{1-K}{K} $$

and at $K = 0.0392$ the mean lag is 24.5 quarters. The centre of mass of a published real-time r-star estimate sits **six years and one month in the past**. The most recent four quarters of data carry 14.8 per cent of the weight between them; it takes twenty quarters to accumulate 55 per cent. The right-hand panel of the figure below draws the profile.

The same fraction runs the other way, which is where the arithmetic stops being a technicality. Suppose the natural rate really did jump permanently at some date. After four quarters the estimate has moved 14.8 per cent of the distance; the half-life is 17.3 quarters, or four years and four months. So an observed move in the estimate is a heavily shrunken image of the move in the thing estimated. Run the 2026 numbers through it: a rise from 1.36 per cent to 1.65 over five quarters, seen through a filter that recognises 18.1 per cent of a permanent shift in that span, is what a genuine jump of about 1.6 percentage points would look like. Taking the peak instead — 1.36 to 1.73 over four quarters — implies 2.5 points.

:::think Which way does the error point?
A bond desk reading a 29-basis-point rise in r-star as a 29-basis-point rise in the neutral rate is not making a small error in the obvious direction.
:::

Neither reading is available as a measurement, and that is the point. If the move is real and recent, the estimate is understating it by a factor of five. If the estimate is roughly right about the level, then it is not telling anyone anything about 2026 — it is telling them, with a lag of six years, about 2020. The one interpretation the arithmetic forbids is the one the market made: that a quarterly change in the estimate is a quarterly change in the world.

## The Estimate That Would Rather Not Move

There is a deeper problem, and it concerns $\lambda$ itself. That parameter cannot be assumed; it has to be estimated from the same data. And estimating how much a random-walk trend moves is one of the known pathologies of time-series statistics.

Gaussian maximum likelihood applied to a variance that might be zero has an atom of probability at zero. The likelihood is maximised at the boundary in a large fraction of samples — the *pile-up problem*, characterised for exactly this model by Neil Shephard and Andrew Harvey in 1990 [5]. Their result is stark: when the true signal-to-noise ratio is zero, the probability that maximum likelihood returns zero is 0.96 if the initial level is treated as an unknown constant, and 0.66 under a diffuse prior. A simulation of twenty thousand samples of 250 quarters with a diffuse start returns exactly zero in 65.0 per cent of them, which reproduces the published 0.66 from a paper that could not be opened, by arithmetic a summary cannot fake.

![Left: maximum likelihood re-estimates of the signal-to-noise ratio across 20,000 simulated samples of 250 quarters, generated at the value Holston, Laubach and Williams report. The orange bar is an atom of probability at exactly zero, not a histogram bin. Right: the weight a steady-state filter places on each past quarter, with the mean lag marked.](../figures/022-pileup-and-weight-profile.png)

The interesting case is not zero but the value actually reported. Simulating 250 quarters — roughly the length of the sample the New York Fed's model runs on — at a true $\lambda$ of 0.040, and re-estimating by maximum likelihood on each, returns *exactly zero* in 13.6 per cent of samples. One sample in seven concludes that the natural rate has no time-varying component at all. The median estimate comes back at 0.0351 rather than 0.040, biased toward stillness. At $\lambda = 0.030$, the value reported for trend growth, 21.3 per cent of samples return zero: more than one in five. Lengthen the sample to a thousand quarters and the pathology essentially vanishes, falling to 0.1 per cent — but a thousand quarters is two hundred and fifty years of quarterly national accounts, so this is not a problem that patience solves.

Laubach and Williams knew this, which is why they do not use maximum likelihood for these two parameters. They use the median-unbiased estimator James Stock and Mark Watson published in 1998, which sidesteps the boundary by inverting the quantile function of a parameter-stability test statistic computed under the constant-parameter null [6]. It is an ingenious repair, and its use here has been contested. Daniel Buncic argues that the second stage of the procedure, as implemented, rests on a misspecified model and cannot recover the ratio it is meant to identify, spuriously amplifying it instead; correcting the implementation drops the United States estimate of $\lambda_z$ from 0.040 to 0.013 and raises the level of r-star by up to a hundred basis points [7]. Feed 0.013 back through the gain formula and the mean lag stretches from 24.5 quarters to 76.4 — from a six-year moving average to a nineteen-year one, with only 5.1 per cent of the weight on the most recent year. An estimate averaged over nineteen years does not have a downward trend to explain, which is precisely Buncic's finding.

Tino Berger and Bernd Kempa reach the question from another direction, using Bayesian model selection to ask whether the time variation is there at all. They find it in trend growth and not in the other determinants, which are better described as constant [8]. Between them, these two results say that the component of r-star with no economic interpretation may also have no statistical existence.

## How Wrong, and Who Pays

The uncertainty comes in three flavours, and only the first is routinely reported.

The narrowest is the filter's own uncertainty about the state given the parameters. For the local level model this has a closed form: the real-time standard error is $\sqrt{K}$ times the noise scale, which at $K = 0.0392$ is 0.198, confirmed against simulation at 0.1977. Second is the revision that arrives when future data are added, turning a real-time estimate into a final one. In simulation the real-time error is 1.40 times the final error at both calibrations, and the root-mean-square revision between the two is 0.65 times the true trend's own variation at $\lambda = 0.040$ and 1.28 times it at 0.013. That last figure deserves a moment: the revision is *larger* than the movement being revised. It is also an old finding. Athanasios Orphanides and Simon van Norden established for the output gap in 2002 that ex post revisions run to the same order of magnitude as the estimated gap itself [9] — a result the arithmetic above reproduces from nothing but a signal-to-noise ratio.

Third and largest is uncertainty about the model. Published bands are wide even before you get there. A Cleveland Fed model puts the nominal neutral rate at 3.7 per cent with a 68 per cent coverage band of 2.9 to 4.5 [10], an interval 1.6 points across at one standard deviation. A survey chapter in a Hoover Institution volume reads the 95 per cent band on the two-sided Laubach-Williams estimates as running from roughly +5.5 to −4.5 per cent [11], which implies a standard error near 2.55 points and makes the entire recorded variation in the series statistically indistinguishable from a flat line.

Model uncertainty shows up most cleanly when several estimates are laid against the same quarter. For 2024 Q2, a Richmond Fed comparison reports four [12]:

| Estimate for 2024 Q2 | r-star | Nominal neutral | Stance |
|---|---|---|---|
| Lubik-Matthes | 2.60 | 4.60 | 0.78 |
| Laubach-Williams | 1.22 | 3.22 | 2.16 |
| Holston-Laubach-Williams | 0.74 | 2.74 | 2.63 |
| New York Fed DSGE | 0.55 | 2.55 | 2.83 |

Nominal neutral adds the two-per-cent inflation target; stance subtracts it from 5.375, the midpoint of the federal funds target range then in force, in percentage points. The four models span 2.05 points, and the same policy rate is therefore between 0.78 and 2.83 points restrictive depending on which is chosen — a factor of 3.65 in the measured tightness of monetary policy, at one date, with no data in dispute. Robert Beyer and Volker Wieland made the general version of this argument: the estimates are unstable, imprecise, and used inconsistently [13]. Marco Del Negro and colleagues, working from a quite different model built around the demand for safe and liquid assets, get a different series again [14], and Michael Kiley's survey finds that global factors dominate the trend in every advanced economy, which shifts the United States estimate below what United States-only models produce [15].

## The Precedent

None of this is hypothetical, because the same class of error has already produced a monetary disaster. Through the 1970s the Federal Reserve's real-time estimates of potential output badly overstated the economy's capacity, so the output gap looked far more negative than it was. Policy that appeared appropriate against the real-time gap was in fact strongly expansionary, and Orphanides's counterfactual simulations attribute much of the Great Inflation to precisely that mismeasurement rather than to bad intentions or a bad rule [16]. The natural rate of interest is the same object with a different name: an unobservable, estimated by filtering, entering the policy rule one-for-one, so that an error in it becomes a permanent error in the rate.

The response Orphanides and Williams proposed is worth more than the estimate itself. If the level of a natural rate cannot be pinned down, write rules that do not require it — *difference rules*, which respond to changes in unemployment and inflation rather than to levels measured against an unknown benchmark. Such rules are less efficient when the natural rate happens to be known, and far more robust when it is not [17]. Laubach and Williams themselves concluded, in their own retrospective, that uncertainty about the natural rate argues for approaches more robust to mismeasuring it [18].

The institutional record makes the fragility hard to deny. The New York Fed suspended publication of both models in November 2020, after the extreme volatility of pandemic-era GDP, and did not resume until May 2023, when the estimates were released again with a modified specification allowing for time-varying volatility and a persistent supply shock [19]. Whatever else that gap means, a measurement that must be withdrawn when the economy moves sharply is not a measurement. And in August 2026 a San Francisco Fed letter, working from a medium-run concept, concluded that the policy rate might sit *below* neutral — that policy was accommodative rather than restrictive — while noting that uncertainty around the estimate remains high [20].

The right conclusion is not that r-star is useless. It is a real economic object, and the filters are honest attempts to see it. The conclusion is that the published series is not a reading but a long, slow average, whose centre of mass lies years behind its own date, whose defining parameter is the hardest thing in the model to estimate, and whose confidence interval swallows the whole of the debate conducted inside it. A number like that can support a judgement about a decade. It cannot support a trade on a quarter.

## References

1. "Measuring the Natural Rate of Interest," Federal Reserve Bank of New York, r-star estimates and real-time series; and "Bond selloff is likely amplified by obscure economic rate," Reuters, Sept. 2026.
2. K. Wicksell, *Interest and Prices*, R. F. Kahn, trans. London: Macmillan, 1936; orig. *Geldzins und Güterpreise*, 1898.
3. T. Laubach and J. C. Williams, "Measuring the Natural Rate of Interest," *Review of Economics and Statistics*, vol. 85, no. 4, pp. 1063-1070, 2003.
4. K. Holston, T. Laubach, and J. C. Williams, "Measuring the Natural Rate of Interest: International Trends and Determinants," *Journal of International Economics*, vol. 108, suppl. 1, pp. S59-S75, 2017.
5. N. Shephard and A. C. Harvey, "On the Probability of Estimating a Deterministic Component in the Local Level Model," *Journal of Time Series Analysis*, vol. 11, no. 4, pp. 339-347, 1990.
6. J. H. Stock and M. W. Watson, "Median Unbiased Estimation of Coefficient Variance in a Time-Varying Parameter Model," *Journal of the American Statistical Association*, vol. 93, no. 441, pp. 349-358, 1998.
7. D. Buncic, "Econometric Issues in the Estimation of the Natural Rate of Interest," *Economic Modelling*, vol. 132, art. 106641, 2024.
8. T. Berger and B. Kempa, "Testing for Time Variation in the Natural Rate of Interest," *Journal of Applied Econometrics*, vol. 34, no. 5, pp. 836-842, 2019.
9. A. Orphanides and S. van Norden, "The Unreliability of Output-Gap Estimates in Real Time," *Review of Economics and Statistics*, vol. 84, no. 4, pp. 569-583, 2002.
10. "Neutral Interest Rates and the Monetary Policy Stance," Federal Reserve Bank of Cleveland Economic Commentary no. 2025-08, 2025.
11. "R-Star: The Natural Rate and Its Role in Monetary Policy," in *The Structural Foundations of Monetary Policy*, M. D. Bordo, J. H. Cochrane, and A. Seru, Eds. Stanford, CA: Hoover Institution Press, 2018.
12. "Examining the Differences in r* Estimates," Federal Reserve Bank of Richmond Economic Brief no. 24-36, Nov. 2024.
13. R. C. M. Beyer and V. Wieland, "Instability, Imprecision and Inconsistent Use of Equilibrium Real Interest Rate Estimates," *Journal of International Money and Finance*, vol. 94, pp. 1-14, 2019.
14. M. Del Negro, D. Giannone, M. P. Giannoni, and A. Tambalotti, "Safety, Liquidity, and the Natural Rate of Interest," *Brookings Papers on Economic Activity*, vol. 48, no. 1, pp. 235-316, 2017.
15. M. T. Kiley, "The Global Equilibrium Real Interest Rate: Concepts, Estimates, and Challenges," *Annual Review of Financial Economics*, vol. 12, pp. 305-326, 2020.
16. A. Orphanides, "The Quest for Prosperity without Inflation," *Journal of Monetary Economics*, vol. 50, no. 3, pp. 633-663, 2003.
17. A. Orphanides and J. C. Williams, "Robust Monetary Policy Rules with Unknown Natural Rates," *Brookings Papers on Economic Activity*, vol. 2002, no. 2, pp. 63-118, 2002.
18. T. Laubach and J. C. Williams, "Measuring the Natural Rate of Interest Redux," *Business Economics*, vol. 51, pp. 57-67, 2016.
19. K. Holston, T. Laubach, and J. C. Williams, "Measuring the Natural Rate of Interest after COVID-19," Federal Reserve Bank of New York Staff Report no. 1063, June 2023.
20. "Assessing a Medium-Run Natural Rate of Interest," Federal Reserve Bank of San Francisco Economic Letter, Aug. 2026.
