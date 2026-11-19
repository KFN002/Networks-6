# Workshop 05 — Adding Realism to Mininet Topologies

**Course:** LZSCC.231-1-2026 | **Source:** `task.html` (Moodle: *Workshop 05 Tasks*)
**Environment:** `scc_231/mininet` devcontainer (image `reg.lzscc.de/papacchi/lzscc231:2026.10.20-fix`), privileged, root user.

This document explains how to complete the lab and what the completed solution in `solutions/` contains.

---

## 1. What this lab is about

Week 4 introduced Mininet with a basic topology. Real networks are more complex: they involve multiple switches, routers and hosts, and real-world conditions such as limited bandwidth, latency and packet loss.

In this workshop you will:

1. **Part 1 — Add network realism** to a topology: bandwidth (`bw`), delay and loss on links.
2. **Part 2 — Configure static routing** so that every host can reach every other host, with all IP configuration embedded in `topology.py` via the Mininet API (no manual CLI commands after startup).

By the end you will be able to design advanced topologies, configure static routing in Mininet, and simulate realistic network conditions.

**Learning objectives**
- Design advanced network topologies using Mininet.
- Configure static routing in Mininet.
- Simulate realistic network conditions using Mininet.

---

## 2. Prerequisites / Getting started

1. Load and use the devcontainer environment (`scc_231/mininet`).
2. On a terminal on your lab machine, allow GUI apps from the container to display on the host:
   ```bash
   xhost +
   ```
3. Open the workspace folder (`/workspace`) in VS Code. The template code is:
   - `topology.py` — Mininet topology definition (the file you edit).
   - `Makefile` — convenience targets to start/stop the emulator.

   ```bash
   # start the topology
   make topo        # mn --custom topology.py --topo tutorialTopology --controller none --mac --switch lxbr --link tc
   # stop / clean everything
   make clean       # mn -c
   ```

> **Note:** `make topo` uses `--switch lxbr` (a Linux learning bridge), so the switches forward traffic without needing an OpenFlow controller. Do not change this unless you also start a controller.

---

## 3. The provided topology

`topology.py` defines `TutorialTopology` with 4 hosts and 2 switches:

| Link | Parameters |
|------|------------|
| h1 — s1 | bw=100, delay=30ms, loss=1 |
| s1 — h2 | bw=10, delay=10ms, loss=1 |
| h2 — h3 | (plain, direct router link) |
| h4 — s2 | bw=100, delay=100ms |
| s2 — h3 | bw=100, delay=100ms |

**Part 1** (link realism) is already present in the template `topology.py`.

**Part 2** is the part to complete: the topology currently has no IP addressing and no static routes, so only the directly-connected pairs `h1↔h2` and `h3↔h4` can communicate. You must embed full IP configuration in `topology.py` so all hosts are reachable.

There are three Layer-3 regions:

| Region | Network | Interfaces |
|--------|---------|------------|
| 1 | `10.0.0.0/24` | h1-eth0, h2-eth0 |
| 2 | `192.168.0.0/24` | h2-eth1, h3-eth0 |
| 3 | `10.1.0.0/24` | h3-eth1, h4-eth0 |

Hosts `h2` and `h3` must act as routers (IP forwarding on) so traffic can cross regions.

---

## 6. Files in this workspace

| File | Purpose |
|------|---------|
| `topology.py` | Template topology (Part 1 done; Part 2 to be completed by you). |
| `Makefile` | `make topo` / `make clean` convenience targets. |
| `task.html` | Original Moodle task page (reference). |
| `task_files/` | Assets referenced by `task.html` (figures, CSS, JS). |
| `INSTRUCTIONS.md` | These instructions. |
| `solutions/` | Completed solution (see below). |

---

## 7. The completed solution (`solutions/`)

`solutions/topology.py` is a finished `TutorialTopology` that embeds **both** Part 1 (link realism) and Part 2 (IP addressing + static routing) entirely in the Mininet API. Copy it over `topology.py` to submit/use it:

```bash
cp solutions/topology.py topology.py
make clean && make topo
mininet> pingall      # 0% packet loss
```

The solution was validated by starting Mininet with it and confirming:
- `pingall`: **0% packet loss (12/12 received)**
- `h1 ping -c 3 10.1.0.2` → **3/3 received, 0% loss**
- `h4 ping -c 3 10.0.0.1` → **3/3 received, 0% loss**
- IP forwarding enabled on `h2` and `h3`
- All interfaces carry the expected IPs; all static routes present

`solutions/test_solution.py` is a non-interactive verification script you can run with:
```bash
python3 solutions/test_solution.py
```

`solutions/Makefile` is a copy of the project `Makefile` for convenience.

---

## 8. Troubleshooting

| Problem | Likely cause / fix |
|---------|--------------------|
| `pingall` reports loss / hosts unreachable | IP forwarding not enabled on h2/h3, or a static route missing/wrong gateway. Check `ip route show` on each host. |
| `Destination Host Unreachable` from h1 | h1 has no default route — check `defaultRoute='via 10.0.0.2'` was set. |
| Switches don't forward | You are using OVSKernelSwitch without a controller. Use `--switch lxbr` as in `make topo`. |
| Changes not applied after editing `topology.py` | Run `make clean` (or `mn -c`) before restarting the topology. |
| GUI windows don't appear | Run `xhost +` on the lab machine and forward X11 into the container. |
