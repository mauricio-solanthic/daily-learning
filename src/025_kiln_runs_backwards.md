---
seq: 25
date: 2026-09-21
category: Climate & Sustainability
title: The Kiln Runs Backwards
slug: KilnRunsBackwards
deck: Making cement drives a reaction that the open air spends the next century quietly undoing, at a rate set less by chemistry than by the thickness of a wall.
slack: Producing a tonne of cement clinker releases about 510 kg of carbon dioxide before a gram of fuel is burned, and the open air then spends decades putting a large part of it back — at 20 degrees Celsius the equilibrium carbon dioxide pressure over limestone sits twenty orders of magnitude below the atmosphere's, so every concrete surface on earth is a reaction waiting for a diffusion path. The strange part is who does the absorbing. Mortar is about a quarter of the world's cement use and roughly half of the entire carbonation sink, because the front only advances as the square root of time: a 10 mm bed joint is finished in seven years, a metre-thick raft foundation would need eighteen thousand. Five published accounts now put the cumulative return at 21 to 24 billion tonnes of carbon dioxide, a quantity the Global Carbon Budget carries as a line item and no national inventory does.
burned:
  - Calcination of limestone, 0.785 kg of carbon dioxide per kg of lime, and the IPCC default clinker factor of 0.510
  - Reproducing both IPCC clinker emission factors, 0.5070 and 0.5101, from the 64.6 and 65 per cent lime defaults
  - The clinker energy balance - 2.07 GJ/t of calcination minus the 0.30 GJ/t exotherm of alite formation, reaching a published theoretical floor near 1.75
  - Equilibrium carbon dioxide pressure over calcium carbonate at ambient temperature, and twenty orders of magnitude of atmospheric supersaturation
  - The diffusion-limited carbonation front and its advance as k times the root of elapsed time
  - Deriving the carbonation coefficient from Fick's law, effective diffusivity and lime binding capacity, landing on the measured band
  - Mortar as a quarter of cement use and half of the carbonation sink, and the surface-to-volume explanation
  - The four-geometry comparison - 10 mm bed joint, 20 mm render, 200 mm slab, 1 m raft, at 7, 28, 711 and 17,778 years to full carbonation
  - The five published cumulative sink accounts - Xi 2016, Guo 2021, Huang 2023, Wu 2024, Niu 2025 - spanning 16.5 to 23.9 Gt and 43 to 55 per cent
  - The internal identity 22.9 over 41.6 reproducing a reported 55.1 per cent offset
  - The cement carbonation sink as a Global Carbon Budget line item of 0.2 GtC a year, cross-checked through the carbon-to-carbon-dioxide factor
  - The ceiling argument - full carbonation returns the calcination carbon dioxide mole for mole and never the fuel carbon dioxide
  - Under exponential growth exactly half of cumulative output dates from within the last doubling time, and cement's 2003-2013 doubling
  - Carbonation-induced depassivation, pore solution falling from pH 13 to below 9, and cover as a diffusion delay line
  - Eurocode 2 durability cover of 25 mm for a fifty-year life reproduced by the root-time law at k near 3.75
  - Demolition and crushing as the accelerant, and the sink being largest when the structure is destroyed
  - The accounting asymmetry - calcination counted in every national inventory, carbonation counted in none
  - Openings now used up - the two-hundredth anniversary of the Portland cement patent as a way in
next:
  - Supplementary cementitious materials as a supply-constrained decarbonisation lever, and what happens when blast furnaces close
  - Enhanced rock weathering, the same carbonation chemistry run on basalt, and its measurement problem
  - The cement kiln as a point source for capture, and why concentrated process carbon dioxide is the easiest capture case in industry
---

Two hundred years ago last autumn, a bricklayer in Leeds named Joseph Aspdin
took out a patent on a way of making artificial stone by burning a mixture of
limestone and clay and grinding the result to powder [1]. He called it Portland
cement, after the pale oolitic limestone quarried on the Dorset coast, because
he wanted builders to believe the stuff would set into something like rock. The
name was marketing. The chemistry turned out to be more literal than he could
have known: the powder really does want to become limestone again, and given a
few decades and a supply of ordinary air, a great deal of it does.

That return has recently become large enough to appear in the world's carbon
accounts. The manufacture of cement is responsible for something over seven per
cent of anthropogenic carbon dioxide, and roughly three-fifths of that is not
combustion at all but the chemical decomposition of limestone — an emission no
change of fuel can touch [2]. Set against it, running quietly in every wall,
pavement and rubble pile ever built, is a reverse reaction that the Global
Carbon Budget now carries as a standing line item of about 0.2 billion tonnes of
carbon a year [3]. What follows is an account of how large that return is, why
it takes so long, and why the credit for most of it belongs not to concrete but
to the thin grey layer holding bricks together.

## Two Tonnes of Stone, One of Powder

The reaction at the heart of a cement kiln is the simplest in heavy industry.
Calcium carbonate, heated hard enough, gives up its carbon dioxide and leaves
quicklime behind:

$$ \mathrm{CaCO_3} \longrightarrow \mathrm{CaO} + \mathrm{CO_2}, \qquad \Delta H^{\circ} = +179\ \mathrm{kJ\,mol^{-1}} $$

Everything downstream follows from the molar masses. Calcium carbonate is 56.03
per cent lime and 43.97 per cent carbon dioxide by weight, so every kilogram of
lime costs 0.785 kg of carbon dioxide, released as a matter of stoichiometry
rather than of efficiency. Clinker — the fused nodules that come out of the kiln
and are ground into cement — is about 65 per cent lime, and 0.65 times 0.785
gives 0.510 tonnes of carbon dioxide per tonne of clinker. That is the number
national inventory compilers use [4]. Indeed the two default emission factors in
circulation, 0.5070 and 0.5101, are not competing measurements: they are the
same calculation run on lime contents of 64.6 and 65.0 per cent, and both
reproduce to four decimal places from the molar masses alone. Cement is not
pure clinker — the world average is roughly 72 per cent, the rest being slag,
fly ash and ground limestone [18] — so the process burden per tonne of cement
sold is nearer 0.37 tonnes.

The energy tells a similar story. A tonne of clinker needs 1.16 tonnes of
carbonate decomposed, which is 11,591 moles, which at 179 kJ each is 2.08
gigajoules of pure chemistry. Some of it comes back: the lime then combines with
silica to form alite, the phase that gives cement its strength, and that
combination is exothermic to the tune of about 115 kJ for every mole formed, or
roughly 0.30 GJ per tonne of clinker at ordinary alite contents. Net, the
irreducible heat of making clinker is about 1.77 GJ per tonne, which is where
the published theoretical minimum of roughly 1.75 GJ per tonne comes from [5].
Real kilns burn something closer to 3.5. The gap is heat loss, not chemistry,
and it is the part of the problem that engineering can attack.

## A Reaction the Air Wants to Undo

Calcination is violently unfavourable at room temperature, which is precisely
why it needs a kiln. Run the standard thermodynamic numbers the other way and
the magnitude is startling. With an enthalpy of 179 kJ per mole and an entropy
change of 160.2 J per mole per kelvin, the free energy of decomposition at 20
degrees Celsius is 132 kJ per mole, and the equilibrium partial pressure of
carbon dioxide over calcium carbonate is about 3 times 10 to the minus 24 bar.

The atmosphere currently sits at 422 parts per million, or 4.3 times 10 to the
minus 4 bar. The air outside every building on earth is supersaturated with
respect to limestone by twenty orders of magnitude. Thermodynamically there is
no question whatever about which way the reaction runs; a set of concrete steps
is not in equilibrium with the air around it and never will be until every
available calcium atom has gone back to carbonate.

:::think The obvious question

If the driving force is that overwhelming, why is there any lime left in a
hundred-year-old bridge at all?
:::

Because nothing in this story is limited by thermodynamics. In hardened cement
the calcium sits as portlandite and as calcium silicate hydrate inside a pore
network saturated with alkaline solution, and carbon dioxide has to dissolve
into that solution and diffuse inward before it can react at all. The reaction
itself is fast. The delivery is not — and the delivery is the whole subject.

## Why a Century Is Not Long Enough

Treat the carbonated skin as a diffusion barrier and the mathematics is the same
sharp-front problem that governs oxidation scales and case hardening. Carbon
dioxide diffuses through the already-reacted outer layer at an effective
diffusivity $D_e$, meets unreacted material at depth $x$, and is consumed there.
If the concrete binds $a$ moles of carbon dioxide per cubic metre and the
external concentration is $C_s$, conservation across the advancing front gives

$$ x(t) = \sqrt{\frac{2 D_e C_s}{a}\, t} \;=\; k\sqrt{t} $$

which is the square-root law every durability code is built on [6], [7]. Put
ordinary numbers in it. At 422 parts per million and 20 degrees Celsius the air
holds 0.0175 moles of carbon dioxide per cubic metre. A concrete with 300 kg of
cement per cubic metre at 65 per cent lime binds about 3,480 moles per cubic
metre — roughly two hundred thousand times the concentration in the air feeding
it, which is the real reason the front crawls. With an effective diffusivity of
5 times 10 to the minus 8 square metres per second, typical of carbonated
structural concrete, the coefficient $k$ works out at 4.0 mm per square root of
a year; at one-fifth that diffusivity it is 1.8. Field surveys of in-service
structures report coefficients across very much the same band, from about 2 for
dense concrete in sheltered conditions to 6 and above in cyclically wet exposure
and into the teens for poor material [7]. A first-principles calculation with
two textbook inputs lands where the measurements are.

The consequence is a reaction that never finishes and never stops. Doubling the
depth costs four times the wait. Whatever the front has achieved in ten years
takes a further thirty to double, and the last millimetre of a thick section is
effectively unreachable.

![Four elements made of the same material, carbonating at wildly different rates, and what that does to the global accounts. Left: the fraction of a section converted, under a front advancing as k times the root of elapsed time with k of 3.75 mm per root year. Right: shares of cement use, from the 1928-2024 account, against shares of the carbonation sink, from the 1930-2021 account.](../figures/025-carbonation-front-and-sink.png)

## A Quarter of the Cement, Half of the Carbon

Now put that law next to the shapes cement actually gets used in, and something
counterintuitive falls out. A 10 mm mortar bed joint between two bricks is
carbonated through in seven years. A 20 mm render coat is finished in
twenty-eight. A 200 mm floor slab attacked from both faces would need seven
centuries, and a metre-thick raft foundation nearly eighteen thousand years. The
chemistry is identical in all four. Only the distance differs, and the distance
is squared.

So the global sink is not where the cement is. Concrete takes roughly 73 per
cent of the world's cement and supplies about 30 per cent of the carbonation
sink; mortar and render take roughly 24 per cent and supply between 48 and 59
per cent, depending on which account and which period one takes [8], [9]. Per
tonne of cement, in other words, mortar has absorbed something between three and
a half and six times as much carbon dioxide as concrete — a spread worth
printing in full, because the two leading research groups do not agree on it.
Structural engineering gets the credit for concrete; the carbon sink is largely
the work of plasterers.

The same logic explains the other half of the life cycle. Demolition does not
end the process, it accelerates it: crushing a slab into aggregate multiplies
the exposed surface by orders of magnitude and exposes cores that had been
sealed for decades [10]. A structure's largest single day of carbon uptake is
usually the day it is destroyed.

## Twenty-One Billion Tonnes, and Counting

Five research accounts now exist of how much has come back, and they are close
enough to be credible and far enough apart to be honest about.

| Account | Window | Uptake, Gt CO2 | Share of process emissions |
|---|---|---|---|
| Xi et al. 2016 [11] | 1930-2013 | 16.5 | 43 % |
| Guo et al. 2021 [12] | 1930-2019 | 21.0 | — |
| Huang et al. 2023 [8] | 1930-2021 | 22.9 | 55.1 % |
| Wu et al. 2024 [13] | 1930-2023 | 23.9 | 52.3 % |
| Niu et al. 2025 [9] | 1928-2024 | 21.3 | 46.1 % |

Two of these are worth checking rather than trusting. Xi and colleagues report
their result as 4.5 billion tonnes of carbon, which converts to 16.5 billion
tonnes of carbon dioxide at the ratio of molar masses. Huang and colleagues
report 22.9 billion tonnes absorbed against 41.6 billion emitted and an offset
of 55.1 per cent; the division gives 55.05, so all three of their headline
figures confirm each other. The Global Carbon Budget's sink of 0.2 billion
tonnes of carbon a year is the same quantity in different units as the "over 700
million tonnes of carbon dioxide" quoted elsewhere, since the conversion factor
is 3.664 [3].

The current rate is 0.84 to 0.93 billion tonnes of carbon dioxide a year [9],
[13], against process emissions of roughly 1.6 billion — so the world's standing
stock of cement is now reabsorbing more than half of each year's calcination as
it happens.

The spread between 43 and 55 per cent is not noise to be averaged away. It
reflects genuine disagreement about service lives, demolition rates and how much
of a crushed stockpile ever sees air, and the two most recent accounts — from
overlapping author groups, on nearly the same window — differ by six percentage
points. Anyone quoting a single number for this sink is quoting a modelling
choice.

What can be stated exactly is the ceiling. Carbonation reverses calcination mole
for mole: one molecule of carbon dioxide out of the kiln, one molecule back into
the wall. Complete carbonation of every calcium atom that was ever a carbonate
would therefore return 100 per cent of the process emissions and not one gram of
the fuel emissions, which are roughly two-fifths of the total and are gone for
good. A sink running at half its ceiling after a century is doing well, and can
never do better than three-fifths of the industry's footprint however long one
waits.

There is also a reason the cumulative share understates what is coming. Cement
output doubled from two to four billion tonnes between 2003 and 2013, a
continuously compounded 6.9 per cent a year, and under exponential growth
exactly half of everything ever produced dates from within the last doubling
time. Most of the world's cement is young, and young concrete has carbonated a
centimetre at most. The stock has been chasing a flow that only stopped growing
about a decade ago.

## What the Return Costs

The sink is not free, and the bill is paid by the steel. Fresh concrete protects
reinforcement not by sealing it but by surrounding it with pore water at pH 12
to 13, in which iron holds a passive oxide film a few nanometres thick.
Carbonation consumes exactly the alkalinity that maintains that film. Behind the
front the pore solution falls to about 9 or below, the film destabilises, and
corrosion begins wherever moisture and oxygen are available [14], [15].

This is why reinforced concrete is designed with cover, and cover is nothing but
a deliberately imposed diffusion delay. Eurocode 2 asks for 25 mm of durability
cover in moderate-humidity exposure for a fifty-year design life, plus a
construction tolerance [16]. At a coefficient of 3.75 mm per root year, 25 mm of
cover is reached in 44 years; at 3.0 it is 69 years, and at 6.0 it is 17. The
code's requirement and the square-root law agree closely enough that one can see
the second inside the first.

So the same reaction that quietly draws down carbon dioxide is the principal
non-marine deterioration mechanism in reinforced concrete worldwide, and the
engineering response to it — denser mixes, thicker cover, longer service lives —
is precisely a strategy for slowing the sink down. There is no version of this
trade-off in which one side wins outright. A structure optimised to absorb
carbon dioxide is a structure optimised to rust.

## Counted Going Out, Not Coming In

The asymmetry in the accounting is the last oddity. The calcination emission
appears in every national greenhouse gas inventory in the world, computed with
the factor derived above. The carbonation sink appears in none of them: the 2006
IPCC Guidelines make no provision for it, and the question of whether and how to
include it is still before the relevant expert bodies [17], [18]. It is,
meanwhile, a routine term in the Global Carbon Budget, which means the same
physical flux is inside the number climate scientists use and outside the number
governments report.

It would be a mistake to read any of this as absolution. The sink is slow, it is
capped at the process emissions alone, and it is largest in exactly the
materials — thin renders, mortar beds, crushed demolition waste — that nobody
builds for that reason. It cannot be banked in advance, and building more to
capture more is self-defeating, since a tonne of new cement emits its carbon
dioxide today and reclaims half of it over a century.

The stoichiometry does point somewhere useful, though, and it points backwards
into the kiln rather than forwards into the wall. Alite, the fast-hardening
phase cement is optimised for, is 73.7 per cent lime; belite, its slow sibling,
is 65.1 per cent. Making clinker richer in the second lowers the limestone
demand by about 12 per cent and the irreducible heat by 27 — 1,343 kJ per
kilogram of phase against 1,848 — which is a larger saving than anything
available downstream. The reason the industry has not simply done it is that
belite takes months to develop strength rather than days, and construction
schedules, not chemistry, are what set the composition of clinker.

What it does change is the
arithmetic of what is already standing. The world has poured about 30 billion
tonnes of concrete a year for a decade [19], and every square metre of it is
slowly, silently running the kiln in reverse, at a rate fixed two centuries ago
by a bricklayer's choice of raw material and by the diffusivity of carbon
dioxide through a few millimetres of reacted paste.

## References

1. J. Aspdin, "An Improvement in the Modes of Producing an Artificial Stone,"
   British Patent 5022, 21 October 1824.
2. R. M. Andrew, "Global CO2 emissions from cement production, 1928-2018,"
   *Earth System Science Data*, vol. 11, pp. 1675-1710, 2019.
3. P. Friedlingstein, M. O'Sullivan, M. W. Jones, R. M. Andrew, et al., "Global
   Carbon Budget 2024," *Earth System Science Data*, vol. 17, no. 3,
   pp. 965-1039, 2025.
4. Intergovernmental Panel on Climate Change, "Mineral Industry Emissions," in
   *2006 IPCC Guidelines for National Greenhouse Gas Inventories*, vol. 3,
   ch. 2, Institute for Global Environmental Strategies, 2006.
5. "Assessing minimum energy requirements and emissions for different raw
   material compositions in clinker production," *Environmental Research:
   Infrastructure and Sustainability*, 2025. Author list not established from
   the records consulted.
6. K. Tuutti, *Corrosion of Steel in Concrete*, Report No. 4-82, Swedish Cement
   and Concrete Research Institute, Stockholm, 1982.
7. Federation Internationale du Beton, *Model Code for Service Life Design*,
   fib Bulletin 34, Lausanne, 2006.
8. Z. Huang, J. Wang, L. Bing, Y. Qiu, R. Guo, et al., "Global carbon uptake of
   cement carbonation accounts 1930-2021," *Earth System Science Data*, vol. 15,
   pp. 4947-4958, 2023.
9. L. Niu, S. Wu, R. M. Andrew, Z. Shao, J. Wang, and F. Xi, "Global and
   national CO2 uptake by cement carbonation from 1928 to 2024," *Earth System
   Science Data*, vol. 17, pp. 2231-2247, 2025.
10. "Carbon dioxide uptake in demolished and crushed concrete," Project Report
    395, SINTEF Building and Infrastructure, Oslo, 2006.
11. F. Xi, S. J. Davis, P. Ciais, D. Crawford-Brown, D. Guan, et al.,
    "Substantial global carbon uptake by cement carbonation," *Nature
    Geoscience*, vol. 9, pp. 880-883, 2016.
12. R. Guo, J. Wang, L. Bing, D. Tong, P. Ciais, et al., "Global CO2 uptake by
    cement from 1930 to 2019," *Earth System Science Data*, vol. 13,
    pp. 1791-1805, 2021.
13. S. Wu, Z. Shao, R. M. Andrew, J. Wang, L. Niu, and F. Xi, "Global CO2
    uptake by cement materials accounts 1930-2023," *Scientific Data*, vol. 11,
    art. 1409, 2024.
14. "CO2 uptake in cement-containing products," Report B2309, IVL Swedish
    Environmental Research Institute, Stockholm, 2018.
15. "Concrete Carbonation: Significance and Proper Testing," technical primer,
    Wiss, Janney, Elstner Associates, Northbrook, Illinois.
16. European Committee for Standardization, *Eurocode 2: Design of Concrete
    Structures - Part 1-1: General Rules and Rules for Buildings*,
    EN 1992-1-1, Brussels, 2004.
17. "Note on Cement Carbonation," 19th meeting of the Editorial Board of the
    IPCC Emission Factor Database, Institute for Global Environmental
    Strategies, 2023.
18. World Economic Forum, *Net-Zero Industry Tracker 2023: Cement Industry*,
    Geneva, 2023.
19. "We use 30 billion tonnes of concrete each year - here's how to make it
    sustainable," editorial, *Nature*, 2025.
