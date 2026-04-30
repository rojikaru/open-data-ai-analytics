## 0.5.0 (2026-04-30)

### Feat

- **infra**: replace Azure Terraform with AWS EC2
- add web console
- add sqlite facade

### Fix

- **aws**: bigger instance
- use non-spot VM
- set bigger vm variant
- **web**: jinja2 template response new version contact
- **deploy**: docker configuration & dependency resolution
- **deploy**: missing env
- **deploy**: docker installation during init
- **deploy**: cloud init header
- **terraform**: SKU offer
- **terraform**: ubuntu offer
- **terraform**: switch from ED25519 to RSA keys
- **terraform**: track lockfile for reproducible deployments
- code smells in Dockerfiles and data manipulation
- add sqlite create into pipeline

## 0.4.1 (2026-04-01)

### Fix

- code smells in Dockerfiles and data manipulation
- add sqlite create into pipeline

## 0.4.0 (2026-04-01)

### Feat

- add web console
- add sqlite facade
- **ci**: configure self-host runner
- **ci**: configure cloud runner
- split up project execution steps

### Fix

- switch self-host CI to uv
- **ci**: node.js 20 deprecation in actions/checkout

## 0.3.0 (2026-03-11)

### Feat

- **ci**: configure self-host runner
- **ci**: configure cloud runner
- split up project execution steps

### Fix

- **ci**: node.js 20 deprecation in actions/checkout

### Refactor

- improve error handling and documentation in data loading functions
- format files

## 0.2.0 (2026-02-18)

### Feat

- add datasets automatic download

### Refactor

- format files
- define constants module

## 0.1.0 (2026-02-18)

### Feat

- add vehicle ownership plot
- vehicle ownership by region
- most common vehicle types
- **data**: minimalistic data quality analysis
- add dataset load function
