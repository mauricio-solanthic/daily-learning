---
seq: 19
date: 2026-09-07
category: Energy
title: The Work Already Done
slug: WorkAlreadyDone
deck: Enrichment is measured in a unit that was never properly published, and the unit explains why the hard part comes first.
slack: Uranium enrichment is priced in a unit Dirac invented in 1941 and never published, and it turns out to be a potential — the separative work to get from natural uranium to bomb metal is 208 SWU per kilogram no matter which route you take, verified here to thirteen decimal places. The consequence is uncomfortable: 78 per cent of that work is already spent by the time you reach the 4.5 per cent assay of ordinary reactor fuel, and 92 per cent by the 19.75 per cent ceiling of the HALEU now being built for advanced reactors. Also here — Paducah's 3,000 megawatts of Tennessee Valley Authority power reconcile to within two per cent of its 11.3-million-SWU rating, and the same electricity through modern centrifuges would deliver eight times the entire world's enrichment capacity.
burned:
  - Uranium enrichment and the separative work unit as the organising idea of a piece
  - Dirac's 1941 unpublished note, the Fuchs-Peierls 1942 classified report, and Cohen's 1951 NNES volume
  - The value function V(x) = (2x-1) ln(x/(1-x)), its zero at one half and its logarithmic divergence at both ends
  - The cascade mass balance F = P(xp-xt)/(xf-xt) and SWU = P V(xp) + T V(xt) - F V(xf)
  - Separative work as a potential - path independence verified to 1.7e-13 across six intermediate assays
  - The 208.03 SWU per kg of 90 per cent HEU from natural feed at 0.25 per cent tails
  - The 78 per cent result - work already spent by 4.5 per cent reactor assay - and 92 per cent by 19.75 per cent HALEU
  - The 37 per cent stripping floor that is paid before the assay has moved at all
  - The ideal-cascade stage count, abundance ratio rising by root alpha per stage
  - Gaseous diffusion alpha = sqrt(352.04/349.03) = 1.0043, and the 1,172-stage reconstruction of the published 1,200
  - Dirac's v-to-the-fourth separative power law and the Tronin/Bogovalov vacuum-core revision to v-squared
  - Gernot Zippe, Sukhumi, and the University of Virginia repeat of 1958-1960
  - Paducah's 3,000 MW of TVA power reconciled against its 11.3 million SWU design rating
  - The 2,400 versus 50 kWh per SWU contrast, and the 1,040-to-1 versus 22-to-1 energy return
  - Megatons to Megawatts - 500 t of HEU, 12,000 t of LEU, 104 million SWU destroyed
  - The optimal tails assay condition r = V(xf) - V(xt) - (xf-xt) V'(xt), symbolically confirmed
  - The optimal tails assay being independent of the product assay
  - The 2021-to-2026 SWU and uranium price tripling that left the price ratio almost unmoved
  - The 0.20-to-0.30 per cent tails swing worth 14,800 tU and 12 million SWU a year at world scale
  - The 2026 fuel cost stack - uranium 50 per cent, enrichment 33 per cent, 1.19 cents per kWh
  - IAEA significant quantities of 25 and 75 kg of contained U-235, and why mass is the wrong metric for the barrier
  - Seventeen AC100 machine-years for one significant quantity, against Centrus's 16-machine cascade
  - The derived 331 SWU per machine per year from the 900 kg HALEU obligation, against the published 340 rating
  - Openings now used up - the unpublished note, and the value-function-plus-cumulative-work panel
next:
  - HVDC transmission and the economics of multi-terminal DC grids
  - Industrial heat electrification and the temperature ladder
  - Transformer and high-voltage cable supply chains as a build-rate constraint
---

Some units have a founding document. The metre has a treaty, the ampere has a
definition adopted by acclamation at a General Conference, and the joule has
Joule. The unit in which the world buys and sells uranium enrichment has a note
that Paul Dirac wrote in 1941 and never properly published.

Dirac had spent the early part of the war on isotope separation, and the idea
that lasted from it was an answer to a question separation engineers could not
otherwise answer: what, exactly, does an enrichment plant produce? Not the mass
of its product, because turning natural uranium into reactor fuel and turning
reactor fuel into bomb metal are wildly different amounts of work for the same
output mass. Not energy, because energy depends on the technology and the whole
point was to compare technologies. Dirac proposed a quantity he called
separative work, and Klaus Fuchs and Rudolf Peierls adopted it in a classified
report the following year [1]. Karl Cohen's 1951 volume in the National Nuclear
Energy Series is the first systematic open treatment [2]. The unit is now
written SWU, pronounced "swoo", and about sixty million of them are sold every
year.

## The Unit Dirac Never Published

Start with the bookkeeping. An enrichment plant takes in feed of mass $F$ at
U-235 weight fraction $x_F$ and splits it into product of mass $P$ at the higher
assay $x_P$ and tails, or waste, of mass $T$ at the lower assay $x_T$. Uranium
is conserved and so is U-235, which gives two equations and hence, for a chosen
product, everything:

$$
F \;=\; P\,\frac{x_P - x_T}{x_F - x_T}, \qquad
T \;=\; P\,\frac{x_P - x_F}{x_F - x_T}.
$$

Natural uranium is 0.711 per cent U-235 by weight; a light-water reactor wants
three to five per cent. For one kilogram of five per cent product with tails
discarded at 0.25 per cent, those equations say the plant must swallow 10.30
kilograms of natural uranium and throw away 9.30 kilograms of nearly-depleted
material. Enrichment is overwhelmingly an exercise in disposal.

Dirac's contribution was to assign to any uranium stream a value depending only
on its assay,

$$
V(x) \;=\; (2x - 1)\,\ln\!\left(\frac{x}{1-x}\right),
$$

and to define the work done by a separation as the value it creates:

$$
\Delta U \;=\; P\,V(x_P) \;+\; T\,V(x_T) \;-\; F\,V(x_F).
$$

One separative work unit is one kilogram of that quantity, which is the first
oddity: because the value function is dimensionless, a SWU has the dimensions of
mass, and plant capacity is quoted in kilograms per year even though nothing
about it is a mass flow.

The left panel of the figure below draws $V$. It vanishes at $x = 1/2$, is
symmetric about that point, and rises logarithmically towards both ends. It is
not a price and not an energy; it measures how far a mixture sits from being
half-and-half, in the units that make separative work additive. A kilogram of
natural uranium scores 4.87 and a kilogram of ninety per cent bomb metal scores
1.76, which sounds absurd until you remember that the function is applied to
masses, and that the masses here are lopsided beyond intuition.

Run the arithmetic for the five per cent kilogram and it comes to 7.92 SWU. The
World Nuclear Association's worked examples give 7.9 SWU for that case, 4.8 SWU
for 3.5 per cent product at the same tails assay, and 4.3 SWU if the tails rise
to 0.30 per cent [3]. The formula reproduces all three to the digit quoted —
7.923, 4.811 and 4.339.

## Additive, and Route-Independent

Suppose you want a kilogram of ninety per cent uranium from natural feed, with a
tails assay of 0.25 per cent. You could run one enormous cascade in a single
pass. Or make 4.95 per cent reactor fuel first and feed that into a second,
smaller cascade. Or stop at 19.75 per cent, or at sixty. Do these cost different
amounts of separative work?

They do not. Provided the intermediate stage returns its tails at the natural
assay — where they are simply recycled as feed to the first stage, which is the
physically honest way to make the comparison — every route requires exactly the
same separative work, the same natural uranium, and leaves the same tails.
Checking six intermediate assays from two per cent to sixty against the
single-pass cascade returns 208.03186 SWU per kilogram every time, agreeing to
1.7 parts in $10^{13}$, which is machine precision rather than approximation.
Separative work is a potential. Only the endpoints matter.

![Left: Dirac's value function on a logarithmic assay axis. It vanishes at a fifty-fifty mixture and diverges at both ends, so the natural-uranium assay of 0.711 per cent scores far higher than ninety per cent bomb metal does. Right: for one kilogram of ninety per cent product drawn from natural feed at 0.25 per cent tails — 208.03 SWU in total — the share of that work already spent by the time the material reaches a given assay. Because the total is route-independent, the split is well defined. Reactor fuel at 4.5 per cent sits at 78 per cent of the way.](../figures/019-separative-work-staircase.png)

That is a pleasant mathematical fact with an unpleasant consequence, which the
right panel draws. Because the work is route-independent, it makes sense to ask
how much of the 208 SWU has been spent by the time the material reaches a given
assay — and almost all of it is spent early.

:::think Of the journey from natural uranium to weapons-grade, which half is the expensive half?
:::

The first, and not by a small margin. By the time the material reaches one per
cent U-235 — a change so slight that no reactor would accept it as fuel — 47 per
cent of the separative work has been done. By 4.5 per cent, the assay of
ordinary light-water reactor fuel, it is 78 per cent. By 19.75 per cent, the
ceiling of the high-assay low-enriched uranium being built for advanced reactor
designs, 92 per cent. By sixty per cent, 98. The last stretch from sixty to
ninety, the one that sounds like the difficult part, is four SWU out of 208.

The reason is the lopsided mass. One kilogram of ninety per cent material takes
194.7 kilograms of natural uranium, but only 21.1 kilograms of 4.95 per cent, or
4.7 kilograms of 19.75 per cent. Separative work scales with the tonnage pushed
through the machines, and the tonnage collapses as the assay rises. The final
cascade in a two-stage route is a small machine handling a trickle; the first is
a factory.

There is even a floor. Push the intermediate assay down towards natural uranium
and the share does not fall to zero but converges to 37 per cent, because
stripping tails to 0.25 per cent out of a very large feed stream is work every
route must pay before the product assay has moved at all.

## Why a Diffusion Plant Needs Twelve Hundred Stages

None of that says anything about how you separate. It is a statement about the
task, deliberately technology-blind, which is exactly what Dirac wanted. The
machines enter through a single number: the separation factor $\alpha$ by which
one pass through one stage multiplies the abundance ratio $x/(1-x)$ of a stream.

For gaseous diffusion, in which uranium hexafluoride is pushed against a porous
barrier and the lighter molecules get through very slightly faster, the ideal
separation factor is the square root of the mass ratio of the two molecules:

$$
\alpha_{\text{ideal}} \;=\; \sqrt{\frac{352.04}{349.03}} \;=\; 1.00430.
$$

Four parts in a thousand. In an ideal cascade, where the streams that meet at
each junction have matching assays and no separative work is wasted on
remixing, the abundance ratio climbs by $\sqrt{\alpha}$ per stage, so the stage
count between two assays is a logarithm divided by a very small number:

$$
N \;=\; \frac{\ln\!\bigl(R_P / R_T\bigr)}{\ln \sqrt{\alpha}}, \qquad R = \frac{x}{1-x}.
$$

| Route | Diffusion, 1.0043 | Centrifuge, 1.3 | Centrifuge, 1.5 |
|---|---|---|---|
| Natural to 3 per cent | 682 | 11 | 7 |
| Full cascade to 3 per cent | 1,172 | 19 | 12 |
| Natural to 4.4 per cent | 868 | 14 | 9 |
| Full cascade to 90 per cent | 3,817 | 62 | 40 |

The second row is the one to check against reality, because the published figure
for a diffusion plant making ordinary three per cent reactor fuel is about 1,200
stages [4]. The formula gives 1,172 once the stripping section is counted — the
stages below the feed point that chase the assay down to the tails specification
— and 682 if only the enriching section is. That the published number matches
the whole cascade rather than the enriching half is a structural fact the
arithmetic hands over for free: two fifths of the stages in a diffusion plant
exist to make the waste more wasteful.

A centrifuge changes $\alpha$ by two orders of magnitude and the stage count
collapses with it, to nineteen. Why is a neat piece of dimensional reasoning. In
a long counter-current centrifuge the separation depends on the pressure
gradient rotation establishes across the radius, which goes as the square of the
peripheral speed, and the separative power on the square of that — so it scales
as the fourth power of rotor speed and only linearly with rotor length [6].
Dirac derived that limit too, which is why a centrifuge programme is really a
materials programme: everything is bought with tip speed, and tip speed is set
by the tensile strength of whatever you can spin without it flying apart.
Aluminium gave way to maraging steel and then to carbon fibre for that reason
and no other. The law is, it turns out, too generous: Tronin and colleagues
showed in 2021 that the derivation ignores the vacuum core that forms around the
axis at high speeds, where no separation happens at all, and that the corrected
limit grows only as the square of the speed [5].

The engineering that made this practical belongs largely to Gernot Zippe, an
Austrian engineer captured at the end of the war and put to work on the Soviet
programme at Sukhumi, where he solved the problem that had defeated everyone
else: supporting a rapidly spinning rotor for years without the bearing
destroying itself, which he did by pairing a needle pivot with a magnetic
bearing. Released in 1956 and intercepted by American intelligence, he spent two
years at the University of Virginia reproducing from memory what he had built in
Georgia, and a version of that machine is the ancestor of nearly every
centrifuge now turning [7]. The modern industry descends from a bearing.

## What Three Thousand Megawatts Bought

The most vivid way to feel the difference between the two technologies is the
electricity bill. Gaseous diffusion consumes roughly 2,400 kilowatt-hours per
SWU; a modern centrifuge plant, about fifty [3].

The Paducah Gaseous Diffusion Plant in Kentucky, which enriched uranium from
1952 to 2013, drew about 3,000 megawatts from the Tennessee Valley Authority —
enough, as the Department of Energy puts it, to power a city the size of
Nashville [8]. Run 3,040 megawatts, the reported peak demand of its four process
buildings, for a year and you get 26.6 terawatt-hours; divide by 2,400
kilowatt-hours per SWU and you get 11.1 million SWU a year. Paducah's design
capacity was 11.3 million. Three numbers from three separate places — a peak
electrical demand, a process energy intensity, and a plant rating — agree to
within two per cent, which is about as good a confirmation as a figure gets
without opening the paper it came from.

Put that same 26.6 terawatt-hours through centrifuges and it would deliver 533
million SWU a year, roughly eight and a half times the entire world's present
enrichment capacity of about 61 million. One obsolete plant's electricity,
redirected through modern machines, would enrich fuel for eight planets.

Run the comparison the other way. A kilogram of 4.5 per cent enriched uranium
taken to 45 gigawatt-days per tonne of burnup at 33 per cent thermal efficiency
yields 356 megawatt-hours of electricity, and enriching it takes 6.87 SWU, or
0.34 megawatt-hours — an energy return on the enrichment step of about 1,040 to
one. Under gaseous diffusion that step cost 16.5 megawatt-hours and the return
was twenty-two to one, still positive but a different industry.

### RUNNING IT BACKWARDS

There is one large historical case of the process in reverse. Under the 1993
Megatons to Megawatts agreement, Russia downblended five hundred tonnes of
weapons-grade uranium from dismantled warheads — the equivalent of some twenty
thousand of them — into low-enriched fuel for American reactors. The programme
ran twenty years, concluded in December 2013, and over its life supplied close
to half of all American nuclear fuel, which is to say roughly ten per cent of
all American electricity [9].

In separative-work terms, blending down is vandalism on a heroic scale. Five
hundred tonnes of ninety per cent material embodies 104 million SWU relative to
natural uranium, or one year and nine months of total world enrichment output at
present capacity, and dilution destroys all of it. Whether it was a good trade
is not a close question. But the unit invented to price the industry also prices
the disarmament, and prices it very high.

## Choosing How Much to Throw Away

The tails assay $x_T$ has been sitting in every formula above as though it were
given. It is not. It is a decision, and the most consequential discretionary
number in the fuel cycle.

Lower tails mean squeezing more U-235 out of each kilogram of feed: less
uranium, more separative work. Higher tails mean the opposite. Since the plant
buys both, the question is a minimisation. Writing $r$ for the price of a
kilogram of feed divided by the price of one SWU, the cost per kilogram of
product comes to $rF + \Delta U$ and setting its derivative in $x_T$ to zero
gives a condition on $r$ alone:

$$
r \;=\; V(x_F) \;-\; V(x_T) \;-\; (x_F - x_T)\,V'(x_T).
$$

Two things about that expression deserve attention. The first is that it is
correct: it is the condition quoted in the trade literature, and differentiating
the cost function symbolically returns it exactly rather than approximately. The
second is what is missing from it. The product assay $x_P$ does not appear, so
the optimal tails assay depends only on the price ratio and the feed assay, and
not at all on what you are making. A plant enriching to 4.5 per cent for a
pressurised water reactor and one enriching to 19.75 per cent for a small
modular reactor should, at the same prices, discard material of identical
quality.

The condition is monotone and steep at the cheap-uranium end. At $r = 0.5$ the
optimal tails assay is 0.302 per cent, at $r = 1$ it is 0.227, at $r = 2$ it is
0.158, and at $r = 3$ it falls to 0.124 — so a plant facing cheap uranium and
dear centrifuges throws away material two and a half times richer than one
facing the reverse.

At the end of August 2026 the long-term price of uranium concentrate was about
96 dollars a pound, conversion about 53 dollars per kilogram of uranium, and
enrichment about 181 dollars per SWU [10]. A pound of triuranium octoxide
contains 0.3846 kilograms of uranium, so delivered feed costs about 303 dollars
per kilogram and $r$ is about 1.67, implying an optimal tails assay of 0.175 per
cent. Real plants run higher, typically 0.20 to 0.30 per cent, because contracts
cap the tails assay a supplier may use without a surcharge and because the naive
optimum ignores the cost of carrying inventory through a cascade with a long
equilibrium time [11].

The interesting part is what has not moved. Spot separative work traded near 56
dollars in 2021 and above 200 in mid-2026, a consequence of the sanctions that
followed February 2022 and of the American prohibition on imported Russian
low-enriched uranium that took effect in August 2024. But uranium tripled too,
from the low thirties to the high eighties a pound. The ratio $r$ went from
about 1.88 to about 1.67 and the optimal tails assay from 0.164 to 0.175 per
cent. A crisis that transformed the industry barely touched its most important
operating parameter, because it moved both prices at once.

The leverage in that parameter is nonetheless large. Against world reactor
requirements of about 68,900 tonnes of uranium in 2025 [12], shifting the whole
industry from 0.20 to 0.30 per cent tails would raise natural uranium demand by
roughly 14,800 tonnes a year, more than a fifth, while freeing about 12 million
SWU — a fifth of world enrichment capacity. Uranium and centrifuges are
substitutes, and the exchange rate between them is a curve any fuel buyer can
differentiate.

## The Cost of Fuel, and the Cost of One Bomb

Assembling the stack at 2026 long-term prices, for one kilogram of 4.5 per cent
fuel at 0.20 per cent tails, gives a bill of about 4,240 dollars.

| Component | Quantity | Cost, dollars | Share |
|---|---|---|---|
| Natural uranium | 8.41 kgU | 2,100 | 50 per cent |
| Conversion | 8.41 kgU | 446 | 11 per cent |
| Enrichment | 7.69 SWU | 1,392 | 33 per cent |
| Fabrication | 1 kg | 300 | 7 per cent |

Spread across the 356 megawatt-hours that kilogram will generate, that is 11.89
dollars per megawatt-hour, or 1.19 cents per kilowatt-hour. At 2021 prices the
same calculation gives 4.51 dollars. Fuel has become two and a half times more
expensive in five years and remains a rounding error against the capital cost of
the plant burning it, which is the durable economic fact about fission.

The last thing the unit is good for is something Dirac was probably not thinking
about. The International Atomic Energy Agency defines a significant quantity as
the approximate amount of material for which the possibility of building an
explosive device cannot be excluded, and sets it at 25 kilograms of contained
U-235 for highly enriched uranium and 75 kilograms for low-enriched [13]. Those
are masses, in a ratio of three to one. But the barrier is separative work, and
on that measure the two are nothing like three to one apart.

Twenty-five kilograms of contained U-235 at ninety per cent assay is 27.8
kilograms of metal, requiring 5,779 SWU from natural feed and about 5.4 tonnes
of concentrate. Taken instead from 4.5 per cent reactor fuel it needs 1,281 SWU,
and 655 kilograms of that fuel — well under the 75-kilogram-of-U-235 threshold
at which the Agency's accounting begins to treat a stock as consequential.
Reasoning in machines rather than tonnes is what the nonproliferation literature
does with this arithmetic [15]: an AC100, rated above 340 SWU a year, would need
seventeen machine-years to make one significant quantity from natural uranium.
The demonstration cascade Centrus operates at Piketon, Ohio, contains sixteen
centrifuges, and its obligation is at least 900 kilograms of 19.75 per cent
HALEU a year [14]. Take that obligation, assume 4.95 per cent feed, and the
implied throughput is 5,300 SWU a year, or 331 SWU per machine — recovering the
published machine rating from a production quota, two numbers never meant to be
compared.

None of this is an argument against enriching uranium, which is how a fifth of
the world's low-carbon electricity gets made. It is an argument for measuring
the right thing. Assay is a percentage and reads like a distance still to be
travelled; mass is intuitive and easy to inspect. Separative work is neither,
and it is the only one of the three that tracks what a cascade actually has to
do. Dirac's unpublished note picked the quantity that mattered, and eighty-five
years later the industry cannot find a better one.

## References

1. J. Bernstein, "SWU for U and Me," arXiv:0906.2505, 2009.
2. K. Cohen, *The Theory of Isotope Separation as Applied to the Large-Scale Production of U235*. New York: McGraw-Hill, 1951.
3. World Nuclear Association, *Uranium Enrichment*, information paper, 2025.
4. US Nuclear Regulatory Commission, *Uranium Enrichment Processes: Gaseous Diffusion*, ML12045A050, 2012.
5. I. V. Tronin *et al.*, "Impact of the Vacuum Core on the Upper Limit of the Separative Power of Gas Centrifuges," *Annals of Nuclear Energy*, vol. 153, art. 108029, 2021.
6. S. Whitley, "Review of the Gas Centrifuge until 1962. Part I," *Reviews of Modern Physics*, vol. 56, pp. 41-66, 1984.
7. R. S. Kemp, "Gas Centrifuge Theory and Development: A Review of U.S. Programs," *Science & Global Security*, vol. 17, pp. 1-19, 2009.
8. US Department of Energy, *Paducah Site Background*, agency page, 2025.
9. US Energy Information Administration, "Megatons to Megawatts Program Will Conclude at the End of 2013," 2013.
10. UxC LLC, *Nuclear Fuel Price Indicators*, monthly series, August 2026.
11. T. L. Neff, "Enrichment Tails Assays and Uranium Supply: A Dynamic Relationship," *The Ux Weekly*, vol. 19, no. 41, 2005.
12. World Nuclear Association, *World Nuclear Fuel Report*, 2025.
13. International Atomic Energy Agency, *IAEA Safeguards Glossary*, 2022 ed. Vienna: IAEA, 2022.
14. US Department of Energy, "Centrus Reaches 900 Kilogram Mark for HALEU Production," 2025.
15. A. Glaser, "Characteristics of the Gas Centrifuge for Uranium Enrichment and Their Relevance for Nuclear Weapon Proliferation," *Science & Global Security*, vol. 16, pp. 1-25, 2008.
