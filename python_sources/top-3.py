import re
import csv
import operator
from collections import defaultdict

all_tags = ['quantum-mechanics', 'homework-and-exercises', 'newtonian-mechanics', 'electromagnetism', 'quantum-field-theory', 'thermodynamics', 'general-relativity', 'special-relativity', 'classical-mechanics', 'forces', 'optics', 'fluid-dynamics', 'gravity', 'energy', 'particle-physics', 'electrostatics', 'cosmology', 'visible-light', 'statistical-mechanics', 'waves', 'black-holes', 'electricity', 'newtonian-gravity', 'electromagnetic-radiation', 'condensed-matter', 'experimental-physics', 'kinematics', 'photons', 'magnetic-fields', 'string-theory', 'lagrangian-formalism', 'spacetime', 'electric-circuits', 'mathematical-physics', 'mass', 'angular-momentum', 'differential-geometry', 'speed-of-light', 'solid-state-physics', 'pressure', 'operators', 'energy-conservation', 'nuclear-physics', 'momentum', 'electrons', 'rotational-dynamics', 'quantum-information', 'astrophysics', 'soft-question', 'astronomy', 'resource-recommendations', 'reference-frames', 'wavefunction', 'acoustics', 'temperature', 'conservation-laws', 'orbital-motion', 'hilbert-space', 'acceleration', 'time', 'friction', 'atomic-physics', 'quantum-spin', 'terminology', 'electric-fields', 'electric-current', 'schroedinger-equation', 'entropy', 'everyday-life', 'symmetry', 'water', 'charge', 'work', 'potential', 'universe', 'electrical-resistance', 'quantum-electrodynamics', 'velocity', 'standard-model', 'harmonic-oscillator', 'vectors', 'metric-tensor', 'gauge-theory', 'potential-energy', 'space-expansion', 'hamiltonian-formalism', 'field-theory', 'supersymmetry', 'relativity', 'material-science', 'radiation', 'entanglement', 'capacitance', 'collision', 'renormalization', 'laser', 'semiconductor-physics', 'reflection', 'group-theory', 'scattering', 'quantum-gravity', 'uncertainty-principle', 'research-level', 'earth', 'education', 'voltage', 'simulation', 'big-bang', 'measurement', 'torque', 'projectile', 'superconductivity', 'computational-physics', 'double-slit-experiment', 'units', 'conformal-field-theory', 'refraction', 'classical-electrodynamics', 'conventions', 'curvature', 'frequency', 'thermal-radiation', 'gravitational-waves', 'gauss-law', 'tensor-calculus', 'atmospheric-science', 'history', 'vacuum', 'coordinate-systems', 'definition', 'fourier-transform', 'inertial-frames', 'atoms', 'quantum-interpretations', 'probability', 'planets', 'ideal-gas', 'measurement-problem', 'path-integral', 'rotation', 'physical-chemistry', 'notation', 'faster-than-light', 'polarization', 'mass-energy', 'spring', 'interference', 'drag', 'feynman-diagram', 'maxwell-equations', 'rotational-kinematics', 'fermions', 'group-representations', 'quantum-chromodynamics', 'dark-matter', 'air', 'geometric-optics', 'geometry', 'spectroscopy', 'variational-principle', 'mathematics', 'power', 'aerodynamics', 'biophysics', 'diffraction', 'sun', 'hamiltonian', 'home-experiment', 'quantum-optics', 'quantum-computer', 'phase-transition', 'antimatter', 'neutrinos', 'integration', 'differentiation', 'specific-reference', 'time-dilation', 'dimensions', 'higgs', 'representation-theory', 'speed', 'solar-system', 'space', 'stars', 'lie-algebra', 'wave-particle-duality', 'symmetry-breaking', 'free-body-diagram', 'dirac-equation', 'boundary-conditions', 'commutator', 'dimensional-analysis', 'oscillators', 'topology', 'observers', 'density', 'spinors', 'action', 'heat', 'rocket-science', 'event-horizon', 'causality', 'singularities', 'perturbation-theory', 'elasticity', 'vector-fields', 'galaxies', 'estimation', 'tensors', 'centripetal-force', 'flow', 'resonance', 'stress-energy-tensor', 'linear-algebra', 'noethers-theorem', 'cosmological-inflation', 'moment-of-inertia', 'lenses', 'surface-tension', 'celestial-mechanics', 'plasma-physics', 'rigid-body-dynamics', 'error-analysis', 'radioactivity', 'quarks', 'crystals', 'physical-constants', 'ads-cft', 'relative-motion', 'statics', 'conductors', 'lorentz-symmetry', 'induction', 'hydrogen', 'software', 'dark-energy', 'coulombs-law', 'equilibrium', 'wavelength', 'superposition', 'geodesics', 'angular-velocity', 'buoyancy', 'eigenvalue', 'continuum-mechanics', 'electronic-band-theory', 'complex-numbers', 'centrifugal-force', 'discrete', 'geophysics', 'many-body', 'string', 'gauge-invariance', 'stress-strain', 'photoelectric-effect', 'statistics', 'fusion', 'electronics', 'dielectric', 'differential-equations', 'large-hadron-collider', 'vibration', 'observables', 'hydrostatics', 'cmb', 'density-operator', 'calculus', 'kinetic-theory', 'interactions', 'molecules', 'topological-field-theory', 'hawking-radiation', 'inductance', 'information', 'thermal-conductivity', 'free-fall', 'moon', 'diffusion', 'popular-science', 'batteries', 'topological-order', 'electrical-engineering', 'doppler-effect', 'approximations', 'metals', 'viscosity', 'covariance', 'greens-functions', 'distributions', 'particles', 'tidal-effect', 'neutrons', 'equivalence-principle', 'yang-mills', 'topological-insulators', 'vision', 'regularization', 'correlation-functions', 'constrained-dynamics', 'inertia', 'klein-gordon-equation', 'si-units', 'virtual-particles', 'bose-einstein-condensate', 'experimental-technique', 'data-analysis', 'second-quantization', 'wavefunction-collapse', 'distance', 'magnetic-moment', 'elementary-particles', 'beyond-the-standard-model', 'determinism', 'weak-interaction', 'protons', 'stability', 'fluid-statics', 'ising-model', 'nuclear-engineering', 'phase-space', 'weight', 'pauli-exclusion-principle', 'quantization', 'telescopes', 'unit-conversion', 'turbulence', 'time-evolution', 'magnetic-monopoles', 'degrees-of-freedom', 'evaporation', 'bernoulli-equation', 'propagator', 'scattering-cross-section', 'reversibility', 'partition-function', 'variational-calculus', 'chaos-theory', 'branes', 'matter', 'parity', 'states-of-matter', 'lattice-model', 'satellites', 'signal-processing', 'time-reversal-symmetry', 'decoherence', 'dipole', 'space-travel', 'quantum-anomalies', 'x-rays', 'aircraft', 'navier-stokes', 'interferometry', 'absorption', 'unitarity', 'adiabatic', 'graphene', 'thought-experiment', 'quantum-hall-effect', 'neutron-stars', 'higgs-boson', 'time-travel', 'phonons', 'non-linear-systems', 'radio', 'volume', 'orbitals', 'bosons', 's-matrix-theory', 'antennas', 'electroweak', 'ice', 'binding-energy', 'perpetual-motion', 'supergravity', 'holographic-principle', 'molecular-dynamics', 'metrology', 'gauge', 'compactification', 'lightning', 'quantum-chemistry', 'quantum-tunneling', 'wormholes', 'models', 'chirality', 'electromagnetic-induction', 'bells-inequality', 'explosions', 'nanoscience', 'particle-detectors', 'renewable-energy', 'weather', 'observational-astronomy', 'majorana-fermions', 'gamma-rays', 'dispersion', 'cosmological-constant', 'locality', 'ligo', 'gyroscopes', 'biology', 'vortex', 'strong-force', 'dirac-matrices', 'microscopy', 'classical-field-theory', 'stellar-physics', 'qft-in-curved-spacetime', 'propulsion', 'eye', 'heat-engine', 'fiber-optics', 'non-equilibrium', 'normalization', 'wick-rotation', 'convection', 'applied-physics', 'coherence', 'magnetostatics', 'perception', 'subatomic', 'theory-of-everything', 'superfluidity', 'light-emitting-diodes', 'duality', 'chern-simons-theory', 'noise', 'poincare-symmetry', 'poisson-brackets', 'supernova', 'gas', 'coriolis-effect', 'accelerator-physics', 'microwaves', 'coupled-oscillators', 'dipole-moment', 'spin-statistics', 'non-linear-optics', 'lift', 'radio-frequency', 'semiclassical', 'multipole-expansion', 'galilean-relativity', 'infrared-radiation', 'dissipation', 'effective-field-theory', 'gravitational-lensing', 'x-ray-crystallography', 'multiverse', 'gravitational-redshift', 'grassmann-numbers', 'photon-emission', 'topological-phase', 'chemical-potential', 'arrow-of-time', 'elements', 'helicity', 'precession', 'solid-mechanics', 'kaluza-klein', 'escape-velocity', 'blackbody', 'complex-systems', 'moment', 'brownian-motion', 'cp-violation', 'cooling', 'displacement', 'stellar-evolution', 'observable-universe', 'light', 'instantons', 'general-physics', 'numerical-method', 'data', 'wick-theorem', 'identical-particles', 'imaging', 'levitation', 'exoplanets', 'electrochemistry', 'born-rule', 'carnot-cycle', 'carrier-particles', 'aether', 'casimir-effect', 'confinement', 'climate-science', 'optical-materials', 'point-particle', 'warp-drives', 'anti-de-sitter-spacetime', 'linear-systems', 'foundations', 'teleportation', 'photovoltaics', 'quantum-statistics', 'meteorology', 'anyons', 'berry-pancharatnam-phase', 'bubble', 'cosmic-rays', 'visualization', 'solitons', 'poynting-vector', 'experimental-technology', 'camera', 'asteroids', 'loop-quantum-gravity', 'non-perturbative', 'grand-unification', 'integrable-systems', 'spin-model', 'spherical-harmonics', 'pair-production', 'non-locality', 'gluons', 'functional-derivatives', 'randomness', 'freezing', 'laws-of-physics', 'critical-phenomena', 'structural-beam', 'tachyon', 'textbook-erratum', 'mesons', 'material', 'ground-state', 'isotope', 'jerk', 'harmonics', 'brst', 'space-mission', 'pions', 'waveguide', 'scaling', 'isospin-symmetry', 'ions', 'gauge-symmetry', 'kerr-metric', 'hologram', 'black-hole-thermodynamics', 'capillary-action', 'shockwave', 'scale-invariance', 'redshift', 'particle-accelerators', 'chemical-compounds', 'medical-physics', 'milky-way', 'cold-atoms', 'stochastic-processes', 'color-charge', 'algorithm', 'order-of-magnitude', 'insulators', 'humidity', 'galaxy-rotation-curve', 'luminosity', 'condensation', 'density-functional-theory', 'epr-experiment', 'effective-action', 'trace', 'tight-binding', 'thermoelectricity', 'unified-theories', 'twin-paradox', 'sensor', 'baryons', 'absolute-units', 'fine-tuning', 'higgs-mechanism', 'invariants', 'ghosts', 'combustion', 'cpt-symmetry', 'quasiparticles', 'virtual-photons', 'density-of-states', 'clifford-algebra', 'normal-modes', 'numerics', 'magnetohydrodynamics', 'geomagnetism', 'ionization-energy', 'technology', 'piezoelectric', 'phase-diagram', 'quantum-states', 'machs-principle', 'matrix-elements', 'leptons', 'anticommutator', 'fermis-golden-rule', 'length-contraction', 'solar-system-exploration', 'white-holes', 'scales', 'physics-careers', 'big-list', 'computer', 'entanglement-entropy', 'phase-velocity', 'solar-wind', 'spin-chains', 'wigner-transform', 'solar-cells', 'diffeomorphism-invariance', 'asymptotics', 'non-linear-dynamics', 'modified-gravity', 'nasa', 'instrument', 'analyticity', 'category-theory', 'conservative-field', 'efficient-energy-use', 'ward-identity', 'schroedingers-cat', 'superalgebra', 'de-sitter-spacetime', 'cellular-automaton', 'optimization', 'open-quantum-systems', 'meteors', 'gps', 'fractals', 'baryogenesis', 'black-hole-firewall', 'raman-spectroscopy', 'plane-wave', 'superconformality', 'charge-conjugation', 'equations-of-motion', 'boundary-terms', 'linearized-theory', 'synchrotron-radiation', 'plasmon', 'radiometry', 'virial-theorem', 'wilson-loop', 'jupiter', 'laser-interaction', 'matrix-model', 'nucleosynthesis', 'moduli', 'image-processing', 'fan', 'calabi-yau', 'fluctuation-dissipation', 'stochastic-models', 'string-theory-landscape', 'inert-gases', 'integrals-of-motion', 'comets', 'clock', 'faq', 'cryogenics', 'laboratory-safety', 'mssm', 'oceanography', 'short-circuits', 'proton-decay', 'gravitational-collapse', 'exotic-matter', 'eclipse', 'graph-theory', 'pulsars', 'sigma-models', 'galaxy-clusters', 'dimensional-reg', 'atomic-excitation', 'anharmonic-oscillators', 'anthropic-principle', 'emergent-properties', 'energy-storage', 'interstellar-matter', 'low-temperature-physics', 'shadow', 'superspace-formalism', 'twistor', 'unruh-effect', 'minkowski-space', 'internal-energy', 'disorder', 'design', 'astrophotography', 'cavity-qed', 'interstellar-travel', 'lienard-wiechert', 'sports', 'rigid-solid', 'radar', 'relativistic-jets', 'photometry', 'structure-formation', 'network', 'higgs-field', 'fermi-liquids', 'cold-fusion', 'algebraic-geometry', 'dirac-monopole', 'equation-of-state', 'exchange-interaction', 'earthquake', 'cherenkov-radiation', 'building-physics', 'fluorescence', 'higher-spin', 'nature', 'string-field-theory', 'three-body-problem', 'percolation', 'meteorites', 'half-life', 'epistemology', 'adhesion', 'food', 'mean-free-path', 'porous-media', 'runge-lenz-vector', 'strong-correlated', 'reissner-nordstrom-metric', 'newtonian-fluid', 'length', 'frame-dragging', 'hadron-dynamics', 'accretion-disk', 'brachistochrone-problem', 'axion', 'functional-determinants', 'fock-space', 'liquid-crystal', 'non-commutative-geometry', 'nuclei', 'soft-matter', 'positronium', 'poincare-recurrence', 'steady-state', 'special-functions', 'thermal-field-theory', 'self-energy', 'quark-gluon-plasma', 'heavy-ion', 'bloch-sphere', 'braggs-law', 'deformation-quantization', 'diamond', 'closed-timelike-curve', 'bohmian-mechanics', 'binary-stars', 'leptogenesis', 'metallicity', 'potential-flow', 'stellar-population', 'maxwell-relations', 'non-linear-schroedinger', 'parallax', 'osmosis', 'amorphous-solids', 'canonical-conjugation', 'cosmic-censorship', 'dynamical-systems', 'displacement-current', 'bosonization', 'anderson-localization', 'astrometrics', 'atomic-clocks', 'non-commutative-theory', 'liquid-state', 'glass', 'topological-entropy', 'quasars', 'spin-glass', 'white-dwarfs', 'josephson-junction', 'ion-traps', 'large-n', 'metric-space', 'nucleation', 'born-oppenheimer-approx', 'amplituhedron', 'dirac-string', 'enthalpy', 'optical-lattices', 'nebulae', 'light-pollution', 'isotropy', 'gravitational-potential', 'unruh-radiation', 'two-level-system', 'seiberg-witten-theory', 'radiation-pressure', 'tsunami', 'solar-sails', 'wimps', 'isentropic', 'kerr-newman-metric', 'mass-spectrometry', 'cpt-violation', 'bloch-oscillation', 'bao', 'central-charge', 'debye-length', 'ferromagnetism', 'meteoroids', 'mnemonic', 'hadronization', 'grav-wave-detectors', 'geometric-topology', 'floquet-theory', 'supersymmetric-particles', 'transit', 'tevatron', 'quasicrystals', 'rheology', 'weak-lensing', 'fracture', 'gauss-bonnet', 'granulated-materials', 'nuclear-structure', 'magnets', 'lamb-shift', 'electromagnetic-field', 'cosmic-string', 'ballistics', 'birrefringence', 'landauers-principle', 'non-gaussianity', 'frw-universe', 'wightman-fields', 'wetting', 'reflectance', 'spin-liquid', 'sine-gordon', 'stellar-wind', 'rabi-model', 'free-electron-lasers', 'hopf-algebra', 'impedance-spectroscopy', 'irreversible', 'bifurcation', 'brown-dwarfs', 'correspondence-principle', 'couette-flow', 'econo-physics', 'duration', 'chirp', 'backscattering', 'affine-lie-algebra', 'antimatter-storage', 'pentaquarks', 'synthetic-gauge-fields', 'spin-ice', 'topological-charges', 'quasi-periodic', 'self-capacitance', 'feedback', 'heterotic-string', 'lamb-waves', 'logic-gates', 'machos']
all_tags = set(all_tags)


data_path = "../input/"
in_file = open(data_path+"test.csv")
out_file = open("sub_freq.csv", "w")
reader = csv.DictReader(in_file)
writer = csv.writer(out_file)
writer.writerow(['id','tags'])

def f1_score(tp, fp, fn):
    p = (tp*1.) / (tp+fp)
    r = (tp*1.) / (tp+fn)
    f1 = (2*p*r)/(p+r)
    return f1

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_words(text):
    word_split = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    return [word.strip().lower() for word in word_split.split(text)]
	
top_tags = ["quantum-mechanics", "homework-and-exercises", "newtonian-mechanics"]
for ind, row in enumerate(reader):
    text = clean_html(row["title"])
    tfrequency_dict = defaultdict(int)
    word_count = 0.
    for word in get_words(text):
        if word.isalpha() and word in all_tags:
            tfrequency_dict[word] += 1
            word_count += 1.
    for word in tfrequency_dict:
    	tf = tfrequency_dict[word] / word_count
    	tfrequency_dict[word] = tf 
    pred_title_tags = sorted(tfrequency_dict, key=tfrequency_dict.get, reverse=True)[:3]
    
    text = clean_html(row["content"])
    dfrequency_dict = defaultdict(int)
    word_count = 0.
    for word in get_words(text):
        if word.isalpha() and word in all_tags:
            dfrequency_dict[word] += 1
            word_count += 1.
    for word in dfrequency_dict:
    	tf = dfrequency_dict[word] / word_count
    	dfrequency_dict[word] = tf 
    pred_content_tags = sorted(dfrequency_dict, key=dfrequency_dict.get, reverse=True)[:3]
    
    pred_tags_dict = {}
    for word in set(pred_title_tags + pred_content_tags):
    	pred_tags_dict[word] = tfrequency_dict.get(word,0) + dfrequency_dict.get(word,0)
    pred_tags = set(sorted(pred_tags_dict, key=pred_tags_dict.get, reverse=True)[:3])
    
    
    length = len(pred_tags)
    for tag in top_tags[:3 - length]:
        pred_tags.add(tag)
    
    writer.writerow([row['id'], " ".join(pred_tags)])
    if ind%50000 == 0:
    	print("Processed : ", ind)





































































