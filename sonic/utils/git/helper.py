from github import Github, GithubException, InputGitTreeElement
from sonic.utils.logger import LOG
import datetime


class GitHelper:
    def __init__(self, access_token: str, repo_name: str, base_dir: str = "projects"):
        self.base_dir = base_dir
        self.g = Github(access_token)
        try:
            self.repo = self.g.get_repo(repo_name)
            LOG.info(f"Repository loaded: {self.repo.full_name}")
        except GithubException as e:
            LOG.info(f"Failed to load repository: {e}")

    def create_project(self, project_name: str):
        """Creates a new branch in the repository."""
        try:
            # Get the default branch (usually "main" or "master")
            default_branch = self.repo.default_branch
            base_sha = self.repo.get_branch(default_branch).commit.sha
            # Create new branch from the default branch's latest commit
            self.repo.create_git_ref(ref=f"refs/heads/{project_name}", sha=base_sha)
            LOG.info(f"Branch '{project_name}' created successfully.")
        except GithubException as e:
            if e.status == 422:
                LOG.info(f"Branch '{project_name}' already exists.")
            else:
                LOG.info(f"Failed to create branch '{project_name}': {e}")

    def commit(
        self,
        project_name: str,
        commit_message: str,
        file_content: str,
        filename: str = "",
    ):
        try:
            # Retrieve the branch reference
            ref = f"heads/{project_name}"
            branch_ref = self.repo.get_git_ref(ref)
            base_sha = branch_ref.object.sha

            # Create a new file content
            # Create a blob
            blob = self.repo.create_git_blob(file_content, "utf-8")

            # Get the tree of the branch
            base_tree = self.repo.get_git_tree(base_sha)

            # generate timestamp for the commit
            timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

            # use timestamp for filename
            if not filename:
                filename = f"{timestamp}.txt"

            # Create a tree element for the sub-directory and the file within it
            element = InputGitTreeElement(
                path=f"{self.base_dir}/{project_name}/{filename}",
                mode="100644",
                type="blob",
                sha=blob.sha,
            )

            # Create a new tree that includes the sub-directory and file
            tree = self.repo.create_git_tree([element], base_tree)

            # Create a new commit on the branch
            parent = self.repo.get_git_commit(base_sha)
            commit = self.repo.create_git_commit(commit_message, tree, [parent])

            # Update branch ref to new commit
            branch_ref.edit(commit.sha)

            LOG.info(
                f"Commit successful on branch '{project_name}' with message '{commit_message}'. Created file in sub-directory '{project_name}'."
            )
        except GithubException as e:
            LOG.info(f"Failed to commit to branch '{project_name}': {e}")
