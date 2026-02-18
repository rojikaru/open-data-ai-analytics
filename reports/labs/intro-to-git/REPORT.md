# Report: Intro to Git

[This repository on GitHub](https://github.com/rojikaru/open-data-ai-analytics)

## What I learned

- **Git Basics**: I learned how to initialize a git repository, stage changes, commit with meaningful messages, and push to a remote repository on GitHub.
- **Branching**: I practiced creating and switching between branches, which is essential for managing different features or experiments without affecting the main codebase.
- **Merging**: I learned how to merge branches back into the main branch, and how to resolve merge conflicts when they arise.
- **Git Log**: I explored the git log to understand the history of commits and how to visualize the commit graph.

## What I have done

- Initialized a git repository for my project.
- Created a main branch and a few feature branches for adding new functionality.
- Made several commits with descriptive messages to track my changes (conforming to conventional commits).
- Pushed my changes to GitHub and created a pull request to merge my feature branch into the main branch.
- Resolved a merge conflict that occurred during the merging process.
- Set up commitizen to auto-generate changelog entries based on my commit messages.

## Output of the `git log --oneline --graph --all` command

```plaintext
* 5c87848 (HEAD -> feat/changelog) bump: version 0.0.0 → 0.1.0
| * 62994e2 (tag: 0.1.0) bump: version 0.0.0 → 0.1.0
|/  
* 86e7ef0 (origin/main, origin/HEAD, main) feat: add vehicle ownership plot
| * de23571 (origin/feat/visualization, feat/visualization) feat: add vehicle ownership plot
|/  
* 803b97a feat: vehicle ownership by region
* f367e17 feat: most common vehicle types
* fcc3542 docs: update app entrypoint
* fb93268 chore: relax pylance strictness
| * 506ea77 (origin/feat/data_research, feat/data_research) feat: vehicle ownership by region
| * 3f44dc9 feat: most common vehicle types
| * 44a57a9 docs: update app entrypoint
| * b5367f0 chore: relax pylance strictness
|/  
* 2db4d50 feat(data): minimalistic data quality analysis
| * fca2c3e (origin/feat/data_quality_analysis, feat/data_quality_analysis) feat(data): minimalistic data quality analysis
|/  
* b2cee72 feat: add dataset load function
| * 463e7ce (origin/feat/data-load) feat: add dataset load function
|/  
* f09e8b0 chore: initialize the project
* ff4d030 docs: add LICENSE
* 20fdbfe docs: add README
* 8262cab chore: initial commit
```
