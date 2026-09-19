# Fork a repository

Forking a repository on GitHub lets you create your own copy of a project so you can experiment, contribute changes, and manage work without changing the upstream repository directly.

## About forks

A fork is a separate repository that starts as a copy of another repository. The original repository is called the **upstream repository**.

Forks are useful when you want to:

- Propose changes to an upstream repository.
- Experiment safely in your own copy of a project.
- Maintain a customized version of a project.
- Collaborate without needing direct write access to the upstream repository.

A fork is different from a branch. A branch exists inside a single repository, while a fork is its own repository with its own settings, collaborators, and pull requests.

> [!NOTE]
> Forks stay connected to the upstream repository through the repository network. That connection makes it possible to keep your fork synchronized with changes from the upstream repository.

## Prerequisites

Before you fork a repository and work with it locally, make sure you have completed the following setup:

- Install Git and configure your name, email address, and preferred default branch name.
- Set up authentication with GitHub, such as HTTPS credentials or SSH keys.
- Install [GitHub CLI](https://cli.github.com/) if you want to fork repositories from the command line.
- Install [GitHub Desktop](https://desktop.github.com/) if you prefer a desktop application.

For the full setup steps, see GitHub Docs:

- [Set up Git](https://docs.github.com/en/get-started/git-basics/set-up-git)
- [About GitHub CLI](https://docs.github.com/en/github-cli/github-cli/about-github-cli)

## Forking a repository in the GitHub web UI

Use these steps to create a fork in your browser.

1. On GitHub, navigate to the repository you want to fork.
2. In the upper-right corner of the page, click **Fork**.
3. Under **Owner**, choose the account or organization that should own the new fork.
4. In **Repository name**, keep the existing name or enter a new name for your fork.
5. In **Description**, optionally enter a short description.
6. Optionally select **Copy the default branch only**.

   Copying only the default branch is often enough when you are contributing to an open source project. If you leave this option unselected, GitHub copies all branches from the upstream repository into the new fork.

7. Click **Create fork**.

> [!NOTE]
> If you fork only the default branch and later need another branch, you can fetch it from the upstream repository after you configure `upstream` locally.

## Forking a repository with GitHub CLI

If you use GitHub CLI, create a fork with `gh repo fork`.

### Basic usage

```shell
gh repo fork REPOSITORY
```

Replace `REPOSITORY` with a repository in `OWNER/REPO` format, such as `octocat/Spoon-Knife`.

### Fork into an organization

Use `--org` to create the fork in an organization that allows you to create repositories.

```shell
gh repo fork REPOSITORY --org YOUR-ORG
```

### Clone the fork immediately

Use `--clone=true` if you want GitHub CLI to clone the fork to your computer right after creating it.

```shell
gh repo fork REPOSITORY --clone=true
```

### Configure a remote for the upstream repository

Use `--remote=true` to configure a remote for the upstream repository automatically.

```shell
gh repo fork REPOSITORY --remote=true
```

### Choose a custom remote name

Use `--remote-name` if you want a remote name other than the default value.

```shell
gh repo fork REPOSITORY --remote=true --remote-name upstream-repo
```

### Combine flags in one command

You can combine flags when you want GitHub CLI to create the fork, clone it locally, and configure the upstream repository in one step.

```shell
gh repo fork REPOSITORY --clone=true --remote=true
```

## Forking with GitHub Desktop

GitHub Desktop can help you fork a repository while you work locally.

1. Open GitHub Desktop.
2. Clone a repository that you do not have permission to push to.
3. Make a change on a topic branch and try to publish or push the branch.
4. When GitHub Desktop prompts you to create a fork, follow the dialog to continue.
5. Choose whether the fork is for contributing back to the upstream repository or for your own work.

For more detailed Desktop-specific screenshots and workflow guidance, see the GitHub Docs article on forking a repository.

## Cloning your forked repository

If you created the fork in the web UI and have not cloned it yet, clone your fork with `git clone`.

```shell
git clone https://github.com/YOUR-USERNAME/YOUR-FORK.git
```

For example:

```shell
git clone https://github.com/YOUR-USERNAME/Spoon-Knife.git
```

After cloning, move into the repository directory:

```shell
cd YOUR-FORK
```

## Configuring Git to sync your fork with the upstream repository

After you clone your fork, add the upstream repository as a second remote so you can pull in changes from the original project.

1. Change into your cloned fork.
2. Add the upstream repository remote:

   ```shell
   git remote add upstream https://github.com/ORIGINAL-OWNER/ORIGINAL-REPOSITORY.git
   ```

3. Verify your remotes:

   ```shell
   git remote -v
   ```

You should see both `origin` and `upstream`:

```shell
origin    https://github.com/YOUR-USERNAME/YOUR-FORK.git (fetch)
origin    https://github.com/YOUR-USERNAME/YOUR-FORK.git (push)
upstream  https://github.com/ORIGINAL-OWNER/ORIGINAL-REPOSITORY.git (fetch)
upstream  https://github.com/ORIGINAL-OWNER/ORIGINAL-REPOSITORY.git (push)
```

> [!NOTE]
> Once `upstream` is configured, you can fetch changes from the upstream repository and merge or rebase them into your local topic branch or your local copy of the default branch.

## Editing a fork

A common fork-based workflow looks like this:

1. Sync your local copy of the default branch with the upstream repository.
2. Create a new topic branch for your change.
3. Make and commit your changes on that topic branch.
4. Push the topic branch to your fork.
5. Open a pull request from your fork to the upstream repository.

For example, after updating your local default branch, you might run:

```shell
git switch -c my-topic-branch
```

Then push the topic branch to your fork:

```shell
git push -u origin my-topic-branch
```

When your branch is ready, open a pull request on GitHub so the upstream repository maintainers can review your work.

## Finding other repositories to fork

You can fork most public repositories to your personal account. You can also fork to an organization when that organization allows you to create repositories.

To find projects worth forking:

- Browse [GitHub Explore](https://github.com/explore).
- Search for projects related to your interests or programming languages.
- Look for repositories with issues labeled for new contributors.
- Review the repository's contribution guidelines before you start working.

For more details about when forking is available, see [Forks](https://docs.github.com/en/pull-requests/reference/forks).

## Next steps

After you create a fork, these guides can help you continue:

- [Syncing a fork](https://docs.github.com/en/pull-requests/how-tos/work-with-forks/syncing-a-fork)
- [Creating a pull request from a fork](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request-from-a-fork)
- [Managing branches within your repository](https://docs.github.com/en/pull-requests/how-tos/commit-changes/managing-branches-within-your-repository)
- [Finding ways to contribute to open source on GitHub](https://docs.github.com/en/get-started/exploring-projects-on-github/finding-ways-to-contribute-to-open-source-on-github)
