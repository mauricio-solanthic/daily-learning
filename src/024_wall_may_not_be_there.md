---
seq: 24
date: 2026-09-18
category: Cross-Domain Synthesis
title: The Wall That May Not Be There
slug: WallMayNotBeThere
deck: Flood engineers, reinsurers and ceramicists design against catastrophe with the same equation, and disagree only about the sign of one number.
slack: Dike heights, reinsurance treaties and the strength of a ceramic bearing all come out of one three-parameter family, and the entire question of whether a worst case exists reduces to the sign of a single shape parameter. Fit three of them to the same century of annual maxima and they agree to within 23 cm at a ten-year return period, then disagree by 4.46 m at ten thousand years — one of them insisting on a hard ceiling at 5.00 m that no storm can ever pass. Van Dantzig's 1956 cost-benefit calculation for the Dutch coast wanted a one-in-125,000-year dike; the Delta Committee legislated one-in-10,000 and built barely half the height he recommended.
burned:
  - Extreme value theory as a cross-domain skeleton spanning hydrology, insurance and materials failure
  - The Fisher-Tippett-Gnedenko theorem, max-stability, and the three limiting families
  - Jenkinson's 1955 unification into the generalised extreme value distribution and the single shape parameter xi
  - The sign of xi as the whole question of whether a finite upper endpoint exists
  - The upper endpoint mu - sigma/xi and the worked case that lands on exactly 5.00 m
  - The three-curve return level comparison at mu = 3.00 m, sigma = 0.30 m - 23 cm apart at ten years, 4.46 m apart at ten thousand
  - Increments per decade of rarity - constant sigma ln 10 at xi = 0, multiplicative 10^xi above, shrinking below
  - The 1-in-T event over T years converging to 1 - 1/e = 0.6321, and 0.2603 over a thirty-year mortgage
  - Emil Gumbel counting Weimar political murders, losing Heidelberg in 1932, and becoming the father of applied extreme value statistics
  - Wemelsfelder's 1939 straight line on logarithmic paper as a knife-edge xi = 0 assumption
  - Van Dantzig's 1956 Econometrica cost-benefit model for the Dutch Delta Committee
  - The 1/125,000 economic optimum against the 1/10,000 legislated standard, and 115 cm built of 215 cm recommended
  - The 1953 North Sea flood, 1,836 Dutch deaths, and design levels of 3.85, 5.00 and 6.00 m NAP at Hoek van Holland
  - Weibull's weakest-link chain, the 1939 IVA paper and the 1951 Journal of Applied Mechanics paper
  - The Weibull modulus m and the size effect sigma proportional to volume to the power -1/m
  - Four decades of volume costing a factor of 6.31 in strength at m = 5 and 1.45 at m = 25
  - Weibull as a minimum problem and therefore the same theorem run upside down
  - The generalised Pareto distribution, peaks over threshold, Pickands 1975 and Balkema-de Haan 1974
  - The Danish fire insurance data straddling xi = 0.5, the exact boundary of finite variance
  - Hill's alpha of 2.01 at threshold 10 against a generalised Pareto xi of 0.684 at threshold 20
  - The penultimate approximation, xi_n = -1/(2 ln n), and the normal maximum that looks bounded at every finite n
  - Gumbel approximation error for normal maxima still 2 per cent at a trillion observations
  - The 2021 Lytton record of 49.6 C, 4.6 C above the previous Canadian mark, outside a fitted GEV's upper bound
  - Framings now exhausted - the record that fell outside its own fitted curve, and the fanning return-level chart
next:
  - Percolation proper - lattice thresholds, universality classes and substance-independent exponents
  - The renormalisation group as the reason unrelated systems share critical exponents
  - Cascading failure in interdependent networks and branching models of blackout size
---

On 29 June 2021 the village of Lytton, in the dry canyon country of interior
British Columbia, reached 49.6 degrees Celsius. The Canadian national record
before that week had stood since July 1937 at 45.0 degrees, set on the
Saskatchewan prairie. Lytton did not edge past it. Lytton beat it by 4.6
degrees, on the third consecutive day of breaking it, and burned down the next
day.

What makes the number unsettling is not its size but its position. Statisticians
who fit distributions to annual maximum temperatures for a living had fitted one
to the Pacific Northwest, using seventy years of observations and allowing the
distribution to drift upward with global mean temperature. The June 2021
reading did not sit in the far tail of that fitted curve. It sat outside it
altogether, beyond the largest value the fitted distribution assigned any
probability at all [1]. The model had not merely been surprised. It had
contained a wall, and the weather had walked through the place where the wall
was supposed to be.

That wall is a single parameter, and its sign is the subject of this piece. The
same parameter, in a different profession, decides how high to build a sea dike;
in a third, what a reinsurance layer is worth; in a fourth, how much strength a
ceramic component loses when you scale it up. These trades do not read each
other's journals. They are nevertheless solving the same equation, and almost
all of their practical disagreements reduce to what they believe about one
number.

## Only Three Things a Maximum Can Do

The central theorem of the subject was proved in Cambridge in 1928 by Ronald
Fisher and Leonard Tippett, and given its modern necessary-and-sufficient form
by Boris Gnedenko in 1943 [2], [3]. It concerns the largest of $n$ independent
draws from some distribution. Nobody knows what that distribution is — that is
the point — and for almost any interesting question nobody ever will.

The theorem says this. Suppose you take the maximum of $n$ draws, recentre and
rescale it so that it settles down as $n$ grows, and suppose the result
converges to something non-degenerate at all. Then that something must be one of
exactly three distributions. Not approximately three. Three.

The reasoning is a stability argument of striking economy. The maximum of $2n$
draws is the maximum of two independent maxima of $n$ draws each. So whatever
limiting law $G$ the maximum obeys, $G^2$ must be the same law with different
centring and scale; the same for $G^3$, and for every power. Very few functions
survive that constraint, and solving for them yields the three families.
Everything else about the parent distribution — its mean, its skewness, whether
it is a sum of a thousand small effects or the product of a dozen large ones —
washes out.

Anthony Jenkinson noticed in 1955 that the three families are one family wearing
three hats, and wrote them as a single expression [4], now universal as the
generalised extreme value distribution:

$$ G(z) \;=\; \exp\!\left\{-\left[1+\xi\left(\frac{z-\mu}{\sigma}\right)\right]^{-1/\xi}\right\} $$

with $\mu$ a location, $\sigma > 0$ a scale, and $\xi$ the shape. The case
$\xi = 0$ is read as the limit, giving the double-exponential Gumbel law. What
was three qualitatively different answers becomes one continuous dial [5].

And the dial is not a refinement. It decides the question everyone actually
cares about. When $\xi < 0$ the distribution has a finite upper endpoint,

$$ z_{\max} \;=\; \mu - \frac{\sigma}{\xi} $$

above which nothing can ever be observed, no matter how long you wait. When
$\xi > 0$ the tail is a power law with index $1/\xi$, unbounded, and heavy
enough that high moments cease to exist. When $\xi = 0$ the tail is exponential:
unbounded, but only barely, and with every moment finite. One number decides
whether the worst case is a wall, a cliff or a slope.

| Shape | Family | Tail behaviour | Typically fitted to |
|---|---|---|---|
| $\xi < 0$ | Weibull | bounded above | material strength, annual maximum temperature |
| $\xi = 0$ | Gumbel | exponential | storm surge, classical flood design |
| $\xi > 0$ | Fréchet | power law | fire and liability losses, extreme rainfall |

The names carry an irony worth noting. Emil Julius Gumbel, whose name sits on
the middle row and who did more than anyone to turn this theorem into an
engineering tool, first became known for a different kind of counting. In 1922
he published a tally of the political murders of the early Weimar Republic,
finding that the overwhelming majority were committed from the right and that
almost none of those were punished [6]. It cost him his chair at Heidelberg in
1932, and then his citizenship. He arrived at flood statistics as an exile, and
the textbook that made the field practical appeared in New York in 1958 [7].

## What A Return Period Actually Says

Engineering does not speak in shape parameters. It speaks in return periods: the
hundred-year flood, the ten-thousand-year sea level, the fifty-year wind. A
return period of $T$ years names the level exceeded by one annual maximum in
$T$, and inverting the expression above gives the level directly. Writing
$y_T = -\ln(1 - 1/T)$ for the annual exceedance rate, the level is

$$ z_T \;=\; \mu + \frac{\sigma}{\xi}\Big(y_T^{-\xi} - 1\Big), \qquad
   z_T \;=\; \mu - \sigma \ln y_T \ \ \text{when } \xi = 0 $$

Two things about that phrase deserve more suspicion than they get. The first is
elementary and still routinely misread. A one-in-hundred-year flood is not a
flood that arrives every century. If exceedances are independent from year to
year, the chance of at least one in a hundred years is $1 - (1 - 1/100)^{100}$,
which is 0.6340 — and as $T$ grows this converges to $1 - 1/e$, or 0.6321. Over
a thirty-year mortgage the same flood has probability 0.2603. Gumbel was making
this point to hydrologists in 1941 [8], and it still needs making.

:::think Before reading on
A coastal authority has a century of annual maximum sea levels and must design
for the level exceeded once in ten thousand years. How much of that answer is
coming from the data?
:::

The second is the real problem, and the figure below is the whole of it. Take
three generalised extreme value distributions with identical location
$\mu = 3.00$ metres and identical scale $\sigma = 0.30$ metres, differing only
in shape: $\xi = -0.15$, $\xi = 0$ and $\xi = +0.15$. Over the range a century
of annual records actually constrains, they are nearly the same distribution. At
a ten-year return period their levels are 3.57, 3.68 and 3.80 metres — a spread
of 23 centimetres, comfortably inside the sampling noise of a hundred
observations. No goodness-of-fit test on such a record will confidently separate
them.

Now extrapolate. At ten thousand years the three give 4.50, 5.76 and 8.96
metres. The spread is 4.46 metres: nineteen times what it was, and the
difference between a dike and a decision to move the city. The $\xi = -0.15$
curve, moreover, is bounded by $\mu - \sigma/\xi = 5.00$ metres exactly. Not
5.00 metres at ten thousand years — 5.00 metres at any return period whatsoever,
a level that a million years of storms cannot reach.

![Left: three GEV distributions with the same location and scale, differing only in shape, fanning out beyond the range the data constrain. Right: the shape parameter fitted to simulated maxima of n standard normal variables, against the penultimate value −1/(2 ln n).](../figures/024-shape-parameter.png)

The structure underneath is simple enough to state in words. Each factor of ten
in rarity adds a fixed increment $\sigma \ln 10 = 0.691$ metres when $\xi = 0$;
above zero, each factor of ten multiplies the excess over $\mu$ by $10^{\xi}$
asymptotically; below zero the increments shrink geometrically and sum to a
finite total. The answer to the call-out is therefore uncomfortable. The data
supply $\mu$ and $\sigma$ with reasonable precision. They barely constrain
$\xi$, and $\xi$ is what the extrapolation runs on.

## A Dike, An Economist And A Straight Line

The Dutch confronted this earlier and more seriously than anyone, because they
had to. In 1939 Pieter Wemelsfelder, an engineer at Rijkswaterstaat, plotted
half a century of high waters at Hoek van Holland on logarithmic paper and found
that the exceedance frequencies fell close to a straight line [9]. He drew the
correct and radical conclusion: design should be against a stated probability
rather than against the highest level anyone happened to have seen, and on that
basis many Dutch dikes were too low.

The argument was not acted upon. On the night of 31 January 1953 a North Sea
surge overtopped and breached the defences of Zeeland and South Holland and
killed 1,836 people. The Delta Committee convened afterwards did something no
flood authority had done before: it asked a mathematician what the right
probability was.

David van Dantzig's answer appeared in *Econometrica* in 1956 [10]. He wrote the
present value of expected flood losses as damage multiplied by an exceedance
probability that falls exponentially in dike height, added the cost of
construction, and minimised the sum. It is a clean piece of operations research
— the marginal metre of dike is built when it costs less than the discounted
risk it removes — and its descendants still govern Dutch investment decisions.

What happened next is the part worth keeping. His calculation for the heart of
Holland pointed to an exceedance probability of one in 125,000 per year and a
design level at Hoek van Holland of about 6 metres above the Amsterdam datum — a
rise of 215 centimetres on the 3.85 metres then in place. The standard written
into Dutch law in 1958 was one in 10,000 per year, twelve and a half times less
demanding, and the level chosen was 5.00 metres, a rise of 115 centimetres. Just
over half the height the economics recommended, and the economics was
acknowledged at the time as one argument among several rather than the decisive
one [11].

It is tempting to read that as politics overruling arithmetic, and that is
partly what it was. But notice what the arithmetic rested on. Wemelsfelder's
straight line on log paper is precisely the assumption that $\xi = 0$ — an
exponential tail, the knife edge between a bounded world and a power-law one. It was adopted
because the plotted points looked straight over the range that had been
observed, which is exactly the range in which the figure above shows all three
shapes looking alike. Later Dutch work took the shape parameter seriously as a
quantity to be estimated rather than assumed, and Laurens de Haan's 1990 account
of that effort remains the best description of what it is like to extrapolate a
tail three orders of magnitude beyond your data with a country underneath it
[12].

## The Weakest Link And The Heaviest Loss

Two other professions found the same three families by walking in from opposite
directions.

Waloddi Weibull was a Swedish engineer interested in why nominally identical
specimens break at wildly different stresses. His answer, published in 1939 and
restated for an American audience in 1951, was that a brittle body is a chain
[13], [14]. It contains flaws of random severity, and it fails when the worst
flaw in it fails. The strength of the body is therefore the *minimum* over its
flaws — and a minimum is a maximum upside down, so the same theorem applies. The
distribution that bears his name is what you get.

The consequence engineers care about follows in two lines. If a body of volume
$V$ survives stress $\sigma$ with probability $\exp[-V(\sigma/\sigma_0)^m]$,
then setting the survival probabilities of two sizes equal gives

$$ \frac{\sigma_2}{\sigma_1} \;=\; \left(\frac{V_1}{V_2}\right)^{1/m} $$

Big things are weaker than small things made of the same material, because they
contain more chances to be unlucky, and the exponent is the reciprocal of the
Weibull modulus $m$. For ordinary glass, with $m$ around 5, four decades of
volume cost a factor of 6.31 in strength. For a well-made alumina at $m = 10$
the same scaling costs 2.51, and at $m = 25$ only 1.45. The modulus is
effectively a quality metric: a material with a high $m$ is one whose worst flaw
is predictable. Weibull's 1951 paper, it is worth recording, was received with
open scepticism, and he conceded that he had no theoretical derivation and
doubted one was available.

Insurance came in from the other side and found the third family. The relevant
machinery is not block maxima but exceedances: given that a loss is larger than
some threshold $u$, how much larger? James Pickands in 1975, and August Balkema
and Laurens de Haan in 1974, established that the answer converges to the
generalised Pareto distribution, with the same shape parameter $\xi$ as the
corresponding extreme value limit [15], [16]. Bruce Hill's estimator of that
parameter, from the same year, remains the standard first look at a fat tail
[17].

Here the sign of $\xi$ is not about a ceiling; it is about whether the ordinary
apparatus of insurance works at all. Under the generalised Pareto the mean loss
is finite only when $\xi < 1$, and the variance only when $\xi$ is below one
half. Above that second threshold the law of large numbers stops being useful: pooling more
policies no longer makes the average predictable, because the average is
dominated by whichever single claim happens to be largest.

Which brings us to the best-studied loss dataset in the literature. Alexander
McNeil's 1997 study of large Danish fire insurance claims — 2,156 losses above
one million kroner — fitted a generalised Pareto above a threshold of 20 million
and obtained $\xi = 0.684$, a tail index of $1/0.684 = 1.46$ [18]. Analyses of
the same losses using Hill's estimator at a threshold of 10 put the index nearer
2.01, or $\xi \approx 0.50$; Sidney Resnick's companion discussion, printed
immediately after McNeil's paper in the same issue, is largely about how
unstable that choice of threshold makes the answer [19].

:::think Worth pausing on
Careful analyses of one loss dataset, differing mainly in where they cut the
threshold, straddle the exact value at which the variance of a fire loss becomes
infinite.
:::

That is not a failure of either analysis. It is what tail estimation looks like:
the answer depends on where you cut the threshold, and there is no consistent
estimator that avoids the choice. The practical reading is that Danish fire
losses sit close enough to $\xi = 1/2$ that a reinsurer cannot know from the
data whether the variance of its own portfolio exists — and a difference of 0.18
in $\xi$ corresponds, deep in the tail, to a 1-in-1,000 loss that is 3.2 rather
than 4.8 times the 1-in-100 loss, which is precisely the number a treaty is
priced on [20].

## The Fine Print In The Theorem

The theorem promises that the maximum converges to one of three laws. It says
nothing whatever about how fast.

For the normal distribution, the news is bad in an interesting way. Normal
maxima do converge, to the Gumbel law with $\xi = 0$. But Fisher and Tippett
noticed in their original 1928 paper that the approach is so slow as to be
useless, and that finite samples are better fitted by a *bounded* distribution
with $\xi < 0$ [2]. The modern statement, sharpened by Joan Cohen in 1982, is
that the best shape parameter for the maximum of $n$ standard normals is
approximately $-1/(2 \ln n)$ [21]: negative at every finite $n$, and creeping to
zero at the speed of one over a logarithm.

The right-hand panel of the figure is that claim checked by simulation. Sixty
thousand maxima were drawn at each of eight block sizes from a hundred to three
hundred thousand, and a generalised extreme value distribution fitted to each
set. The fitted shapes run from $-0.095$ to $-0.038$ and track $-1/(2 \ln n)$
throughout. The most unbounded distribution in statistics looks bounded at every
sample size anyone will ever collect. Pushed the other way, the error in the
limiting Gumbel approximation is still 3.1 per cent at a million observations
per block and 2.0 per cent at a trillion; it takes $n$ of order $10^{100}$ to
get it under half a per cent.

So a fitted $\xi$ of $-0.05$ is entirely consistent with a parent distribution
that has no upper bound at all, and the apparent wall is an artefact of the
sample size. It is also entirely consistent with a parent distribution that does
have one. The data cannot distinguish these, and no amount of care with the
fitting procedure will make them distinguishable, because the difference lives
in a region where there are no observations by construction.

There is a second piece of fine print, and 2021 is where it bit. The theorem
assumes the draws are independent and identically distributed. Temperature
extremes under a warming climate are not identically distributed; they are drawn
from a distribution whose location is moving. The Pacific Northwest analysis
handled that in the standard way, letting $\mu$ shift with global mean
temperature while holding $\sigma$ and $\xi$ fixed [1]. That is a reasonable
assumption and it is still an assumption, and Lytton's 49.6 degrees fell outside
the resulting curve's support. The team's own reading was that the event was
made at least 150 times more likely by human-caused warming and that something
about the fitted structure was wrong — either the shape, or the fixed scale, or
the premise that a moving location is enough.

The honest summary of the whole business is this. Extreme value theory is a
genuine and beautiful reduction: it tells you that the shape of catastrophe in
your field is one of three things, and it tells you this without requiring you
to know anything about the mechanism. What it does not do is tell you which of
the three, and that is the only part anyone needs. A dike, a treaty and a
turbine blade are all bets on the sign of $\xi$, placed by people who mostly do
not realise they are betting on the same number, using data that by definition
contains almost no information about it.

## References

1. S. Y. Philip et al., "Rapid attribution analysis of the extraordinary heat
   wave on the Pacific coast of the US and Canada in June 2021," *Earth System
   Dynamics*, vol. 13, pp. 1689-1713, 2022.
2. R. A. Fisher and L. H. C. Tippett, "Limiting Forms of the Frequency
   Distribution of the Largest or Smallest Member of a Sample," *Mathematical
   Proceedings of the Cambridge Philosophical Society*, vol. 24, no. 2,
   pp. 180-190, 1928.
3. B. V. Gnedenko, "Sur la distribution limite du terme maximum d'une série
   aléatoire," *Annals of Mathematics*, vol. 44, no. 3, pp. 423-453, 1943.
4. A. F. Jenkinson, "The Frequency Distribution of the Annual Maximum (or
   Minimum) Values of Meteorological Elements," *Quarterly Journal of the Royal
   Meteorological Society*, vol. 81, no. 348, pp. 158-171, 1955.
5. S. Coles, *An Introduction to Statistical Modeling of Extreme Values*.
   London, UK: Springer, 2001.
6. E. J. Gumbel, *Vier Jahre politischer Mord*, 1922.
7. E. J. Gumbel, *Statistics of Extremes*. New York, NY: Columbia Univ. Press,
   1958.
8. E. J. Gumbel, "The Return Period of Flood Flows," *Annals of Mathematical
   Statistics*, vol. 12, no. 2, pp. 163-190, 1941.
9. P. J. Wemelsfelder, note on the statistical frequency of storm surge levels
   at Hoek van Holland, *De Ingenieur*, 1939 (in Dutch); title not verified from
   a primary record.
10. D. van Dantzig, "Economic Decision Problems for Flood Prevention,"
    *Econometrica*, vol. 24, no. 3, pp. 276-287, 1956.
11. C. Eijgenraam, "Optimal Safety Standards for Dike-Ring Areas," CPB
    Netherlands Bureau for Economic Policy Analysis, The Hague, Discussion
    Paper 62, 2006.
12. L. de Haan, "Fighting the Arch-Enemy with Mathematics," *Statistica
    Neerlandica*, vol. 44, no. 2, pp. 45-68, 1990.
13. W. Weibull, "A Statistical Theory of the Strength of Materials,"
    *Ingeniörsvetenskapsakademiens Handlingar*, no. 151, 1939.
14. W. Weibull, "A Statistical Distribution Function of Wide Applicability,"
    *Journal of Applied Mechanics*, vol. 18, no. 3, pp. 293-297, 1951.
15. J. Pickands III, "Statistical Inference Using Extreme Order Statistics,"
    *Annals of Statistics*, vol. 3, no. 1, pp. 119-131, 1975.
16. A. A. Balkema and L. de Haan, "Residual Life Time at Great Age," *Annals of
    Probability*, vol. 2, no. 5, pp. 792-804, 1974.
17. B. M. Hill, "A Simple General Approach to Inference About the Tail of a
    Distribution," *Annals of Statistics*, vol. 3, no. 5, pp. 1163-1174, 1975.
18. A. J. McNeil, "Estimating the Tails of Loss Severity Distributions Using
    Extreme Value Theory," *ASTIN Bulletin*, vol. 27, no. 1, pp. 117-137, 1997.
19. S. I. Resnick, "Discussion of the Danish Data on Large Fire Insurance
    Losses," *ASTIN Bulletin*, vol. 27, no. 1, pp. 139-151, 1997.
20. P. Embrechts, C. Klüppelberg and T. Mikosch, *Modelling Extremal Events for
    Insurance and Finance*. Berlin, Germany: Springer, 1997.
21. J. P. Cohen, "The Penultimate Form of Approximation to Normal Extremes,"
    *Advances in Applied Probability*, vol. 14, pp. 324-339, 1982.
