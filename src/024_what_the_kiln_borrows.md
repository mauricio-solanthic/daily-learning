---
seq: 24
date: 2026-09-15
category: Climate & Sustainability
title: What the Kiln Borrows
slug: WhatTheKilnBorrows
deck: Cement's largest emission is not burned into existence but broken out of a rock, and the rock spends the next century quietly trying to reassemble itself.
slack: Roughly half of cement's carbon dioxide never came from fuel at all — it was chemically locked inside limestone and prised out at 1,450 degrees, which is why a zero-carbon kiln still emits 0.507 tonnes per tonne of clinker. The strange part is that the reaction runs backwards on its own: at ordinary temperatures carbonation is downhill by 111 kJ/mol, and published accounts credit set concrete and mortar with having quietly reabsorbed between 16.5 and 23.9 billion tonnes since 1930, an offset somewhere between 43 and 55 per cent of all cement process emissions ever made. Britain became the first country to put that sink in its UN inventory this year, at 1.48 Mt for 2024 — and the same reaction that takes the carbon back is the one that strips the alkalinity protecting steel reinforcement, so the repayment arrives as rust.
burned:
  - Calcination stoichiometry - CaCO3 to CaO plus CO2, 0.4397 t CO2 per t CaCO3 and 0.7848 per t CaO
  - The IPCC 64.6 per cent lime default reproducing the 0.507 t CO2 per t clinker emission factor exactly
  - Recovering the global clinker-to-cement ratio of about 0.72 from published cement output and process emissions
  - Joseph Aspdin's 1824 patent 5022 and its phrase "until the carbonic acid is entirely expelled"
  - The 2.05 GJ/t calcination heat against the 1.75 GJ/t net theoretical heat of clinker formation, and the clinkering exotherm
  - Van 't Hoff on CaCO3 - 1 bar equilibrium at dH/dS, and 517 C at 420 ppm ambient partial pressure
  - Carbonation favoured by 111 kJ/mol at 298 K and 420 ppm - the kiln borrows rather than destroys
  - The carbonation front as x equals k root t, and Sagues's 18-bridge Florida survey with median k of 1.4 mm per root-year
  - The 2 k root t over d section-fraction rule, and the 10 mm render against the 300 mm column
  - Four published uptake accounts disagreeing - Xi 2016, Guo 2021, Wu 2024, Niu 2025
  - Guo's 21.02 Gt to 2019 against Niu's 21.26 Gt to 2023, four years apart and 3 Gt of uptake missing
  - The Global Carbon Budget's 10.1 versus 10.3 GtC with and without the cement carbonation sink
  - Tuutti's 1982 initiation-and-propagation split, and 13.7 years to initiation with 30 years to cracking
  - Portlandite at about 20 per cent of hardened paste, pH 12.5 falling below 9, and passive-film loss
  - The UK's 2026 National Inventory Document entry - 1.48 Mt against 5.1 Mt process emissions and 371 Mt territorial
  - The rebate-not-credit framing - cutting the clinker factor cuts the future sink in the same stroke
next:
  - Nitrous oxide, the stratosphere, and the one greenhouse gas with no substitute in agriculture
  - Sea-level commitment - thermosteric expansion, ice-sheet lag, and what is already owed
  - Carbon border adjustment mechanisms and the measurement problem underneath them
---

## The Carbonic Acid Entirely Expelled

Joseph Aspdin, a bricklayer from Leeds, was granted British patent 5022 on the
twenty-first of October 1824 for what he called an improvement in the mode of
producing an artificial stone [1]. The recipe was limestone and clay, broken into
lumps and burned in something like a lime kiln. The instruction that matters is
the one Aspdin gave for knowing when the burning was done: continue, he wrote,
until the carbonic acid is entirely expelled.

Carbonic acid was the chemistry of the day's name for carbon dioxide. Two
centuries before anyone thought of it as an emission, the defining step of making
cement was described in a patent as the deliberate and complete expulsion of
carbon dioxide from a rock. It is still the defining step, and it is the reason
cement occupies such an awkward position in the decarbonisation of industry.
Roughly seven to eight per cent of global carbon dioxide emissions come from
cement [2], [3], and the larger share of that is not combustion at all.

The reaction is calcination:

$$
\mathrm{CaCO_3} \longrightarrow \mathrm{CaO} + \mathrm{CO_2}
$$

Everything about cement's carbon problem follows from the three molar masses
involved. Calcium carbonate is 100.086 grams per mole, quicklime 56.077, carbon
dioxide 44.009. The last two sum exactly to the first, because nothing is created
or lost — the kiln simply splits the rock. Every tonne of limestone decomposed
releases 0.4397 tonnes of carbon dioxide; every tonne of quicklime produced
carries 0.7848 tonnes of released gas behind it.

Clinker, the nodular intermediate ground up to make cement, is roughly
two-thirds lime by mass. The IPCC's inventory guidelines take the lime fraction as
64.6 per cent and assume all of it came from carbonate rock, which fixes the
default emission factor at $0.646 \times 0.7848 = 0.507$ tonnes of carbon dioxide
per tonne of clinker [4]. That number is not an engineering estimate of a
particular kiln. It is arithmetic on atomic masses, and no improvement in
combustion, no alternative fuel, no electrified kiln touches it.

The scale follows in one more step. Global cement output is now around four
billion tonnes a year [5], and the world's clinker-to-cement ratio can be
recovered rather than looked up: dividing the reported process emissions of about
1.5 gigatonnes by four billion tonnes of cement at 0.507 gives an implied ratio
near 0.74, and at 4.2 billion tonnes, 0.70. The industry's own reported figure
sits inside that bracket, which is a useful check that three independently
published numbers are telling the same story. The ratio has been falling — Andrew
puts the global average at 0.83 in 1990 and 0.67 by 2013 [3] — and every point of
decline is clinker not made and carbon not released.

## A Debt, Not a Destruction

Heat is what holds the reaction open. Calcination is endothermic by about 178
kilojoules per mole, and a tonne of clinker contains roughly 11,520 moles of lime,
so simply breaking the carbonate absorbs 2.05 gigajoules per tonne. The accepted
theoretical minimum for making clinker is lower, near 1.75 gigajoules per tonne
[6], and the gap is real chemistry rather than rounding: once the lime is free, it
combines with silica and alumina to form the calcium silicates that give cement
its strength, and those reactions give heat back. The kiln pays about 2.05 and is
refunded about 0.30.

:::think Where does the reaction want to go?
A kiln runs at 1,450 degrees Celsius to drive carbon dioxide out of limestone.
At the temperature of a building site, with the atmosphere at 420 parts per
million of carbon dioxide, which direction does that same reaction favour — and
by how much?
:::

Treat the decomposition with a van 't Hoff argument. Equilibrium sits where the
free-energy change vanishes, so with an enthalpy of 177.8 kilojoules per mole and
an entropy of 160.5 joules per mole per kelvin, the temperature at which carbon
dioxide reaches one bar over the rock is their ratio, 1,108 kelvin, or about 835
degrees Celsius. The measured value is 898 degrees, and the discrepancy is
honest: those are room-temperature values for quantities that drift with
temperature. The shape of the answer survives the imprecision, and the shape is
what matters when the pressure is not one bar but the 420 parts per million of
the open air. Putting that partial pressure into the same expression moves
equilibrium down to about 517 degrees Celsius.

Below that temperature, limestone is the stable phase and quicklime is not. At
298 kelvin the decomposition has a free-energy change of about $+111$ kilojoules
per mole against the real atmosphere, which is to say that carbonation — the
reverse reaction, in which set cement takes carbon dioxide back out of the air —
is downhill by that same enormous margin. Nothing in the kiln destroys the
carbonate bond permanently. The kiln borrows against it, at a temperature where
the loan is possible, and hands the product to a world where the repayment is
thermodynamically inevitable and only kinetically slow.

In hardened cement the repayment happens through the alkaline hydration products.
Portlandite, calcium hydroxide, makes up roughly a fifth of hardened paste by
mass, and it reacts with dissolved carbon dioxide to regenerate calcium
carbonate; when it is exhausted, the calcium silicate hydrate gel that provides
the material's strength is attacked in turn, leaving calcium carbonate and silica
gel. Mole for mole, every unit of lime that left the kiln as carbon dioxide can
take a unit back.

## The Front That Moves Like a Square Root

What stops the reaction from running to completion in a season is transport.
Carbon dioxide must diffuse through the pore network of already-carbonated
material to reach fresh alkalinity, and the reacted layer it has to cross grows
as the front advances. That is the classic structure of a diffusion-limited
moving boundary, and it yields the law Tuutti made the foundation of concrete
durability modelling in 1982 [7]:

$$
x(t) = k\sqrt{t}
$$

Depth goes as the square root of time, with $k$ in millimetres per root-year
carrying everything else — mix design, water-to-cement ratio, curing, humidity,
exposure. Sagüés and colleagues measured it directly on eighteen Florida bridges
built between 1939 and 1981 and found $k$ spanning zero to 14 millimetres per
root-year, with a median of 1.4 and the highest values on inland bridge decks
[8]. The square root is unforgiving in both directions: doubling the depth
reached costs four times the wait. In years for the front to arrive:

| $k$ (mm yr$^{-1/2}$) | 25 mm cover | 30 mm cover | 50 mm cover |
|---|---|---|---|
| 1.4 | 319 | 459 | 1,276 |
| 3.0 | 69 | 100 | 278 |
| 5.0 | 25 | 36 | 100 |
| 8.0 | 10 | 14 | 39 |

![The same one-parameter law, read two ways. Left: carbonation depth against time for four values of the rate coefficient, with the Eurocode nominal cover band shaded. Right: the carbonated share of a member of thickness d exposed on both faces, which is 2k√t/d until it saturates — a thin render is finished in under three years while a column has managed a seventh of its section in fifty.](../figures/024-carbonation-front.png)

The same law explains where the world's carbonation actually happens. For a member
of thickness $d$ attacked from both faces, the carbonated share of the section is
$2k\sqrt{t}/d$ until it saturates. At a middling $k$ of 3, a ten-millimetre mortar
render is completely carbonated in 2.8 years. A 150-millimetre slab reaches 28 per
cent in fifty years. A 300-millimetre column manages 14 per cent — one seventh of
its cement, after half a century of standing in the weather.

Structural concrete, in other words, is a poor absorber, and thin material is an
excellent one. Renders, screeds, mortar beds and above all the rubble left when a
building is demolished and crushed — where a cubic metre of intact concrete
becomes square metres of new surface — are where the reaction gets its
opportunity. The accounting papers that estimate the global sink all partition
cement use into concrete, mortar, kiln dust and construction waste for exactly
this reason [9], [10].

## Four Accounts of the Same Sink

The size of that sink has been estimated four times in a decade, by overlapping
groups, using similar models and different data. The results do not agree.

| Account | Period | Uptake (Gt CO₂) | Offset |
|---|---|---|---|
| Xi et al., 2016 [9] | 1930–2013 | 16.5 | 43% |
| Guo et al., 2021 [10] | 1930–2019 | 21.0 | 55% |
| Wu et al., 2024 [11] | 1930–2023 | 23.9 | 52% |
| Niu et al., 2025 [12] | 1928–2023 | 21.3 | 46% |

Xi and colleagues reported 4.5 gigatonnes of carbon, which is 16.5 gigatonnes of
carbon dioxide, absorbed between 1930 and 2013 [9]. The disagreement is sharpest
between the two most recent: Guo's account reaches 21.02 gigatonnes by 2019, and
Niu's reaches 21.26 by 2023 — a quarter of a gigatonne apart across four years in
which annual uptake alone should have added something like 3.2. Two careful teams,
both including several of the same authors, differ by roughly the entire uptake of
the interval between their endpoints.

The present-day flow shows the same spread. The Global Carbon Budget, which
carries the sink as the average of two published series, puts 2023 fossil
emissions at 10.1 gigatonnes of carbon with the cement sink included and 10.3
without [13] — a difference of 0.2 gigatonnes of carbon, or 0.73 gigatonnes of
carbon dioxide. Wu's account gives 0.93 for the same year [11]; Niu's gives 0.84
[12]. Highest to lowest is a 27 per cent disagreement about a flux comparable to
the annual emissions of Germany.

None of this makes the sink doubtful. Every account agrees it is large, that it
has been running since the first Portland cement was set, and that its magnitude
is somewhere between two-fifths and rather more than half of all cement process
emissions ever made. What the spread reveals is how much of the estimate depends
on assumptions no one can measure globally: how thick the world's concrete is, how
much of it has been demolished, how finely the rubble was crushed, and what
happened to it afterwards.

## What the Repayment Costs

There is a reason the construction industry spent a century treating this reaction
as a defect rather than a service. Fresh concrete's pore solution sits near pH
12.5 to 13, held there by portlandite, and at that alkalinity steel carries a
passive oxide film that makes it effectively immune to corrosion. Carbonation
consumes precisely the compound responsible. As the front passes, pH falls below
9, the film is no longer thermodynamically stable, and reinforcement that was
protected becomes ordinary steel in damp salty concrete.

Tuutti's framework splits the resulting service life into two phases: an
initiation period during which the front travels through the cover and nothing
visible happens, and a propagation period during which the steel corrodes, the
rust expands, and the cover cracks and spalls [7]. A Spanish survey of
twenty-five reinforced concrete buildings put average initiation at about 13.7
years and a further 30 years from initiation to cracking [14]. That is why
Eurocode 2 specifies cover by exposure class and design life rather than by
strength alone: for the carbonation classes at a fifty-year design life, minimum
durability cover runs from 25 to 50 millimetres, with a further construction
tolerance on top [15]. Read the carbonation-depth table as a design chart and the
logic is plain — thirty millimetres of cover buys a century at $k = 3$ and
fourteen years at $k = 8$.

The conflict is not hypothetical, and it has sharpened as the sink has become
attractive. A 2026 study of steel in early-age carbonated calcium
sulfoaluminate-Portland mortar found that deliberately forcing carbon dioxide into
fresh material accelerated corrosion sharply — mean corrosion cluster volume
doubling after four hours of treatment — and named the problem outright as the
carbon sinking–corrosion dilemma [16]. Every route to making the sink faster is a
route to reaching the reinforcement sooner.

Two things keep the dilemma from being a crisis. The first is that the reaction
is genuinely slow in good concrete: Sagüés projected 266 years to corrosion
initiation for the worst decile of rate coefficients combined with the worst decile
of cover in the Florida inventory, and concluded that only a small fraction of
those bridges would show carbonation-induced corrosion within a 75-year life [8].
The second is that the fastest absorption happens in material with no steel in it
at all — renders, mortars, crushed demolition waste. The sink and the risk are
largely in different places, which is luck rather than design.

## Counting a Reaction Nobody Owns

For all its size, the sink has been institutionally invisible. The 2006 IPCC
inventory guidelines [4] and their 2019 refinement have no line for it, so national
greenhouse gas accounts have counted cement's process emission in full on the day
the kiln ran and counted nothing at all in the decades afterwards. It is due to be
addressed in a forthcoming IPCC methodology report on carbon dioxide removal
expected in 2027.

Britain moved first. In its 2026 National Inventory Document the United Kingdom
became the first country to report a country-specific estimate of concrete
carbonation, putting the 2024 sink at 1.48 million tonnes of carbon dioxide — 29
per cent of the roughly 5.1 million tonnes of process emissions attributable to
cement used in the UK, and around 0.4 per cent of territorial greenhouse gas
emissions [17]. Those three figures check against each other and against an
outside source: 1.48 over 5.1 is 29.0 per cent, and a sink that is 0.4 per cent of
the national total implies a national total of 370 million tonnes, against the
371 million reported for 2024 [18].

A hard question sits underneath the accounting. The sink is a rebate, not a
credit. Carbonation can only ever take back carbon that calcination released, and
only from clinker that was actually made — so the ceiling on the sink is one
hundred per cent of process emissions and not a molecule more. Against the 38.3
gigatonnes of carbon dioxide that cement production released between 1928 and 2018
[3], the 16.5 to 23.9 gigatonnes recovered to date is repayment on a debt, arriving
decades late and by no means in full.

That makes the sink a poor foundation for a net-zero strategy, and a worse one the
better the strategy works. Clinker substitution, the most reliable decarbonisation
lever the industry has, cuts the emission and the future sink in the same stroke:
lime that is never calcined cannot carbonate. A world that halves its clinker
factor halves the reaction running in its walls a generation later. Only
capture and storage breaks the symmetry, by keeping carbon that the rock has
already given up from ever reaching the air.

Aspdin's instruction was to burn until the carbonic acid was entirely expelled. He
did not mention that the stone would spend the next two centuries trying to take
it back, because he had no reason to care. The reaction was always reversible; what
changed is that we now have an interest in which direction it runs, and a
great deal of concrete standing around quietly running it.

## References

1. J. Aspdin, "An Improvement in the Mode of Producing an Artificial Stone,"
   British Patent 5022, Oct. 21, 1824.
2. "We use 30 billion tonnes of concrete each year — here's how to make it
   sustainable," *Nature*, vol. 639, 2025.
3. R. M. Andrew, "Global CO2 emissions from cement production, 1928-2018,"
   *Earth System Science Data*, vol. 11, no. 4, pp. 1675-1710, 2019.
4. Intergovernmental Panel on Climate Change, *2006 IPCC Guidelines for National
   Greenhouse Gas Inventories*, Vol. 3, Ch. 2: Mineral Industry Emissions.
   Hayama, Japan: IGES, 2006.
5. U.S. Geological Survey, *Mineral Commodity Summaries 2025: Cement.* Reston,
   VA: USGS, 2025.
6. International Energy Agency and World Business Council for Sustainable
   Development, *Technology Roadmap: Low-Carbon Transition in the Cement
   Industry.* Paris, France: IEA, 2018.
7. K. Tuutti, *Corrosion of Steel in Concrete*, CBI Research Report 4:82.
   Stockholm, Sweden: Swedish Cement and Concrete Research Institute, 1982.
8. A. A. Sagüés, S. C. Kranc, F. Presuel-Moreno, et al., *Carbonation in Concrete
   and Effect on Steel Corrosion*, Report BA-502. Tallahassee, FL: Florida
   Department of Transportation, 1997.
9. F. Xi, S. J. Davis, P. Ciais, et al., "Substantial global carbon uptake by
   cement carbonation," *Nature Geoscience*, vol. 9, no. 12, pp. 880-883, 2016.
10. R. Guo, J. Wang, L. Bing, et al., "Global CO2 uptake by cement from 1930 to
    2019," *Earth System Science Data*, vol. 13, no. 4, pp. 1791-1805, 2021.
11. S. Wu, Z. Shao, R. M. Andrew, et al., "Global CO2 uptake by cement materials
    accounts 1930-2023," *Scientific Data*, vol. 11, art. 1409, 2024.
12. L. Niu, S. Wu, R. M. Andrew, Z. Shao, J. Wang, and F. Xi, "Global and national
    CO2 uptake by cement carbonation from 1928 to 2024," *Earth System Science
    Data*, vol. 17, pp. 2231-2247, 2025.
13. P. Friedlingstein, M. O'Sullivan, M. W. Jones, et al., "Global Carbon Budget
    2024," *Earth System Science Data*, vol. 17, no. 3, pp. 965-1039, 2025.
14. J. Sánchez Montero, P. Saura Gómez, J. E. Torres Martín, S. Chinchón-Payá,
    and N. Rebolledo Ramos, "Variation of Corrosion Rate, Vcorr, during the
    Carbonation-Induced Corrosion Propagation Period in Reinforced Concrete
    Elements," *Materials*, vol. 17, no. 1, art. 101, 2024.
15. European Committee for Standardization, *EN 1992-1-1, Eurocode 2: Design of
    Concrete Structures — Part 1-1: General Rules and Rules for Buildings.*
    Brussels, Belgium: CEN, 2004.
16. Q. Zeng, Y. Lan, Y. Qiu, et al., "The carbon sinking-corrosion dilemma in
    concrete: insights from early-age CSA-PC mortar," *npj Materials
    Degradation*, 2026.
17. Mineral Products Association, "UK includes concrete carbonation in national
    climate inventory for first time," London, UK, 2026.
18. Department for Energy Security and Net Zero, *2024 UK Greenhouse Gas
    Emissions, Provisional Figures.* London, UK, 2025.
