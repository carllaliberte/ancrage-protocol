# ANCRAGE

Re-mesurer avant date.
Physique ≠ crypto.
Version 0 : téléphone + gratuit.

Un ancrage expire. Il n'est pas faux. Il est à refaire.
Pas de photon inventé. Pas de node QUANTUM sur Git.

## Commandes

```bash
python3 ancrage.py ecrire --objet figure --avant 2028-08-31
python3 ancrage.py verifier carte.ancrage.json
python3 ancrage.py lire carte.ancrage.json
```

`ecrire` prend un verrou sidecar POSIX (`carte.ancrage.json.lock`) via `fcntl.flock`, comme mesure. Pas sur `lire` / `verifier`. Windows : pas de lock. Un `.lock` orphelin est inoffensif.

`verifier` refuse une date déjà passée.
Reculer la date sans nouvel acte = interdit (autre ancrage).

Carte citée : https://acorn-royal-dune-blend.grok.me  
Cadastre : https://github.com/carllaliberte/famille

© 2026 Carl Laliberté. MIT.
