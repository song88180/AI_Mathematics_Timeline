import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ACHIEVEMENTS_PATH = ROOT / "achievements.json"
VIBEMATHED_PATH = ROOT / "vibemathed.json"

OVERLAP_BY_SLUG = {
    "erdos-planar-unit-distance": "Unit-distance conjecture",
    "cycle-double-cover-conjecture": "Cycle double cover",
    "jacobian-conjecture": "Jacobian conjecture",
    "sendov-s-conjecture": "Sendov’s conjecture",
    "more-than-67-of-riemann-zeta-zeros-are-on-the-critical-line": "Zeta zeros on the critical line",
    "elliptic-curve-rank-record-thirty-one": "Record elliptic-curve ranks",
    "modular-family-of-2-tori-as-a-complex-structure-on-s6": "Hopf problem on S⁶",
    "tilted-residue-class-construction-for-long-prime-free-intervals": "Erdős–Rankin improvement",
    "prime-gaps-at-most-186": "Short prime gaps",
    "absence-of-critical-bernoulli-bond-percolation-on-z-d-in-every-dimension-d-2": "Dying percolation conjecture",
    "kothe-conjecture": "Köthe conjecture",
    "navier-stokes-millennium-prize-problem-finite-time-breakdown-with-smooth-forcing": "Navier–Stokes regularity",
    "ibragimov-iosifescu-varphi-mixing-clt-conjecture": "Ibragimov–Iosifescu conjecture",
}

# Concise, reader-facing copy. Summaries introduce the mathematical question and
# result rather than recounting the model's process, and stay below 45 words.
CURATED_VIBE = {
    "boussinesq-blowup-smooth-forcing": (
        "Boussinesq blowup with smooth forcing",
        "The inviscid Boussinesq problem asks whether smooth initial data and space-time smooth forcing can produce a finite-time singularity. The reported construction gives such blowup on the plane while the temperature remains bounded.",
    ),
    "euler-blowup-smooth-forcing": (
        "Euler blowup with smooth forcing",
        "The three-dimensional incompressible Euler problem asks whether a smooth flow can lose regularity in finite time. The reported construction produces genuine blowup from smooth data under space-time smooth forcing.",
    ),
    "ibragimov-iosifescu-varphi-mixing-clt-conjecture": (
        "Ibragimov–Iosifescu central limit conjecture",
        "The conjecture predicted a central limit theorem for stationary, φ-mixing sequences with finite variance and diverging partial-sum variance. A counterexample shows that normalized sums can instead converge to zero along a subsequence.",
    ),
    "navier-stokes-millennium-prize-problem-finite-time-breakdown-with-smooth-forcing": (
        "Navier–Stokes breakdown with smooth forcing",
        "The Clay problem asks whether smooth three-dimensional Navier–Stokes data can develop a finite-time singularity. The reported solution uses smooth external forcing, addressing the permitted forced formulations while leaving the unforced case unresolved.",
    ),
    "prime-gaps-at-most-186": (
        "Bounded prime gaps at 186",
        "The bounded-gaps problem asks how close together consecutive primes can occur infinitely often. Subject to three stated analytic and numerical inputs, this result lowers the unconditional upper bound to 186; the twin-prime target remains 2.",
    ),
    "bounded-prime-gaps-at-most-212": (
        "Bounded prime gaps at 212",
        "The bounded-gaps problem asks how close together consecutive primes can occur infinitely often. This result proved that infinitely many consecutive prime pairs differ by at most 212, improving the previous bound of 240.",
    ),
    "absence-of-critical-bernoulli-bond-percolation-on-z-d-in-every-dimension-d-2": (
        "Critical bond percolation in every dimension",
        "For nearest-neighbor bond percolation on the integer lattice, the question asks whether an infinite open cluster exists at the critical probability. The reported result proves that the probability of such a cluster at criticality is zero in every dimension at least two.",
    ),
    "kothe-conjecture": (
        "Köthe’s conjecture",
        "Köthe’s conjecture asks whether the sum of two nil left ideals is always nil. A constructed ring contains a nil ideal whose two-by-two matrix ideal has a nonnilpotent element, disproving the conjecture.",
    ),
    "smale-s-mean-value-conjecture-k-1": (
        "Smale’s mean value conjecture",
        "Smale asked whether the universal constant in his mean value theorem for complex polynomials could be reduced from 4 to 1. A polynomial counterexample shows that the constant 1 is impossible.",
    ),
    "improved-maximal-prime-gap-lower-bound": (
        "Maximal prime-gap lower bound",
        "The maximal prime-gap problem asks how large gaps between consecutive primes can become. This result improves the asymptotic lower bound through a stronger short-translates theorem combined with an Erdős–Rankin covering argument.",
    ),
    "bounded-prime-gaps-at-most-236": (
        "Bounded prime gaps at 236",
        "The bounded-gaps problem asks how close together consecutive primes can occur infinitely often. This announcement established an upper bound of 236, improving 240 before being superseded by stronger results.",
    ),
    "erdos-matching-conjecture-the-four-uniform-case": (
        "Four-uniform Erdős matching conjecture",
        "The Erdős matching conjecture gives the maximum size of a uniform set family with bounded matching number. The reported result settles every parameter in the four-uniform case; higher uniformities remain open.",
    ),
    "erdos-problem-1-sum-distinct-sets": (
        "Erdős problem 1: sum-distinct sets",
        "A set is sum-distinct when all of its subset sums differ. Erdős proposed a universal exponential lower bound on the containing interval; arbitrarily large counterexamples show that no such constant-factor bound exists.",
    ),
    "erdos-problem-571": (
        "Erdős problem 571: bipartite Turán exponents",
        "This problem asks which growth exponents occur as Turán numbers of a single bipartite graph. The result realizes every rational exponent from 1 up to, but not including, 2.",
    ),
    "erdos-problem-548-erdos-sos-conjecture": (
        "Erdős problem 548: Erdős–Sós conjecture",
        "The Erdős–Sós conjecture states that a graph with average degree greater than k − 1 contains every tree with k edges. The reported result establishes the full density statement.",
    ),
    "tilted-residue-class-construction-for-long-prime-free-intervals": (
        "Large prime-gap lower bound",
        "The large-gap problem asks how far apart consecutive primes can be infinitely often. A tilted residue-class construction improves the preceding asymptotic lower bound by an unbounded iterated-logarithm factor.",
    ),
    "nevanlinna-s-half-plane-omitted-values-problem": (
        "Nevanlinna’s half-plane problem",
        "Nevanlinna asked whether a meromorphic function omitting three values in a half-plane must be of bounded type there. A real meromorphic counterexample gives a negative answer for both half-planes.",
    ),
    "modular-family-of-2-tori-as-a-complex-structure-on-s6": (
        "Complex structure on the six-sphere",
        "Hopf’s 1948 problem asks whether the six-sphere admits an integrable complex structure. The manuscript claims an explicit complex threefold diffeomorphic to the six-sphere; the result awaits independent verification.",
    ),
    "elliptic-curve-rank-record-thirty-one": (
        "Elliptic-curve rank 31",
        "Whether elliptic curves over the rationals have unbounded rank remains open. An explicit curve with 31 independent rational points raises the unconditional record to at least 31; exact rank claims require additional conjectural assumptions.",
    ),
    "the-de-bruijn-newman-constant-is-0-1787854": (
        "de Bruijn–Newman constant upper bound",
        "The de Bruijn–Newman constant measures when zeros in a heat-flow deformation of the Riemann xi function become entirely real. Its upper bound is reduced to 0.1787854; the Riemann hypothesis corresponds to a bound of zero.",
    ),
    "elliptic-curve-rank-record-thirty": (
        "Elliptic-curve rank 30",
        "Whether elliptic curves over the rationals have unbounded rank remains open. An explicit curve with 30 independent rational points raised the unconditional record before a rank-31 example superseded it three days later.",
    ),
    "marton-inner-bound-capacity-region": (
        "Marton’s inner-bound conjecture",
        "Marton’s inner bound is the best-known achievable rate region for a general broadcast channel. A finite two-receiver channel shows that its one-letter form does not always equal the full capacity region.",
    ),
    "mathbb-c-infty-caratheodory-conjecture": (
        "Smooth Carathéodory conjecture",
        "Carathéodory asked whether every closed convex surface in three-dimensional space has at least two umbilic points. A smooth convex sphere with exactly one umbilic disproves the smooth case; the real-analytic theorem remains valid.",
    ),
    "matrix-multiplication-exponent-2371177": (
        "Matrix-multiplication exponent",
        "The matrix-multiplication exponent measures the asymptotic cost of multiplying square matrices. Its upper bound is lowered from 2.371339 to 2.371177, while the central question of whether the exponent equals 2 remains open.",
    ),
    "banach-s-isometric-conjecture": (
        "Banach’s isometric conjecture",
        "Banach asked whether a real normed space must be a Hilbert space when all subspaces of a fixed intermediate dimension are mutually isometric. Resolving the remaining odd-dimensional cases completes the conjecture over the reals.",
    ),
    "more-than-67-of-riemann-zeta-zeros-are-on-the-critical-line": (
        "Riemann zeta zeros on the critical line",
        "The Riemann hypothesis places every nontrivial zeta zero on the critical line. This unconditional result raises the known proportion of simple zeros on that line to at least 67.25 percent; it does not prove the hypothesis.",
    ),
    "schiffer-conjecture": (
        "Schiffer’s conjecture",
        "Schiffer’s conjecture asks whether a bounded domain admitting a Neumann eigenfunction constant on its boundary must be a ball. Infinitely many noncircular planar domains provide counterexamples and also resolve the equivalent Pompeiu problem negatively.",
    ),
    "sendov-s-conjecture": (
        "Sendov’s conjecture",
        "Sendov’s conjecture states that every zero of a polynomial whose zeros lie in the unit disk is within distance one of a critical point. The result settles the statement for every polynomial degree.",
    ),
    "non-sofic-groups-exist": (
        "Existence of non-sofic groups",
        "Gromov and Weiss asked whether every group admits approximate finite permutation representations, making every group sofic. An explicit construction answers no by producing a non-sofic group.",
    ),
    "connes-rigidity-conjecture": (
        "Connes’ rigidity conjecture",
        "Connes’ rigidity conjecture asks whether ICC property-(T) groups are determined by their group von Neumann algebras. A counterexample shows that nonisomorphic groups can have isomorphic associated algebras.",
    ),
    "sphere-packing-upper-bounds-cohn-elkies": (
        "High-dimensional sphere-packing bounds",
        "The sphere-packing problem asks how densely equal spheres can fill high-dimensional space. The asymptotic upper bound is improved beyond the long-standing Kabatiansky–Levenshtein bound to the Cohn–Elkies linear-programming threshold.",
    ),
    "kls-quadratic-forms": (
        "KLS conjecture for quadratic forms",
        "The Kannan–Lovász–Simonovits conjecture seeks dimension-free variance bounds for isotropic log-concave distributions. The quadratic-form case is established with constant 2, alongside an improved general bound.",
    ),
    "petersen-coloring-conjecture": (
        "Petersen coloring conjecture",
        "Jaeger conjectured that every bridgeless cubic graph admits a Petersen coloring. An explicit bridgeless cubic counterexample disproves the conjecture, while its consequences such as Berge–Fulkerson remain open.",
    ),
    "jacobian-conjecture": (
        "Jacobian conjecture",
        "The Jacobian conjecture states that every complex polynomial map with constant nonzero Jacobian determinant has a polynomial inverse. A three-variable counterexample disproves the conjecture in dimensions three and above; the plane case remains open.",
    ),
    "cycle-double-cover-conjecture": (
        "Cycle double cover conjecture",
        "The cycle double cover conjecture states that every bridgeless graph has a collection of cycles covering each edge exactly twice. The reported proof establishes this long-standing graph-theory statement.",
    ),
    "white-s-conjecture-on-matroids": (
        "White’s matroid conjecture",
        "White conjectured that symmetric exchange binomials generate every matroid toric ideal. A rank-nine binary matroid supplies a counterexample.",
    ),
    "sum-product-conjecture-reals": (
        "Real sum-product conjecture",
        "The real sum-product conjecture predicted that every finite real set has nearly quadratically many sums or products. Families of algebraic integers with substantially fewer of both provide counterexamples.",
    ),
    "erdos-planar-unit-distance": (
        "Erdős unit-distance conjecture",
        "The unit-distance problem asks how many pairs among a given number of planar points can be exactly one unit apart. The conjectured asymptotic upper bound is disproved by a denser infinite family of configurations.",
    ),
}

CURATED_EXISTING = {
    "Kissing-number bounds": (
        "Kissing-number lower bounds",
        "The kissing-number problem asks how many nonoverlapping unit spheres can touch a central unit sphere. New configurations improve 15 long-standing lower bounds for kissing numbers and related spherical codes.",
    ),
    "Erdős problem survey": (
        "Erdős problem survey",
        "A survey of 700 problems marked open in the Erdős database found five apparently new solutions and eight problems whose earlier solutions had been overlooked.",
    ),
    "Erdős & OEIS proofs": (
        "Erdős and OEIS conjecture proofs",
        "A formal proof-search study resolved 9 of 353 open Erdős problems and proved 44 of 492 conjectures selected from the Online Encyclopedia of Integer Sequences.",
    ),
    "Dinitz–Garg–Goemans": (
        "Dinitz–Garg–Goemans conjecture",
        "The conjecture proposed a cost-preserving way to round divisible multicommodity flows into unsplittable flows under a capacity margin. A network whose best divisible and unsplittable costs differ provides a counterexample.",
    ),
    "Crouzeix’s conjecture": (
        "Crouzeix’s conjecture",
        "Crouzeix’s conjecture states that evaluating a polynomial on a complex matrix increases its norm by at most twice its maximum over the numerical range. The sharp constant 2 is established.",
    ),
    "Ten mathematical advances": (
        "Ten mathematical advances",
        "A single research release presented ten results across mathematics and theoretical computer science, including advances on sofic groups, operator-algebra rigidity, and high-dimensional sphere packing.",
    ),
    "Hadamard matrix constructions": (
        "Hadamard matrices below order 2000",
        "The Hadamard conjecture predicts a plus-or-minus-one matrix of every positive order divisible by four with mutually orthogonal rows. Explicit matrices settle the twelve previously unresolved admissible orders below 2000; the general conjecture remains open.",
    ),
    "OEIS conjecture campaign": (
        "OEIS conjecture campaign",
        "A large-scale study of open conjectures from the Online Encyclopedia of Integer Sequences reported 147 proofs or counterexamples, measuring how automated conjecture solving scales across a broad corpus.",
    ),
    "Kozma–Nitzan follow-up": (
        "Kozma–Nitzan percolation conjectures",
        "The remaining Kozma–Nitzan conjectures concern critical behavior in percolation. A follow-up project reports proofs and formalizations extending the result on the absence of critical infinite clusters.",
    ),
    "Fermat’s Last Theorem formalization": (
        "Fermat’s Last Theorem formalization",
        "Fermat’s Last Theorem states that no three positive integers satisfy aⁿ + bⁿ = cⁿ for n greater than two. Its classical proof has been translated into a computer-checkable formal development.",
    ),
}


def tier_for(significance):
    if significance < 50:
        return "notable"
    if significance <= 60:
        return "major"
    return "landmark"


def source_display_title(problem):
    return (
        (problem.get("shortName") or problem["name"])
        .replace("$\\varphi$", "φ")
        .replace("$\\theta(p_c) = 0$", "θ(p_c) = 0")
        .replace("$S^6$", "S⁶")
    )


def display_status(problem):
    values = filter(None, (problem.get("verification"), problem.get("publication")))
    return " · ".join(value.replace("-", " ").title() for value in values)


def display_ai(problem):
    return " + ".join(
        filter(None, (problem.get("model"), *(problem.get("humanCollaborators") or [])))
    )


def normalize_date(date):
    return f"{date}-01" if re.fullmatch(r"\d{4}-\d{2}", date) else date


def to_achievement(problem):
    significance = problem["significance"]
    curated_title, curated_summary = CURATED_VIBE[problem["slug"]]
    return {
        "date": normalize_date(problem["solveDate"]),
        "title": curated_title,
        "ai": display_ai(problem),
        "tier": tier_for(significance),
        "summary": curated_summary,
        "status": display_status(problem),
        "source": problem["sourceUrl"],
        "vibemathed_significance": significance,
    }


with ACHIEVEMENTS_PATH.open() as file:
    achievements = json.load(file)
with VIBEMATHED_PATH.open() as file:
    problems = json.load(file)["problems"]

# Keep every existing record. Records not represented by VibeMathed retain their
# current editorial fields and receive a null significance value.
merged = [
    {**achievement, "vibemathed_significance": achievement.get("vibemathed_significance")}
    for achievement in achievements
]

for achievement in merged:
    for old_title, (curated_title, curated_summary) in CURATED_EXISTING.items():
        if achievement["title"] in {old_title, curated_title}:
            achievement["title"] = curated_title
            achievement["summary"] = curated_summary
            break

for problem in (
    problem
    for problem in problems
    if isinstance(problem.get("significance"), (int, float))
    and problem["significance"] >= 40
):
    overlap_title = OVERLAP_BY_SLUG.get(problem["slug"])
    incoming = to_achievement(problem)
    matching_titles = {incoming["title"], source_display_title(problem)}
    if overlap_title:
        matching_titles.add(overlap_title)
    overlap_index = next(
        (
            index
            for index, achievement in enumerate(merged)
            if achievement["title"] in matching_titles
        ),
        None,
    )

    if overlap_index is None:
        merged.append(incoming)
    else:
        merged[overlap_index] = incoming

with ACHIEVEMENTS_PATH.open("w") as file:
    json.dump(merged, file, indent=2, ensure_ascii=False)
    file.write("\n")
