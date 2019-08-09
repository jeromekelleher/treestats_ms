#!/usr/bin/env python3
import pyslim, tskit, msprime
import numpy as np
import os, sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

usage = """
Usage:
    {} treefile Ne mut_rate window_width
""".format(sys.argv[0])

if len(sys.argv) != 5:
    raise ValueError(usage)

treefile = sys.argv[1]
Ne = int(sys.argv[2])
mut_rate = float(sys.argv[3])
window_width = float(sys.argv[4])

nreps = 20

outbase = ".".join(treefile.split(".")[:-1])
newtrees = outbase + ".recap.trees"

plotfile = "{}.{}.{}.f4.pdf".format(outbase, int(window_width), mut_rate)
sdplotfile = "{}.{}.{}.f4sd.pdf".format(outbase, int(window_width), mut_rate)

try:
    ts = pyslim.load(newtrees)
except:
    ots = pyslim.load(treefile)
    rts = ots.recapitate(1e-8, Ne=Ne)
    ts = rts.simplify()
    ts.dump(newtrees)

windows = np.arange(0, ts.sequence_length+1, window_width)
windows[-1] = ts.sequence_length
x = windows[:-1] + np.diff(windows)/2

########################

pop_names = ['p1', 'p2', 'p3', 'p4']
num_pops = len(pop_names)

# which populations?
f4_pops = [('p1', 'p2', 'p3', 'p4'),
           ('p1', 'p4', 'p2', 'p3')]
f4_indexes = [tuple(pop_names.index(i) for i in a) for a in f4_pops]

stat_names = [f"{a},{b};{c},{d}" for a, b, c, d in f4_pops]
colors = plt.get_cmap("tab20").colors
stat_colors = { k : colors[j] for j, k in enumerate(stat_names) }
styles = ["-", "-.", ":"]
stat_styles = { k : styles[j] for j, k in enumerate(stat_names) }

alive = ts.individuals_alive_at(0)
pop = np.array([ts.node(ts.individual(ind).nodes[0]).population for ind in alive])

pop_nodes = [[] for _ in range(num_pops)]
for i in alive:
    ind = ts.individual(i)
    pop_nodes[pop[ind.id]].extend(ind.nodes)

all_branch = ts.f4(pop_nodes, indexes=f4_indexes, windows=windows, mode='branch')

# independent versions of the same rate, low

low_mut_rate = mut_rate
all_site = np.zeros((len(windows) - 1, len(f4_pops), nreps))
for k in range(nreps):
    mts = msprime.mutate(ts, rate=low_mut_rate, keep=True)
    all_site[:, :, k] = (1/low_mut_rate) * mts.f4(pop_nodes, indexes=f4_indexes, windows=windows, mode='site')

# and independent versions of the same rate, high

high_mut_rate = mut_rate * 10
all_site_high = np.zeros((len(windows) - 1, len(f4_pops), nreps))
for k in range(nreps):
    mts = msprime.mutate(ts, rate=high_mut_rate, keep=True)
    all_site_high[:, :, k] = (1/high_mut_rate) * mts.f4(pop_nodes, indexes=f4_indexes, windows=windows, mode='site')

# and for independent subsamples

mts = msprime.mutate(ts, rate=mut_rate, keep=True)
sample_size = 50
assert(sample_size * nreps <= len(alive))
sub_branch = np.zeros((len(windows) - 1, len(f4_pops), nreps))
sub_site = np.zeros((len(windows) - 1, len(f4_pops), nreps))
for j in range(nreps):
    sample_nodes = []
    for k in range(num_pops):
        inds = alive[pop == k]
        np.random.shuffle(inds)
        si = inds[:sample_size]
        sn = []
        for ind in si:
            sn.extend(ts.individual(ind).nodes)
        sample_nodes.append(sn)
    sub_branch[:, :, j] = ts.f4(sample_nodes, indexes=f4_indexes, windows=windows, mode='branch')
    sub_site[:, :, j] = (1/mut_rate) * mts.f4(sample_nodes, indexes=f4_indexes, windows=windows, mode='site')


maxy = [0.4 * max(np.max(np.abs(all_site[:,0,:])), np.max(np.abs(all_branch[:,0])),
                   np.max(np.abs(sub_site[:,0,:])), np.max(np.abs(sub_branch[:,0,:]))),
        0.4 * max(np.max(np.abs(all_site[:,1,:])), np.max(np.abs(all_branch[:,1])),
                   np.max(np.abs(sub_site[:,1,:])), np.max(np.abs(sub_branch[:,1,:])))]


######## Plot
fig = plt.figure(figsize=(12, 6))

# indep't mutations: low
plot_index = 0
for j, sn in enumerate(stat_names):
    plot_index += 1
    ax = fig.add_subplot(3,2,plot_index)
    ax.set_ylim(-maxy[j], maxy[j])
    sl, = ax.plot(x, all_site[:,j,0],
                 alpha=0.5,
                 color='black',
                 label="site")
    sll = ax.plot(x, all_site[:,j,1:],
                 alpha=0.5,
                 color='black')
    bl, = ax.plot(x, all_branch[:, j],
                 alpha=1.0,
                 color='red',
                 label="branch")
    ax.set_xlabel("chromosome position (bp)")
    if j == 0:
        ax.set_ylabel("mean f4/μ")
    atl = ax.text(ts.sequence_length, maxy[j], "{}\nμ={:.0}".format(sn, low_mut_rate),
                  horizontalalignment='right',
                  verticalalignment='top')
    hl = ax.axhline(np.mean(all_branch[:, j]), color='red', label='mean')
    hl = ax.axhline(np.mean(all_site[:, j, :]), color='black')

leg = ax.legend(
         loc = "upper left",
         bbox_to_anchor = (1.01, 1.01),
         frameon = False,
         borderpad=0)

# indep't mutations: high
for j, sn in enumerate(stat_names):
    plot_index += 1
    ax = fig.add_subplot(3,2,plot_index)
    ax.set_ylim(-maxy[j], maxy[j])
    sl, = ax.plot(x, all_site_high[:,j,0],
                 alpha=0.5,
                 color='black',
                 label="site")
    sll = ax.plot(x, all_site_high[:,j,1:],
                 alpha=0.5,
                 color='black')
    bl, = ax.plot(x, all_branch[:, j],
                 alpha=1.0,
                 color='red',
                 label="branch")
    ax.set_xlabel("chromosome position (bp)")
    if j == 0:
        ax.set_ylabel("mean f4/μ")
    atl = ax.text(ts.sequence_length, maxy[j], "{}\nμ={:.0}".format(sn, high_mut_rate),
                  horizontalalignment='right',
                  verticalalignment='top')
    hl = ax.axhline(np.mean(all_branch[:, j]), color='red', label='mean')
    hl = ax.axhline(np.mean(all_site[:, j, :]), color='black')

leg = ax.legend(
         loc = "upper left",
         bbox_to_anchor = (1.01, 1.01),
         frameon = False,
         borderpad=0)


# independant subsamples
for j, sn in enumerate(stat_names):
    plot_index += 1
    ax = fig.add_subplot(3,2,plot_index)
    ax.set_ylim(-maxy[j], maxy[j])
    sl, = ax.plot(x, sub_site[:,j,0],
                 alpha=0.5,
                 color='black',
                 label="site")
    sll = ax.plot(x, sub_site[:,j,1:],
                 alpha=0.5,
                 color='black')
    bl, = ax.plot(x, sub_branch[:,j,0],
                 alpha=0.5,
                 color='red',
                 label="branch")
    bll = ax.plot(x, sub_branch[:,j,1:],
                 alpha=0.5,
                 color='red')
    ax.set_xlabel("chromosome position (bp)")
    if j == 0:
        ax.set_ylabel("mean f4/μ")
    atl = ax.text(ts.sequence_length, maxy[j], "{}\nμ={:.0}\n n={}".format(sn, mut_rate, sample_size),
                  horizontalalignment='right',
                  verticalalignment='top')
    hl = ax.axhline(np.mean(all_branch[:, j]), color='red', label='mean')
    hl = ax.axhline(np.mean(all_site[:, j, :]), color='black')

leg = ax.legend(
         loc = "upper left",
         bbox_to_anchor = (1.01, 1.01),
         frameon = False,
         borderpad=0)

# done
fig.savefig(plotfile, bbox_inches = "tight")
plt.close(fig)


###########
# plot relationship of mu and sample size to SD

mutrates = np.arange(1, 20) / 1e9
mut_site = np.zeros((len(windows) - 1, len(f4_pops), len(mutrates)))
for k, mr in enumerate(mutrates):
    mts = msprime.mutate(ts, rate=mr, keep=True)
    mut_site[:, :, k] = (1/mr) * mts.f4(pop_nodes, indexes=f4_indexes, windows=windows, mode='site')

mts = msprime.mutate(ts, rate=mut_rate, keep=True)
sample_sizes = [2, 3, 4, 6, 8, 10, 12, 16, 24, 32, 40, 48, 56, 64]
sub_site = np.zeros((len(windows) - 1, len(f4_pops), len(sample_sizes)))
sub_branch = np.zeros((len(windows) - 1, len(f4_pops), len(sample_sizes)))
for j, sample_size in enumerate(sample_sizes):
    sample_nodes = []
    for k in range(num_pops):
        inds = alive[pop == k]
        np.random.shuffle(inds)
        si = inds[:sample_size]
        sn = []
        for ind in si:
            sn.extend(ts.individual(ind).nodes)
        sample_nodes.append(sn)
    sub_branch[:, :, j] = ts.f4(sample_nodes, indexes=f4_indexes, windows=windows, mode='branch')
    sub_site[:, :, j] = (1/mut_rate) * mts.f4(sample_nodes, indexes=f4_indexes, windows=windows, mode='site')


bf4 = ts.f4(pop_nodes, indexes=f4_indexes, mode='branch')
sf4 = ts.f4(pop_nodes, indexes=f4_indexes, mode='site')


fig = plt.figure(figsize=(6, 3))

ax = fig.add_subplot(1,2,1)
ax.set_xlabel("mutation rate (μ)")
ax.set_ylabel("SD(f4/μ)")
ax.plot(mutrates,
           np.std(mut_site[:, 0, :], axis=0),
           color='black',
           label='site')
ax.axhline(np.std(all_branch[:, 0], axis=0),
           color='red',
           label='branch')

leg = ax.legend()


ax = fig.add_subplot(1,2,2)
ax.set_xlabel("sample size")
# ax.set_ylabel("SD(f4/μ)")
ax.plot(sample_sizes,
           np.std(sub_site[:, 0, :], axis=0),
           color='black',
           label='site')
ax.plot(sample_sizes,
           np.std(sub_branch[:, 0, :], axis=0),
           color='red',
           label='branch')

atl = ax.text(sample_sizes[-1], np.max(np.std(sub_site[:, 0, :], axis=0)),
              "{}\nμ={:.0}".format(stat_names[0], mut_rate),
              horizontalalignment='right',
              verticalalignment='top')


# done
fig.savefig(sdplotfile, bbox_inches = "tight")
plt.close(fig)
