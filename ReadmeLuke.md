# Customizing an Open-Source Project with Upstream Updates

This guide provides step-by-step instructions to clone an original open-source project, customize it in your "custom" repository, and keep it updated with the upstream changes using **merge** (not rebase).

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [1. Clone the Original Repository](#1-clone-the-original-repository)
  - [2. Create a Private Repository on GitHub](#2-create-a-private-repository-on-github)
  - [3. Configure Git Remotes](#3-configure-git-remotes)
  - [4. Push to Your Private Repository](#4-push-to-your-private-repository)
  - [5. Customize Your Code](#5-customize-your-code)
- [Maintaining Updates from the Original Project](#maintaining-updates-from-the-original-project)
  - [1. Fetch Updates from Upstream](#1-fetch-updates-from-upstream)
  - [2. Merge Updates into Your Main Branch](#2-merge-updates-into-your-main-branch)
  - [3. Push Merged Changes to Your Repository](#3-push-merged-changes-to-your-repository)
- [Additional Tips](#additional-tips)

---

## Prerequisites

- **Git** installed on your local machine.
- A **GitHub** account.

---

## Setup Instructions

### 1. Clone the Original Repository

Clone the original project's repository to your local machine.

```bash
git clone https://github.com/original_username/original-project.git
```

> Replace `original_username` and `original-project` with the appropriate GitHub username and repository name.

---

### 2. Create a Private Repository on GitHub

1. Log in to your GitHub account.
2. Click the **"+"** icon in the top-right corner and select **"New repository"**.
3. Name your repository (e.g., `my-custom-project`).
4. Choose **Private** for the repository visibility.
5. **Do not** initialize the repository with a README, `.gitignore`, or license.

---

### 3. Configure Git Remotes

Navigate to your cloned repository and set up the remotes.

```bash
cd original-project
```

#### a. Rename the Original Remote to Upstream

Rename the `origin` remote to `upstream` to track the original project.

```bash
git remote rename origin upstream
```

#### b. Add Your Private Repository as Origin

Add your new private repository as the `origin` remote.

```bash
git remote add origin https://github.com/your_username/my-custom-project.git
```

> Replace `your_username` and `my-custom-project` with your GitHub username and your private repository name.

---

### 4. Push to Your Private Repository

Push the code to your private repository on GitHub.

```bash
git push -u origin main
```

> If the default branch is not `main`, replace `main` with the correct branch name (e.g., `master`).

---

### 5. Customize Your Code

You can now make changes to the codebase as needed.

```bash
# Make your custom changes

git add .
git commit -m "Your custom changes"
git push
```

---

## Maintaining Updates from the Original Project

### 1. Fetch Updates from Upstream

Periodically fetch changes from the original repository to stay updated.

```bash
git fetch upstream
```

---

### 2. Merge Updates into Your Main Branch

Merge the fetched updates into your main branch.

```bash
git merge upstream/main
```

> Resolve any merge conflicts if they occur.

---

### 3. Push Merged Changes to Your Repository

After merging, push the updates to your private repository.

```bash
git push
```

---

## Additional Tips

- **Regular Updates**: Regularly check for updates from the upstream repository to keep your project up-to-date.
- **Conflict Resolution**: Carefully resolve merge conflicts to maintain the integrity of your custom changes.
- **Backup**: Before performing merges, consider backing up your current state.
- **Collaboration**: If working with collaborators, ensure they are aware of the workflow, especially regarding merges from upstream.

---

By following this guide, you'll maintain a customized version of an open-source project that stays synchronized with the original repository's updates using merges.
