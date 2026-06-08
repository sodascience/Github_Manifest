# Git Hub branching strategies at SoDa
## GitHub Flow

```
main ──●──────────────────────────●──── (protected, always stable)
        \                        /
         feature/my-feature ────●
```

All work happens in short-lived feature branches that merge into `main` via PR. `main` is always in a state that could be shared or deployed.

## Git Flow

```
main     ──●────────────────────────●──  (tagged releases only)
            \                      /
develop  ────●────●──────────────●────
              \  /\              /
         feature  \            /
                  release/1.2.0
```

There are multiple branches that enable iterative product development process. This framework is usually used for more complex, critical projects that have release-based deployments where one release can contain 1 or more features or fixes.

| Branch | Purpose |
|---|---|
| `main` | Tagged, published releases only |
| `develop` | Active development, integration target |
| `feature/<name>` | All new work, branched from `develop` |
| `release/<version>` | Stabilization before tagging |
| `hotfix/<name>` | Urgent fixes applied directly to `main` + `develop` |

## Branch naming

Branch names should reflect the type of the changes that the branch is bringing followed by a short name written in kebab-case (separated by hyphens)

Examples of branch names:

```
feature/add-csv-export
fix/null-handling-parser
docs/update-contributing
refactor/simplify-api
release/1.3.0
hotfix/security-input-validation
```