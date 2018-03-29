
# Number of statistics

## Genotype patterns

Suppose that we have $n$ haploid genotypes.
Any single-site statistic is expressible as the average across sites
of the *weight* assigned to the genotype pattern at that site,
for some weighting function
$$\begin{aligned}
    w : \{0,1\}^n \to \R .
\end{aligned}$$
The statistic is then
$$\begin{aligned}
    \frac{1}{L} \sum_{i=1}^L w(x_i) ,
\end{aligned}$$
where $x_i$ is the genotype pattern at site $i$.

The set of such statistics is therefore a linear space of dimension $2^n$.
However, since the assignment of alleles to 0 and 1 is arbitrary,
we furthermore want the weighting function to be *symmetric*, 
i.e., $w(x) = w(1-x)$ for all $x \in \{0,1\}^n$.
To furthermore normalize things, we also require $w(0) = w(1) = 0$, i.e.,
to assign zero weight to monomorphic sites.
Then the linear space of such statistics has dimension $2^{n-1}-1$.

Often there is more structure than this, however.

## Allele frequencies: a single population

Now consider statistics of *allele frequencies*.
Suppose to begin that at each site we can compute $p$,
an estimate of the frequency of allele `1` in some location
(e.g., the empirical frequency in some set of samples, possibly weighted).
Denote by $P$ the (random) allele frequency at a randomly chosen site
from the population we are estimating.
With $k$ samples we can directly estimate quantities such as
$$\begin{aligned}
    \E[a_0 + a_1 P + \cdots + a_k P^k],
\end{aligned}$$
i.e., polynomials in $P$ up to order $k$.
However, it is also natural to require such statistics to be symmetric.
To formalize this, we consider statistics of allele frequency of the form
$$\begin{aligned}
    \frac{1}{L} \sum_{i=1}^L f(p_i),    
\end{aligned}$$
where $p_i$ is the allele frequency at site $i$, and
$$\begin{aligned}
    f \in \mathcal{S}_k := \{ f \st \deg(f) = k \;\text{and}\; f(p) = f(1-p) \} ,
\end{aligned}$$
i.e., $f$ is a symmetric polynomial of degree $k$.

How many such statistics are there?
The linear space of polynomials of degree $k$ is of dimension $k+1$, 
but the requirement that $f(p) = f(1-p)$ imposes a constraint.
Any degree-$k$ polynomial can be written in the form
$$\begin{aligned}
    f(p) = \sum_{\ell=0}^k a_\ell p^\ell (1-p)^{k-\ell} .
\end{aligned}$$
(To see this, multiply any term in $f(p)$ that has degree $j < k$ by $(p + (1-p))^{k-j}$.)
The polynomial $f(p)$ satisfies $f(p) = f(1-p)$ if and only if $a_\ell = a_{k-\ell}$
for each $0 \le \ell \le k$.
The space of such polynomials therefore has dimension $\lceil k/2 \rceil$.

How many such are *actually* of dimension $k$?
For instance, the polynomial $p + (1-p)$ is really of degree 0.
Suppose that $f$ and $g$ are each of degree $\ell$; then
$$\begin{aligned}
    (p + (1-p))^{k-\ell} f + (p + (1-p))^{k-\ell} g = (p + (1-p))^{k-\ell} (f+g)
\end{aligned}$$
gives a linear embedding of $\mathcal{S}_\ell$ in $\mathcal{S}_k$.
Since $\dim S_{2k+1} = \dim S_{2k}$, this implies that odd-degree polynomials include *no extra information*
beyond the next-lower even-degree polynomials.
Only odd degrees add a dimension to the space of statistics.
We already know since $p + (1-p) = 1$, that $S_1 = S_0$.
Next, we can write
$$\begin{aligned}
    \mathcal{S}_2 = \{ f(p) = a + b p (1-p) \st a, b \in \R \} .
\end{aligned}$$
Now, $\mathcal{S}_3$ includes everything of the form $a (p^3 + (1-p)^3) + b (p^2 (1-p) + p (1-p)^2)$;
but since $p^3 + (1-p)^3 = 1 - 3 (p^2 (1-p) + p (1-p)^2)$,
and $p^2 (1-p) + p (1-p)^2 = p (1-p)(p + (1-p)) = p(1-p)$,
in fact $\mathcal{S}_3 = \mathcal{S}_2$.
In fact, this implies that anything in $\mathcal{S}_{2k}$,
i.e., any degree-$2k$, symmetric, single-population statistic of allele frequencies 
can be written in terms of an $f(p)$ of the form
$$\begin{aligned}
    f(p) = \sum_{j=0}^k a_j \left(p (1-p)\right)^j ,
\end{aligned}$$
for some coefficients $a_j \in \R$.

Furthermore requiring (as above) that $f(0) = f(1) = 0$ reduces the dimension by 1.

## Allele frequencies: multiple populations

Define provisionally $S_{k_1, \ldots, k_m}$ to be the class of statistics 
that are defined by polynomials $f$ of $m$ allele frequencies,
$$\begin{aligned}
    f(p_1, \ldots, p_m$) = f(1-p_1, \ldots, 1-p_m$) .
\end{aligned}$$
As above, any such function can be written as
$$\begin{aligned}
    f(p_1, \ldots, p_m$) = \sum_{\ell_1=0}^{k_1} \cdots \sum_{\ell_m=0}^{k_m} a_{\ell_1, \ldots,\ell_m} p_1^{\ell_1} (1-p_1)^{k_1-\ell_1} \cdots p_m^{\ell_1} (1-p_m)^{k_1-\ell_1},
\end{aligned}$$
with $a_{\ell_1, \ldots, \ell_m} = a_{k_1-\ell_1, \ldots, k_m-\ell_m}$.
Therefore, $S_{k_1, \ldots, k_m}$ has dimension $\prod_{i=1}^m (k_i + 1)$,
unless all $k_i$ are odd, in which case the dimension is one less
(since only in that case is there a fixed point of the symmetry of the $a$s).


