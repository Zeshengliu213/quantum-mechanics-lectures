# Quantum Mechanics for Organic Electronics

**A 12-Lecture Series**
*Zesheng Liu · Linköping University · Laboratory of Organic Electronics*

---

## Series Philosophy

> **Understanding over derivation. History over formalism. Animation over equation.**

Each lecture starts with a question the student already wants answered, introduces the quantum mechanics needed to answer it, and lands on a concrete phenomenon in organic semiconductor physics. Every equation earns its place by solving a problem, not by completing a proof.

**Primary references:**
- K&B: Köhler & Bässler, *Electronic Processes in Organic Semiconductors* (Wiley, 2015)
- Nitzan: *Chemical Dynamics in Condensed Phases* (Oxford, 2006)
- 顾樵:《量子力学 I》

---

## Lecture Map

| # | QM Core | Organic Electronics Connection |
|---|---------|-------------------------------|
| 01 | History of QM | Why classical physics fails for π-electrons |
| 02 | Particle in a box | Conjugation length vs. bandgap |
| 03 | Quantum harmonic oscillator | Franck-Condon, Huang-Rhys, vibronic spectra |
| 04 | Tunneling | Charge injection at metal/organic interfaces, SAMs |
| 05 | Angular momentum & H atom | Carbon atomic orbitals → sp² hybridization |
| 06 | Spin & identical particles | Singlet/triplet, OLED spin statistics, radicals |
| 07 | Perturbation theory | Intermolecular coupling, CT states, interface dipoles |
| 08 | Variational method | LCAO, Hückel theory → DFT bridge |
| 09 | Periodic potentials & bands | Band vs. hopping transport in organic solids |
| 10 | Electron-phonon coupling | Polarons, Marcus theory, reorganization energy |
| 11 | Electron transfer at interfaces | D/A charge transfer, Onsager-Braun, molecular conduction |
| 12 | Excitons & many-body physics | Frenkel exciton, exciton diffusion, device efficiency limits |

---

## Phase I — Foundations

### Lecture 01: History of Quantum Mechanics

**Narrative arc:** The four pillars of classical physics collapse one by one.

**Outline:**

1. **The four pillars of classical physics**
   - Continuity, determinism, wave≠particle, passive measurement
   - Kelvin's "two clouds" (1900)

2. **Pillar I collapses: Continuity**
   - Blackbody radiation and the ultraviolet catastrophe
   - Planck's quantized oscillators: E = nhν (1900)
   - *Interactive: blackbody spectrum with temperature slider, Planck vs. Rayleigh-Jeans*

3. **Pillar II collapses: Waves become particles**
   - Photoelectric effect — Einstein's explanation (1905): K_max = hν − φ
   - Compton scattering — photon carries momentum: p = h/λ (1923)
   - *Animated: photons hitting metal → electrons ejected (switchable frequency/intensity)*
   - *Animated: Compton collision with adjustable scattering angle*

4. **Pillar III collapses: Particles become waves**
   - Bohr's atom — stationary states and quantum jumps (1913)
   - de Broglie hypothesis: λ = h/p (1924)
   - Davisson-Germer electron diffraction (1927)
   - Double-slit experiment — electron by electron
   - *Animated: electrons accumulate into interference pattern one dot at a time*
   - *Interactive: Bohr energy levels with clickable transitions*

5. **Pillar IV collapses: Measurement becomes active**
   - Stern-Gerlach experiment — beam splits into discrete spots (1922)
   - Cascaded Stern-Gerlach — Z then X: measurement destroys information
   - Heisenberg uncertainty principle: Δx·Δp ≥ ℏ/2
   - *Animated: SG beam splitting; cascaded SG showing state reset*
   - *Interactive: uncertainty — squeeze position, momentum spreads*

6. **1925–1927: A coherent theory emerges**
   - Heisenberg (matrix mechanics), Schrödinger (wave equation), Born (|ψ|² rule), Dirac (unified formalism)

7. **Summary: all four pillars fallen**

**Refs:** 顾樵 Ch.1 | Nitzan §1.3

---

### Lecture 02: Particle in a Box → Conjugation Length and Bandgap

**Central question:** Why do longer conjugated molecules absorb redder light?

**Outline:**

1. **The simplest quantum system**
   - 1D infinite square well: boundary conditions → quantized solutions
   - ψ_n(x) = √(2/L) sin(nπx/L), E_n = n²π²ℏ²/(2mL²)
   - *Interactive: eigenstates with adjustable n, showing nodes and |ψ|²*

2. **Energy quantization and the role of box size**
   - E_n ∝ n²/L² — larger box → smaller level spacing
   - HOMO-LUMO gap: ΔE = E_{N/2+1} − E_{N/2} ∝ 1/L²
   - *Interactive: adjust L, watch gap shrink in real time*

3. **From box to molecule: the free-electron model**
   - π-electrons in a conjugated chain ≈ particles in a 1D box
   - Effective box length L = (N+1)·d, where d ≈ 1.4 Å (C–C bond)
   - Prediction: absorption wavelength λ ∝ L²

4. **Testing the prediction: polyacene series**
   - Naphthalene → anthracene → tetracene → pentacene
   - Measured absorption maxima vs. free-electron prediction
   - Agreement is qualitative — Hückel theory (Lecture 8) does better

5. **Finite potential well — the more realistic box**
   - Walls are not infinite: wave function leaks into the barrier
   - Fewer bound states, energies shifted down
   - Preview of tunneling (Lecture 4)

6. **2D and 3D boxes — quantum dots**
   - Brief mention: the same physics explains CdSe quantum dot colors
   - Size-tunable emission = particle-in-a-box in 3D

7. **OE connection: effective conjugation length**
   - Disorder breaks the chain into segments of varying length
   - Distribution of conjugation lengths → inhomogeneous broadening
   - K&B §1.3.2, §2.1.2

**Refs:** 顾樵 Ch.3 | K&B §1.3.2 (Hückel model, polyene MOs), Box 1.5

---

### Lecture 03: Quantum Harmonic Oscillator → Franck-Condon and Vibronic Spectra

**Central question:** Why do organic semiconductor absorption/emission spectra have that characteristic vibronic progression?

**Outline:**

1. **The quantum harmonic oscillator**
   - Classical: mass on a spring, V(x) = ½kx²
   - Quantum: E_n = (n + ½)ℏω — equally spaced levels
   - Zero-point energy: the oscillator can never be perfectly still
   - *Interactive: energy levels and wave functions for different n*

2. **Ladder operators (raising/lowering)**
   - â⁺ and â: elegant algebraic approach
   - Why this matters: same formalism reappears for photons and phonons

3. **The displaced harmonic oscillator**
   - Excited state has a shifted equilibrium geometry (ΔQ)
   - Nitzan §2.9.4: the shifted oscillator model
   - *Animated: potential energy curves showing ground and excited state parabolas with offset*

4. **The Franck-Condon principle**
   - Nuclei are slow, electrons are fast → vertical transitions
   - Overlap integrals ⟨χ_m'|χ_n⟩ determine transition intensities
   - *Interactive: FC overlap calculation with adjustable displacement*

5. **The Huang-Rhys factor S**
   - S = ΔQ²·ω/(2ℏ) — measures electron-phonon coupling strength
   - S ≈ 0 → sharp 0-0 line (rigid molecule)
   - S ≈ 1 → prominent vibronic progression (flexible molecule)
   - S >> 1 → broad, featureless band

6. **Reading real spectra**
   - Absorption and emission as mirror images (in the harmonic limit)
   - Stokes shift = 2Sℏω
   - 0-0 peak, 0-1 peak, 0-2 peak spacing ≈ ℏω ≈ 0.17 eV (C=C stretch)
   - K&B §1.4.1–1.4.2: potential curves, radiative transitions, vibrational factor

7. **OE connection: spectral analysis of organic semiconductors**
   - Extracting S and ℏω from experimental PL spectra
   - What S tells you about molecular rigidity and reorganization energy
   - Preview: S is directly related to the reorganization energy λ in Marcus theory (Lecture 10)

**Refs:** 顾樵 Ch.4 | Nitzan §2.9 | K&B §1.4.1–1.4.2

---

### Lecture 04: Tunneling → Charge Injection and SAM Transport

**Central question:** How do charges get injected into organic semiconductors across energy barriers?

**Outline:**

1. **Quantum tunneling through a square barrier**
   - Classical: particle bounces back if E < V₀
   - Quantum: ψ decays exponentially inside the barrier but doesn't vanish
   - Transmission coefficient T ∝ exp(−2κd), where κ = √(2m(V₀−E))/ℏ
   - *Interactive: adjust barrier height and width, watch T change*

2. **WKB approximation for general barriers**
   - T ∝ exp(−2∫κ(x)dx) — works for smooth, slowly varying potentials
   - Fowler-Nordheim tunneling through a triangular barrier under applied field

3. **Tunneling at metal/organic interfaces**
   - Injection barrier = |E_F − HOMO| or |E_F − LUMO|
   - Thermionic emission vs. field-assisted tunneling vs. direct tunneling
   - Richardson-Schottky vs. Fowler-Nordheim regimes
   - K&B §4.1.3: charge injection into organic devices

4. **Tunneling through SAMs: the Simmons model**
   - R = R₀·exp(βd): resistance grows exponentially with SAM thickness
   - β ≈ 0.7–1.0 Å⁻¹ for alkanethiol SAMs
   - β ≈ 0.2–0.3 Å⁻¹ for conjugated SAMs (π-system provides a tunneling highway)
   - Nitzan Ch.17: molecular conduction

5. **SAMs as interface modifiers in organic devices**
   - Phosphonic acid SAMs as hole transport layers
   - How SAMs modify the work function: interface dipole layer
   - Connection to research: interfacial p-doping facilitates ohmic contact even when WF alignment seems unfavorable

6. **Resonant tunneling and negative differential resistance**
   - Brief preview: when energy aligns with a molecular level, T → 1
   - Relevance to molecular electronics

**Refs:** 顾樵 Ch.3 | Nitzan §2.10, Ch.17 | K&B §4.1.3

---

## Phase II — Angular Momentum, Spin, and Symmetry

### Lecture 05: Angular Momentum and the Hydrogen Atom → Atomic Orbitals of Carbon

**Central question:** Where do the s, p, d orbitals come from, and why does sp² hybridization create organic semiconductors?

**Outline:**

1. **Angular momentum in quantum mechanics**
   - Classical: L = r × p. Quantum: L̂ operators and commutation relations
   - [L̂x, L̂y] = iℏL̂z — angular momentum components don't commute
   - Simultaneous eigenstates of L̂² and L̂z: quantum numbers l, m

2. **Spherical harmonics Y_l^m(θ,φ)**
   - Visual shapes: s (sphere), p (dumbbell), d (clover)
   - *Interactive: 3D orbital shapes with selectable l, m*

3. **The hydrogen atom**
   - Radial equation → principal quantum number n
   - E_n = −13.6/n² eV — exact solution
   - Degeneracy: all states with the same n have the same energy (in H)

4. **From hydrogen to carbon**
   - Carbon: 1s² 2s² 2p² — four valence electrons
   - Why carbon is special: 4 valence electrons + small atomic radius → versatile bonding

5. **Hybridization as a quantum mechanical concept**
   - sp³: tetrahedral (methane, saturated polymers)
   - sp²: trigonal planar (ethene, conjugated systems) — the key to organic semiconductors
   - sp: linear (ethyne)
   - *Animated: orbital mixing from 2s + 2p → sp² hybrids + remaining pz*

6. **From sp² to π-conjugation**
   - Three sp² hybrids → σ-bonds (backbone)
   - Remaining pz → sideways overlap → π-bond → delocalization
   - K&B §1.3.1: atomic orbitals in carbon
   - This is why organic molecules can be semiconductors

**Refs:** 顾樵 Ch.5–6 | K&B §1.3.1

---

### Lecture 06: Spin and Identical Particles → Singlet/Triplet States and Organic Radicals

**Central question:** Why do OLEDs have a 25% efficiency limit (and how to beat it)?

**Outline:**

1. **Intrinsic angular momentum: spin**
   - Spin-½: the Stern-Gerlach result explained
   - Pauli matrices σx, σy, σz
   - Spin is not a classical rotation — it has no classical analog

2. **Addition of angular momenta**
   - Two spin-½ particles: S = 0 (singlet) or S = 1 (triplet)
   - Singlet: antisymmetric spin, one state
   - Triplet: symmetric spin, three states (m = −1, 0, +1)

3. **Identical particles and the Pauli exclusion principle**
   - Fermions: antisymmetric total wave function
   - Bosons: symmetric total wave function
   - Consequences: electron configuration, periodic table, molecular orbital filling

4. **Singlet and triplet excited states in organic molecules**
   - Singlet exciton S₁: electron and hole have antiparallel spins
   - Triplet exciton T₁: parallel spins
   - Exchange energy: why T₁ < S₁ (triplet is lower energy)
   - K&B §1.3.4

5. **Spin statistics in OLEDs**
   - Electrical excitation creates 25% singlets + 75% triplets
   - Only singlets emit (fluorescence) → 25% internal quantum efficiency limit
   - Phosphorescent emitters (Ir complexes): strong SOC → harvest triplets → 100%
   - TADF: thermally activated delayed fluorescence → reverse ISC from T₁ to S₁
   - K&B §4.3.2

6. **Organic radicals**
   - Open-shell molecules with unpaired electrons
   - Doublet ground state: S = ½
   - Applications: organic magnets, radical OLEDs, radical batteries

7. **Intersystem crossing (ISC)**
   - Spin-orbit coupling enables S₁ → T₁
   - Heavy atom effect: heavier atoms → stronger SOC → faster ISC
   - K&B §1.4.2.3 (spin factor), §1.4.4 (non-radiative transitions)

**Refs:** 顾樵 Ch.7 | K&B §1.3.4, §1.4.2.3, §4.3.2

---

## Phase III — Approximation Methods

### Lecture 07: Perturbation Theory → Intermolecular Coupling and CT States

**Central question:** How do molecules talk to each other, and what happens at D/A interfaces?

**Outline:**

1. **Why we need approximations**
   - Exact solutions exist only for ~5 systems (free particle, box, HO, H atom, …)
   - Real molecules: too complex → perturbation theory as a systematic tool

2. **Time-independent perturbation theory (non-degenerate)**
   - H = H₀ + λH': start from known solution, add small correction
   - First-order energy: E_n^(1) = ⟨ψ_n⁰|H'|ψ_n⁰⟩
   - Second-order energy and state mixing

3. **Degenerate perturbation theory**
   - When unperturbed levels are degenerate → must diagonalize H' in the degenerate subspace
   - Davydov splitting in molecular crystals as a direct example

4. **Time-dependent perturbation theory and Fermi's golden rule**
   - Transition rate: Γ = (2π/ℏ)|⟨f|H'|i⟩|²·ρ(E_f)
   - Nitzan §2.7.3
   - Application: optical absorption rate, charge transfer rate

5. **Intermolecular electronic coupling (transfer integral)**
   - J = ⟨ψ_A|H'|ψ_B⟩ — the "hopping" matrix element
   - J determines: exciton bandwidth, charge mobility, CT rate
   - Davydov splitting ΔE ≈ 2J
   - K&B §2.1.4

6. **Charge-transfer states at D/A interfaces**
   - CT state: electron on acceptor, hole on donor, Coulomb-bound
   - CT energy: E_CT ≈ IP_D − EA_A − e²/(4πεr)
   - Interface dipole: charge redistribution at the D/A boundary
   - Connection to research: HOMO offset as descriptor for interface dipoles

7. **From coupling to transport**
   - Weak coupling (J < kT): incoherent hopping (most organic semiconductors)
   - Strong coupling (J > kT): coherent band transport (organic single crystals)
   - Preview of Lecture 9

**Refs:** 顾樵 Ch.8 | Nitzan §2.7.3 | K&B §2.1.4, §3.6

---

### Lecture 08: Variational Method → LCAO, Hückel Theory, and the Bridge to DFT

**Central question:** How do we actually calculate molecular orbital energies?

**Outline:**

1. **The variational principle**
   - Theorem: ⟨ψ_trial|H|ψ_trial⟩ ≥ E_0 for any trial ψ
   - Proof is simple; the power is immense
   - Strategy: parameterize ψ_trial, minimize energy

2. **Linear combination of atomic orbitals (LCAO)**
   - ψ = Σ c_i φ_i — molecular orbital as a sum of atomic orbitals
   - Variational optimization → secular equation: det|H_ij − ES_ij| = 0
   - K&B Box 1.5: butadiene worked example

3. **Hückel theory: the minimal model for π-systems**
   - Approximations: S_ij = δ_ij, H_ii = α, H_ij = β (nearest neighbors only)
   - Butadiene: 4×4 secular determinant → 4 MO energies
   - *Interactive: Hückel energy levels for variable chain length*

4. **What Hückel theory gets right**
   - HOMO-LUMO gap decreases with chain length
   - Bond alternation pattern (HOMO vs. LUMO nodal structure)
   - Aromaticity: Hückel's 4n+2 rule for cyclic systems

5. **From Hückel to Hartree-Fock**
   - Self-consistent field (SCF): guess ψ → compute V → solve → iterate
   - Electron-electron repulsion included (Hückel ignores it)
   - INDO, CNDO: semi-empirical shortcuts

6. **Density functional theory (DFT): the modern workhorse**
   - Hohenberg-Kohn theorem: ground-state energy is a functional of electron density ρ(r)
   - Kohn-Sham equations: map interacting problem onto non-interacting orbitals
   - What DFT gives you: optimized geometry, HOMO/LUMO energies, vibrational frequencies
   - Limitations: bandgap underestimation, dispersion corrections needed

7. **OE connection: designing molecules computationally**
   - DFT-predicted HOMO/LUMO → screening candidates for OSCs and OLEDs
   - Connection to research: XGBoost predicting interface dipoles from DFT-computed descriptors

**Refs:** 顾樵 Ch.8 | K&B §1.3.2, Box 1.5 | Nitzan §4.3.4

---

## Phase IV — From Molecules to Solids

### Lecture 09: Periodic Potentials → Band vs. Hopping Transport

**Central question:** Why do organic single crystals have band transport while amorphous films have hopping?

**Outline:**

1. **Bloch's theorem**
   - Periodic potential V(x+a) = V(x) → ψ_k(x) = e^{ikx}·u_k(x)
   - Crystal momentum ℏk, Brillouin zone

2. **Kronig-Penney model**
   - Periodic square wells → allowed energy bands separated by gaps
   - Band width depends on barrier transparency (coupling strength)
   - *Interactive: adjust barrier height, watch bands form and widen*

3. **Tight-binding model (solid-state Hückel)**
   - Start from atomic orbitals, add nearest-neighbor coupling t
   - Band dispersion: E(k) = ε ± 2t·cos(ka)
   - Bandwidth W = 4t — same J as in Lecture 7
   - Nitzan §4.3.4

4. **Effective mass and band curvature**
   - m* = ℏ²/(d²E/dk²) — heavier effective mass = narrower band = slower carrier
   - Organic crystals: narrow bands (W ~ 0.1–0.5 eV) → heavy effective mass

5. **When bands break down: the Anderson localization perspective**
   - Disorder potential → wave function localization
   - Mott criterion: when mean free path < lattice spacing, band picture fails

6. **Hopping transport in disordered organic films**
   - Gaussian Disorder Model (GDM): Bässler's model
   - Site energies drawn from Gaussian distribution σ ~ 0.05–0.15 eV
   - Miller-Abrahams hopping rate: Γ ∝ exp(−2αR)·exp(−ΔE/kT)
   - K&B §3.3

7. **OE connection: band vs. hopping — the transport crossover**
   - Rubrene single crystal: μ ~ 20 cm²/Vs, band-like T-dependence
   - Amorphous P3HT: μ ~ 10⁻⁴ cm²/Vs, activated hopping
   - Morphology (crystallinity, grain boundaries) controls which regime
   - Connection to research: GIWAXS as a tool to assess crystallinity

**Refs:** 顾樵 (periodic potential) | Nitzan §4.3 | K&B §3.3

---

### Lecture 10: Electron-Phonon Coupling → Polarons, Marcus Theory, and Reorganization Energy

**Central question:** Why is charge transport in organic semiconductors so different from silicon?

**Outline:**

1. **Phonons: quantized lattice vibrations**
   - Classical: coupled oscillators → normal modes
   - Quantum: each mode is a QHO → phonon occupation n_q
   - Acoustic vs. optical phonons
   - Nitzan §4.2

2. **Electron-phonon coupling: the polaron concept**
   - A charge on a molecule distorts the molecular geometry
   - The charge + distortion = polaron (a dressed quasiparticle)
   - Holstein model: local coupling to intramolecular vibrations
   - Polaron binding energy E_p = λ/2

3. **Marcus theory of electron transfer**
   - Two parabolas: reactant and product potential energy surfaces
   - Activation energy: ΔG‡ = (λ + ΔG⁰)²/(4λ)
   - Rate: k_ET = (2π/ℏ)|J|²·(1/√4πλkT)·exp(−ΔG‡/kT)
   - Nitzan Ch.16: the clearest derivation of Marcus theory
   - *Interactive: two parabolas with adjustable λ and ΔG⁰*

4. **The reorganization energy λ**
   - λ_inner: intramolecular geometry change (from DFT)
   - λ_outer: polarization of surrounding medium
   - λ = λ_inner + λ_outer
   - Connection to Huang-Rhys factor: λ_inner = Sℏω (from Lecture 3)

5. **Marcus inverted region**
   - When −ΔG⁰ > λ: rate DECREASES with increasing driving force
   - Counterintuitive but experimentally confirmed
   - Implications for charge recombination in OSCs

6. **From single rates to macroscopic mobility**
   - Hopping mobility: μ = ea²ν₀/(kT)·exp(−E_a/kT)
   - Relationship between Marcus rate and GDM hopping

7. **OE connection: designing low-reorganization-energy molecules**
   - Rigid, planar molecules (pentacene, C₆₀) have small λ → fast transport
   - Flexible molecules have large λ → slow transport
   - Connection to research: how molecular design controls λ

**Refs:** Nitzan §4.2, Ch.16 | K&B §1.4.4, §3.3

---

## Phase V — Advanced Topics and Device Connections

### Lecture 11: Electron Transfer at Interfaces → Organic Solar Cell Physics

**Central question:** How does a photon become an electric current in an organic solar cell?

**Outline:**

1. **Molecular conduction: the Landauer approach**
   - Conductance as transmission: G = (2e²/h)·T(E_F)
   - Transmission through a single molecule: resonant vs. off-resonant
   - Nitzan Ch.17

2. **Energy level alignment at interfaces**
   - Vacuum level, ionization energy, electron affinity
   - Schottky-Mott limit vs. real interfaces: Fermi level pinning
   - Interface dipole: Δ = φ_metal − (IP_org or EA_org)
   - Nitzan §4.4–4.5 (work function, screening)

3. **The photovoltaic process step by step**
   - Photon absorption → exciton generation
   - Exciton diffusion to D/A interface (L_D ~ 5–10 nm)
   - Charge transfer: exciton → CT state
   - CT state dissociation: Onsager-Braun model
   - Charge collection at electrodes
   - K&B §4.2

4. **Geminate pair dissociation**
   - Onsager (1938): escape probability in a Coulomb potential
   - Braun extension: finite CT state lifetime
   - K&B §3.6: geminate pair creation and dissociation

5. **The role of energetics: VOC, JSC, and FF**
   - V_OC ∝ (IP_D − EA_A) − losses
   - Strategies to increase V_OC, J_SC, and fill factor
   - K&B §4.2.3–4.2.5

6. **Interface dipoles and energy level tuning**
   - SAMs and interlayers to modify electrode work function
   - Connection to research: SAM-induced p-doping, tape-adhesion defect removal
   - Connection to research: ML prediction of D/A interface dipoles

7. **Thermodynamic efficiency limit**
   - Shockley-Queisser for organic: modified by exciton binding energy and voltage losses
   - K&B §4.2.5

**Refs:** Nitzan Ch.17, §4.4–4.5 | K&B §3.6, §4.2

---

### Lecture 12: Excitons, Frenkel Model, and Device Photophysics

**Central question:** What happens to excitations in organic solids, and how does this limit device performance?

**Outline:**

1. **Many-electron wave functions**
   - Slater determinant: antisymmetrized product of single-particle orbitals
   - Why single-particle MOs are an approximation
   - Electron correlation: exchange and Coulomb integrals

2. **Frenkel excitons in molecular crystals**
   - Excited state delocalized over N molecules
   - Exciton bandwidth W_ex = 4J (same J as Lecture 7)
   - Dispersion: E(k) = E_0 + 2J·cos(ka)
   - K&B §2.1.5

3. **H-aggregates and J-aggregates**
   - H-aggregate: blue-shifted absorption, suppressed 0-0 emission
   - J-aggregate: red-shifted absorption, enhanced 0-0 emission
   - Structural origin: side-by-side vs. head-to-tail packing

4. **CT excitons and Wannier excitons**
   - CT exciton: electron and hole on adjacent molecules
   - Wannier exciton: large radius, weak binding (not typical in organics)
   - Organic semiconductors: mostly Frenkel + some CT character

5. **Exciton diffusion**
   - Förster transfer (singlet): long-range, dipole-dipole, R⁻⁶
   - Dexter transfer (triplet): short-range, orbital overlap, exponential
   - Diffusion length: L_D = √(Dτ) ~ 5–20 nm for singlets
   - K&B §3.7

6. **Bimolecular processes**
   - Singlet-singlet annihilation (SSA)
   - Triplet-triplet annihilation (TTA) → delayed fluorescence
   - Triplet-charge annihilation (TCA)
   - K&B §3.8

7. **Device efficiency limits**
   - OLED: internal quantum efficiency × outcoupling
   - OSC: Shockley-Queisser × exciton-specific losses
   - The role of non-radiative recombination
   - K&B §4.2.5, §4.3

**Refs:** K&B §2.1.5, §3.7, §3.8, §4.2.5, §4.3 | Nitzan §6.2.3

---

## Appendix: Interactive Elements Summary

Each lecture contains 2–5 interactive HTML/Canvas demonstrations:

| Lecture | Interactive Elements |
|---------|---------------------|
| 01 | Blackbody spectrum slider, photoelectric animation, Compton collision, double-slit accumulation, SG beam split, cascaded SG, uncertainty slider |
| 02 | Eigenstates (adjustable n), box size vs. gap, polyacene absorption comparison |
| 03 | HO wave functions, displaced oscillator FC overlap, Huang-Rhys progression |
| 04 | Barrier tunneling (adjustable V₀, d), SAM β-factor comparison |
| 05 | 3D orbital shapes, sp² hybridization step-by-step |
| 06 | Singlet/triplet state construction, OLED spin statistics diagram |
| 07 | Perturbation energy correction, Davydov splitting |
| 08 | Hückel MO levels (adjustable chain), butadiene orbital coefficients |
| 09 | Kronig-Penney bands, GDM hopping simulation |
| 10 | Marcus two-parabola diagram (adjustable λ, ΔG⁰), inverted region |
| 11 | Energy level alignment diagram, Onsager escape probability |
| 12 | Frenkel exciton dispersion, Förster vs. Dexter range comparison |

---

*Last updated: April 2026*
