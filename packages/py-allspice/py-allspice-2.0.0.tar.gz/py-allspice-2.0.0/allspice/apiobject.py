import logging
from datetime import datetime
from typing import List, Tuple, Dict, Sequence, Optional, Union, Set

from .baseapiobject import ReadonlyApiObject, ApiObject
from .exceptions import *


class Organization(ApiObject):
    """see https://hub.allspice.io/api/swagger#/organization/orgGetAll"""

    API_OBJECT = """/orgs/{name}"""  # <org>
    ORG_REPOS_REQUEST = """/orgs/%s/repos"""  # <org>
    ORG_TEAMS_REQUEST = """/orgs/%s/teams"""  # <org>
    ORG_TEAMS_CREATE = """/orgs/%s/teams"""  # <org>
    ORG_GET_MEMBERS = """/orgs/%s/members"""  # <org>
    ORG_IS_MEMBER = """/orgs/%s/members/%s"""  # <org>, <username>
    ORG_HEATMAP = """/users/%s/heatmap"""  # <username>

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Organization): return False
        return self.allspice_client == other.allspice_client and self.name == other.name

    def __hash__(self):
        return hash(self.allspice_client) ^ hash(self.name)

    @classmethod
    def request(cls, allspice_client: 'AllSpice', name: str) -> 'Organization':
        return cls._request(allspice_client, {"name": name})

    @classmethod
    def parse_response(cls, allspice_client, result) -> 'Organization':
        api_object = super().parse_response(allspice_client, result)
        # add "name" field to make this behave similar to users for gitea < 1.18
        # also necessary for repository-owner when org is repo owner
        if not hasattr(api_object, "name"):
            Organization._add_read_property("name", result["username"], api_object)
        return api_object

    _patchable_fields = {"description", "full_name", "location", "visibility", "website"}

    def commit(self):
        values = self.get_dirty_fields()
        args = {"name": self.name}
        self.allspice_client.requests_patch(
            Organization.API_OBJECT.format(**args), data=values
        )
        self.dirty_fields = {}

    def create_repo(
            self,
            repoName: str,
            description: str = "",
            private: bool = False,
            autoInit=True,
            gitignores: str = None,
            license: str = None,
            readme: str = "Default",
            issue_labels: str = None,
            default_branch="master",
    ):
        """Create an organization Repository

        Throws:
            AlreadyExistsException: If the Repository exists already.
            Exception: If something else went wrong.
        """
        result = self.allspice_client.requests_post(
            f"/orgs/{self.name}/repos",
            data={
                "name": repoName,
                "description": description,
                "private": private,
                "auto_init": autoInit,
                "gitignores": gitignores,
                "license": license,
                "issue_labels": issue_labels,
                "readme": readme,
                "default_branch": default_branch,
            },
        )
        if "id" in result:
            self.allspice_client.logger.info("Successfully created Repository %s " % result["name"])
        else:
            self.allspice_client.logger.error(result["message"])
            raise Exception("Repository not created... (gitea: %s)" % result["message"])
        return Repository.parse_response(self, result)

    def get_repositories(self) -> List["Repository"]:
        results = self.allspice_client.requests_get_paginated(
            Organization.ORG_REPOS_REQUEST % self.username
        )
        return [Repository.parse_response(self.allspice_client, result) for result in results]

    def get_repository(self, name) -> "Repository":
        repos = self.get_repositories()
        for repo in repos:
            if repo.name == name:
                return repo
        raise NotFoundException("Repository %s not existent in organization." % name)

    def get_teams(self) -> List["Team"]:
        results = self.allspice_client.requests_get(
            Organization.ORG_TEAMS_REQUEST % self.username
        )
        teams = [Team.parse_response(self.allspice_client, result) for result in results]
        # organisation seems to be missing using this request, so we add org manually
        for t in teams: setattr(t, "_organization", self)
        return teams

    def get_team(self, name) -> "Team":
        teams = self.get_teams()
        for team in teams:
            if team.name == name:
                return team
        raise NotFoundException("Team not existent in organization.")

    def create_team(
            self,
            name: str,
            description: str = "",
            permission: str = "read",
            can_create_org_repo: bool = False,
            includes_all_repositories: bool = False,
            units=(
                    "repo.code",
                    "repo.issues",
                    "repo.ext_issues",
                    "repo.wiki",
                    "repo.pulls",
                    "repo.releases",
                    "repo.ext_wiki",
            ),
            units_map={},
    ) -> "Team":
        """Alias for AllSpice#create_team"""
        # TODO: Move AllSpice#create_team to Organization#create_team and
        #       deprecate AllSpice#create_team.
        return self.allspice_client.create_team(
            org=self,
            name=name,
            description=description,
            permission=permission,
            can_create_org_repo=can_create_org_repo,
            includes_all_repositories=includes_all_repositories,
            units=units,
            units_map=units_map,
        )

    def get_members(self) -> List["User"]:
        results = self.allspice_client.requests_get(Organization.ORG_GET_MEMBERS % self.username)
        return [User.parse_response(self.allspice_client, result) for result in results]

    def is_member(self, username) -> bool:
        if isinstance(username, User):
            username = username.username
        try:
            # returns 204 if its ok, 404 if its not
            self.allspice_client.requests_get(
                Organization.ORG_IS_MEMBER % (self.username, username)
            )
            return True
        except:
            return False

    def remove_member(self, user: "User"):
        path = f"/orgs/{self.username}/members/{user.username}"
        self.allspice_client.requests_delete(path)

    def delete(self):
        """ Delete this Organization. Invalidates this Objects data. Also deletes all Repositories owned by the User"""
        for repo in self.get_repositories():
            repo.delete()
        self.allspice_client.requests_delete(Organization.API_OBJECT.format(name=self.username))
        self.deleted = True

    def get_heatmap(self) -> List[Tuple[datetime, int]]:
        results = self.allspice_client.requests_get(User.USER_HEATMAP % self.username)
        results = [
            (datetime.fromtimestamp(result["timestamp"]), result["contributions"])
            for result in results
        ]
        return results


class User(ApiObject):
    API_OBJECT = """/users/{name}"""  # <org>
    USER_MAIL = """/user/emails?sudo=%s"""  # <name>
    USER_PATCH = """/admin/users/%s"""  # <username>
    ADMIN_DELETE_USER = """/admin/users/%s"""  # <username>
    ADMIN_EDIT_USER = """/admin/users/{username}"""  # <username>
    USER_HEATMAP = """/users/%s/heatmap"""  # <username>

    def __init__(self, allspice_client):
        super().__init__(allspice_client)
        self._emails = []

    def __eq__(self, other):
        if not isinstance(other, User): return False
        return self.allspice_client == other.allspice_client and self.id == other.id

    def __hash__(self):
        return hash(self.allspice_client) ^ hash(self.id)

    @property
    def emails(self):
        self.__request_emails()
        return self._emails

    @classmethod
    def request(cls, allspice_client: 'AllSpice', name: str) -> "User":
        api_object = cls._request(allspice_client, {"name": name})
        return api_object

    _patchable_fields = {
        "active",
        "admin",
        "allow_create_organization",
        "allow_git_hook",
        "allow_import_local",
        "email",
        "full_name",
        "location",
        "login_name",
        "max_repo_creation",
        "must_change_password",
        "password",
        "prohibit_login",
        "website",
    }

    def commit(self, login_name: str, source_id: int = 0):
        """
        Unfortunately it is necessary to require the login name
        as well as the login source (that is not supplied when getting a user) for
        changing a user.
        Usually source_id is 0 and the login_name is equal to the username.
        """
        values = self.get_dirty_fields()
        values.update(
            # api-doc says that the "source_id" is necessary; works without though
            {"login_name": login_name, "source_id": source_id}
        )
        args = {"username": self.username}
        self.allspice_client.requests_patch(User.ADMIN_EDIT_USER.format(**args), data=values)
        self.dirty_fields = {}

    def create_repo(
            self,
            repoName: str,
            description: str = "",
            private: bool = False,
            autoInit=True,
            gitignores: str = None,
            license: str = None,
            readme: str = "Default",
            issue_labels: str = None,
            default_branch="master",
    ):
        """Create a user Repository

        Throws:
            AlreadyExistsException: If the Repository exists already.
            Exception: If something else went wrong.
        """
        result = self.allspice_client.requests_post(
            "/user/repos",
            data={
                "name": repoName,
                "description": description,
                "private": private,
                "auto_init": autoInit,
                "gitignores": gitignores,
                "license": license,
                "issue_labels": issue_labels,
                "readme": readme,
                "default_branch": default_branch,
            },
        )
        if "id" in result:
            self.allspice_client.logger.info("Successfully created Repository %s " % result["name"])
        else:
            self.allspice_client.logger.error(result["message"])
            raise Exception("Repository not created... (gitea: %s)" % result["message"])
        return Repository.parse_response(self, result)

    def get_repositories(self) -> List["Repository"]:
        """ Get all Repositories owned by this User."""
        url = f"/users/{self.username}/repos"
        results = self.allspice_client.requests_get_paginated(url)
        return [Repository.parse_response(self.allspice_client, result) for result in results]

    def get_orgs(self) -> List[Organization]:
        """ Get all Organizations this user is a member of."""
        url = f"/users/{self.username}/orgs"
        results = self.allspice_client.requests_get_paginated(url)
        return [Organization.parse_response(self.allspice_client, result) for result in results]

    def get_teams(self) -> List['Team']:
        url = f"/user/teams"
        results = self.allspice_client.requests_get_paginated(url, sudo=self)
        return [Team.parse_response(self.allspice_client, result) for result in results]

    def get_accessible_repos(self) -> List['Repository']:
        """ Get all Repositories accessible by the logged in User."""
        results = self.allspice_client.requests_get("/user/repos", sudo=self)
        return [Repository.parse_response(self, result) for result in results]

    def __request_emails(self):
        result = self.allspice_client.requests_get(User.USER_MAIL % self.login)
        # report if the adress changed by this
        for mail in result:
            self._emails.append(mail["email"])
            if mail["primary"]:
                self._email = mail["email"]

    def delete(self):
        """ Deletes this User. Also deletes all Repositories he owns."""
        self.allspice_client.requests_delete(User.ADMIN_DELETE_USER % self.username)
        self.deleted = True

    def get_heatmap(self) -> List[Tuple[datetime, int]]:
        results = self.allspice_client.requests_get(User.USER_HEATMAP % self.username)
        results = [
            (datetime.fromtimestamp(result["timestamp"]), result["contributions"])
            for result in results
        ]
        return results


class Branch(ReadonlyApiObject):

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Branch):
            return False
        return self.commit == other.commit and self.name == other.name

    def __hash__(self):
        return hash(self.commit["id"]) ^ hash(self.name)

    _fields_to_parsers = {
        # This is not a commit object
        # "commit": lambda allspice_client, c: Commit.parse_response(allspice_client, c)
    }

    @classmethod
    def request(cls, allspice_client: 'AllSpice', owner: str, repo: str, ref: str):
        return cls._request(allspice_client, {"owner": owner, "repo": repo, "ref": ref})


class Repository(ApiObject):
    API_OBJECT = """/repos/{owner}/{name}"""  # <owner>, <reponame>
    REPO_IS_COLLABORATOR = """/repos/%s/%s/collaborators/%s"""  # <owner>, <reponame>, <username>
    REPO_SEARCH = """/repos/search/%s"""  # <reponame>
    REPO_BRANCHES = """/repos/%s/%s/branches"""  # <owner>, <reponame>
    REPO_BRANCH = """/repos/{owner}/{repo}/branches/{branch}"""
    REPO_ISSUES = """/repos/{owner}/{repo}/issues"""  # <owner, reponame>
    REPO_DELETE = """/repos/%s/%s"""  # <owner>, <reponame>
    REPO_TIMES = """/repos/%s/%s/times"""  # <owner>, <reponame>
    REPO_USER_TIME = """/repos/%s/%s/times/%s"""  # <owner>, <reponame>, <username>
    REPO_COMMITS = "/repos/%s/%s/commits"  # <owner>, <reponame>
    REPO_TRANSFER = "/repos/{owner}/{repo}/transfer"
    REPO_MILESTONES = """/repos/{owner}/{repo}/milestones"""

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Repository): return False
        return self.owner == other.owner and self.name == other.name

    def __hash__(self):
        return hash(self.owner) ^ hash(self.name)

    _fields_to_parsers = {
        # dont know how to tell apart user and org as owner except form email being empty.
        "owner": lambda allspice_client, r: Organization.parse_response(allspice_client, r)
        if r["email"] == "" else User.parse_response(allspice_client, r),
        "updated_at": lambda allspice_client, t: Util.convert_time(t),
    }

    @classmethod
    def request(cls, allspice_client: 'AllSpice', owner: str, name: str):
        return cls._request(allspice_client, {"owner": owner, "name": name})

    _patchable_fields = {
        "allow_manual_merge",
        "allow_merge_commits",
        "allow_rebase",
        "allow_rebase_explicit",
        "allow_rebase_update",
        "allow_squash_merge",
        "archived",
        "autodetect_manual_merge",
        "default_branch",
        "default_delete_branch_after_merge",
        "default_merge_style",
        "description",
        "enable_prune",
        "external_tracker",
        "external_wiki",
        "has_issues",
        "has_projects",
        "has_pull_requests",
        "has_wiki",
        "ignore_whitespace_conflicts",
        "internal_tracker",
        "mirror_interval",
        "name",
        "private",
        "template",
        "website",
    }

    def commit(self):
        values = self.get_dirty_fields()
        args = {"owner": self.owner.username, "name": self.name}
        self.allspice_client.requests_patch(self.API_OBJECT.format(**args), data=values)
        self.dirty_fields = {}

    def get_branches(self) -> List['Branch']:
        """Get all the Branches of this Repository."""
        results = self.allspice_client.requests_get(
            Repository.REPO_BRANCHES % (self.owner.username, self.name)
        )
        return [Branch.parse_response(self.allspice_client, result) for result in results]

    def get_branch(self, name: str) -> 'Branch':
        """Get a specific Branch of this Repository."""
        result = self.allspice_client.requests_get(
            Repository.REPO_BRANCH.format(owner=self.owner.username, repo=self.name, branch=name)
        )
        return Branch.parse_response(self.allspice_client, result)


    def add_branch(self, create_from: Branch, newname: str) -> "Branch":
        """Add a branch to the repository"""
        # Note: will only work with gitea 1.13 or higher!
        data = {"new_branch_name": newname, "old_branch_name": create_from.name}
        result = self.allspice_client.requests_post(
            Repository.REPO_BRANCHES % (self.owner.username, self.name), data=data
        )
        return Branch.parse_response(self.allspice_client, result)

    def get_issues(self) -> List["Issue"]:
        """Get all Issues of this Repository (open and closed)"""
        return self.get_issues_state(Issue.OPENED) + self.get_issues_state(Issue.CLOSED)

    def get_commits(self) -> List["Commit"]:
        """Get all the Commits of this Repository."""
        try:
            results = self.allspice_client.requests_get_paginated(
                Repository.REPO_COMMITS % (self.owner.username, self.name)
            )
        except ConflictException as err:
            logging.warning(err)
            logging.warning(
                "Repository %s/%s is Empty" % (self.owner.username, self.name)
            )
            results = []
        return [Commit.parse_response(self.allspice_client, result) for result in results]

    def get_issues_state(self, state) -> List["Issue"]:
        """Get issues of state Issue.open or Issue.closed of a repository."""
        assert state in [Issue.OPENED, Issue.CLOSED]
        issues = []
        data = {"state": state}
        results = self.allspice_client.requests_get_paginated(
            Repository.REPO_ISSUES.format(owner=self.owner.username, repo=self.name), params=data
        )
        for result in results:
            issue = Issue.parse_response(self.allspice_client, result)
            # adding data not contained in the issue answer
            Issue._add_read_property("repo", self, issue)
            Issue._add_read_property("owner", self.owner, issue)
            issues.append(issue)
        return issues

    def get_times(self):
        results = self.allspice_client.requests_get(
            Repository.REPO_TIMES % (self.owner.username, self.name)
        )
        return results

    def get_user_time(self, username) -> float:
        if isinstance(username, User):
            username = username.username
        results = self.allspice_client.requests_get(
            Repository.REPO_USER_TIME % (self.owner.username, self.name, username)
        )
        time = sum(r["time"] for r in results)
        return time

    def get_full_name(self) -> str:
        return self.owner.username + "/" + self.name

    def create_issue(self, title, assignees=frozenset(), description="") -> ApiObject:
        data = {
            "assignees": assignees,
            "body": description,
            "closed": False,
            "title": title,
        }
        result = self.allspice_client.requests_post(
            Repository.REPO_ISSUES.format(owner=self.owner.username, repo=self.name), data=data
        )
        return Issue.parse_response(self.allspice_client, result)

    def create_milestone(self, title: str, description: str, due_date: str = None, state: str = "open") -> "Milestone":
        url = Repository.REPO_MILESTONES.format(owner=self.owner.username, repo=self.name)
        data = {"title": title, "description": description, "state": state}
        if due_date: data["due_date"] = due_date
        result = self.allspice_client.requests_post(url, data=data)
        return Milestone.parse_response(self.allspice_client, result)

    def create_gitea_hook(self, hook_url: str, events: List[str]):
        url = f"/repos/{self.owner.username}/{self.name}/hooks"
        data = {
            "type": "gitea",
            "config": {"content_type": "json", "url": hook_url},
            "events": events,
            "active": True,
        }
        return self.allspice_client.requests_post(url, data=data)

    def list_hooks(self):
        url = f"/repos/{self.owner.username}/{self.name}/hooks"
        return self.allspice_client.requests_get(url)

    def delete_hook(self, id: str):
        url = f"/repos/{self.owner.username}/{self.name}/hooks/{id}"
        self.allspice_client.requests_delete(url)

    def is_collaborator(self, username) -> bool:
        if isinstance(username, User):
            username = username.username
        try:
            # returns 204 if its ok, 404 if its not
            self.allspice_client.requests_get(
                Repository.REPO_IS_COLLABORATOR
                % (self.owner.username, self.name, username)
            )
            return True
        except:
            return False

    def get_users_with_access(self) -> Sequence[User]:
        url = f"/repos/{self.owner.username}/{self.name}/collaborators"
        response = self.allspice_client.requests_get(url)
        collabs = [User.parse_response(self.allspice_client, user) for user in response]
        if isinstance(self.owner, User):
            return collabs + [self.owner]
        else:
            # owner must be org
            teams = self.owner.get_teams()
            for team in teams:
                team_repos = team.get_repos()
                if self.name in [n.name for n in team_repos]:
                    collabs += team.get_members()
            return collabs

    def remove_collaborator(self, user_name: str):
        url = f"/repos/{self.owner.username}/{self.name}/collaborators/{user_name}"
        self.allspice_client.requests_delete(url)

    def transfer_ownership(self, new_owner: Union["User", "Organization"], new_teams: Set["Team"] = frozenset()):
        url = Repository.REPO_TRANSFER.format(owner=self.owner.username, repo=self.name)
        data = {"new_owner": new_owner.username}
        if isinstance(new_owner, Organization):
            new_team_ids = [team.id for team in new_teams if team in new_owner.get_teams()]
            data["team_ids"] = new_team_ids
        self.allspice_client.requests_post(url, data=data)
        # TODO: make sure this instance is either updated or discarded

    def get_git_content(
            self: str = None,
            ref: Optional["Ref"] = None,
            commit: "Commit" = None
    ) -> List["Content"]:
        """https://hub.allspice.io/api/swagger#/repository/repoGetContentsList

        :param ref: branch or commit to get content from
        :param commit: commit to get content from (deprecated)
        """
        url = f"/repos/{self.owner.username}/{self.name}/contents"
        data = Util.data_params_for_ref(ref or commit)

        result = [Content.parse_response(self.allspice_client, f) for f in self.allspice_client.requests_get(url, data)]
        return result

    def get_file_content(
            self,
            content: "Content",
            ref: "Ref" = None,
            commit: "Commit" = None,
    ) -> Union[str, List["Content"]]:
        """https://hub.allspice.io/api/swagger#/repository/repoGetContents"""
        url = f"/repos/{self.owner.username}/{self.name}/contents/{content.path}"
        data = Util.data_params_for_ref(ref or commit)

        if content.type == Content.FILE:
            return self.allspice_client.requests_get(url, data)["content"]
        else:
            return [Content.parse_response(self.allspice_client, f) for f in self.allspice_client.requests_get(url, data)]

    def get_generated_json(self, content: Union["Content", str], ref: Optional["Ref"] = None) -> dict:
        """
        Get the json blob for a cad file if it exists, otherwise enqueue
        a new job and return a 503 status.

        Note: This is still experimental and not yet recommended for
        critical applications.

        See https://hub.allspice.io/api/swagger#/repository/repoGetAllSpiceJSON
        """

        if isinstance(content, Content):
            content = content.path

        url = f"/repos/{self.owner.username}/{self.name}/allspice_generated/json/{content}"
        data = Util.data_params_for_ref(ref)
        return self.allspice_client.requests_get(url, data)

    def get_generated_svg(self, content: Union["Content", str], ref: Optional[str] = None) -> bytes:
        """
        Get the svg blob for a cad file if it exists, otherwise enqueue
        a new job and return a 503 status.

        Note: This is still experimental and not yet recommended for
        critical applications.

        See https://hub.allspice.io/api/swagger#/repository/repoGetAllSpiceSVG
        """

        if isinstance(content, Content):
            content = content.path

        url = f"/repos/{self.owner.username}/{self.name}/allspice_generated/svg/{content}"
        data = {"ref": ref} if ref else {}
        return self.allspice_client.requests_get_raw(url, data)

    def create_file(self, file_path: str, content: str, data: dict = None):
        """https://hub.allspice.io/api/swagger#/repository/repoCreateFile"""
        if not data:
            data = {}
        url = f"/repos/{self.owner.username}/{self.name}/contents/{file_path}"
        data.update({"content": content})
        return self.allspice_client.requests_post(url, data)

    def change_file(self, file_path: str, file_sha: str, content: str, data: dict = None):
        """https://hub.allspice.io/api/swagger#/repository/repoCreateFile"""
        if not data:
            data = {}
        url = f"/repos/{self.owner.username}/{self.name}/contents/{file_path}"
        data.update({"sha": file_sha, "content": content})
        return self.allspice_client.requests_put(url, data)

    def delete(self):
        self.allspice_client.requests_delete(
            Repository.REPO_DELETE % (self.owner.username, self.name)
        )
        self.deleted = True


class Milestone(ApiObject):
    API_OBJECT = """/repos/{owner}/{repo}/milestones/{number}"""  # <owner, repo>

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Milestone): return False
        return self.allspice_client == other.allspice_client and self.id == other.id

    def __hash__(self):
        return hash(self.allspice_client) ^ hash(self.id)

    _fields_to_parsers = {
        "closed_at": lambda allspice_client, t: Util.convert_time(t),
        "due_on": lambda allspice_client, t: Util.convert_time(t),
    }

    _patchable_fields = {
        "allow_merge_commits",
        "allow_rebase",
        "allow_rebase_explicit",
        "allow_squash_merge",
        "archived",
        "default_branch",
        "description",
        "has_issues",
        "has_pull_requests",
        "has_wiki",
        "ignore_whitespace_conflicts",
        "name",
        "private",
        "website",
    }

    @classmethod
    def request(cls, allspice_client: 'AllSpice', owner: str, repo: str, number: str):
        return cls._request(allspice_client, {"owner": owner, "repo": repo, "number": number})


class Comment(ApiObject):

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Comment): return False
        return self.repo == other.repo and self.id == other.id

    def __hash__(self):
        return hash(self.repo) ^ hash(self.id)

    _fields_to_parsers = {
        "user": lambda allspice_client, r: User.parse_response(allspice_client, r),
        "created_at": lambda allspice_client, t: Util.convert_time(t),
        "updated_at": lambda allspice_client, t: Util.convert_time(t),
    }


class Commit(ReadonlyApiObject):

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    _fields_to_parsers = {
        # NOTE: api may return None for commiters that are no allspice users
        "author": lambda allspice_client, u: User.parse_response(allspice_client, u) if u else None
    }

    def __eq__(self, other):
        if not isinstance(other, Commit): return False
        return self.sha == other.sha

    def __hash__(self):
        return hash(self.sha)

    @classmethod
    def parse_response(cls, allspice_client, result) -> 'Commit':
        commit_cache = result["commit"]
        api_object = cls(allspice_client)
        cls._initialize(allspice_client, api_object, result)
        # inner_commit for legacy reasons
        Commit._add_read_property("inner_commit", commit_cache, api_object)
        return api_object


class Issue(ApiObject):
    API_OBJECT = """/repos/{owner}/{repo}/issues/{index}"""  # <owner, repo, index>
    GET_TIME = """/repos/%s/%s/issues/%s/times"""  # <owner, repo, index>
    GET_COMMENTS = """/repos/%s/%s/issues/comments"""
    CREATE_ISSUE = """/repos/{owner}/{repo}/issues"""

    OPENED = "open"
    CLOSED = "closed"

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Issue): return False
        return self.repo == other.repo and self.id == other.id

    def __hash__(self):
        return hash(self.repo) ^ hash(self.id)

    _fields_to_parsers = {
        "milestone": lambda allspice_client, m: Milestone.parse_response(allspice_client, m),
        "user": lambda allspice_client, u: User.parse_response(allspice_client, u),
        "assignee": lambda allspice_client, u: User.parse_response(allspice_client, u),
        "assignees": lambda allspice_client, us: [User.parse_response(allspice_client, u) for u in us],
        "state": lambda allspice_client, s: Issue.CLOSED if s == "closed" else Issue.OPENED,
        # Repository in this request is just a "RepositoryMeta" record, thus request whole object
        "repository": lambda allspice_client, r: Repository.request(allspice_client, r["owner"], r["name"])
    }

    _parsers_to_fields = {
        "milestone": lambda m: m.id,
    }

    _patchable_fields = {
        "assignee",
        "assignees",
        "body",
        "due_date",
        "milestone",
        "state",
        "title",
    }

    def commit(self):
        values = self.get_dirty_fields()
        args = {"owner": self.repository.owner.username, "repo": self.repository.name, "index": self.number}
        self.allspice_client.requests_patch(Issue.API_OBJECT.format(**args), data=values)
        self.dirty_fields = {}

    @classmethod
    def request(cls, allspice_client: 'AllSpice', owner: str, repo: str, number: str):
        api_object = cls._request(allspice_client, {"owner": owner, "repo": repo, "index": number})
        return api_object

    @classmethod
    def create_issue(cls, allspice_client: 'AllSpice', repo: Repository, title: str, body: str = ""):
        args = {"owner": repo.owner.username, "repo": repo.name}
        data = {"title": title, "body": body}
        result = allspice_client.requests_post(Issue.CREATE_ISSUE.format(**args), data=data)
        return Issue.parse_response(allspice_client, result)

    def get_time_sum(self, user: User) -> int:
        results = self.allspice_client.requests_get(
            Issue.GET_TIME % (self.owner.username, self.repo.name, self.number)
        )
        return sum(
            result["time"]
            for result in results
            if result and result["user_id"] == user.id
        )

    def get_times(self) -> Optional[Dict]:
        return self.allspice_client.requests_get(
            Issue.GET_TIME % (self.owner.username, self.repository.name, self.number)
        )

    def delete_time(self, time_id: str):
        path = f"/repos/{self.owner.username}/{self.repository.name}/issues/{self.number}/times/{time_id}"
        self.allspice_client.requests_delete(path)

    def add_time(self, time: int, created: str = None, user_name: User = None):
        path = f"/repos/{self.owner.username}/{self.repository.name}/issues/{self.number}/times"
        self.allspice_client.requests_post(
            path, data={"created": created, "time": int(time), "user_name": user_name}
        )

    def get_comments(self) -> List[ApiObject]:
        results = self.allspice_client.requests_get(
            Issue.GET_COMMENTS % (self.owner.username, self.repo.name)
        )
        allProjectComments = [
            Comment.parse_response(self.allspice_client, result) for result in results
        ]
        # Comparing the issue id with the URL seems to be the only (!) way to get to the comments of one issue
        return [
            comment
            for comment in allProjectComments
            if comment.issue_url.endswith("/" + str(self.number))
        ]


class Team(ApiObject):
    API_OBJECT = """/teams/{id}"""  # <id>
    ADD_REPO = """/teams/%s/repos/%s/%s"""  # <id, org, repo>
    TEAM_DELETE = """/teams/%s"""  # <id>
    GET_MEMBERS = """/teams/%s/members"""  # <id>
    GET_REPOS = """/teams/%s/repos"""  # <id>

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Team): return False
        return self.organization == other.organization and self.id == other.id

    def __hash__(self):
        return hash(self.organization) ^ hash(self.id)

    _fields_to_parsers = {
        "organization": lambda allspice_client, o: Organization.parse_response(allspice_client, o)
    }

    _patchable_fields = {
        "can_create_org_repo",
        "description",
        "includes_all_repositories",
        "name",
        "permission",
        "units",
        "units_map",
    }

    @classmethod
    def request(cls, allspice_client: 'AllSpice', id: int):
        return cls._request(allspice_client, {"id": id})

    def commit(self):
        values = self.get_dirty_fields()
        args = {"id": self.id}
        self.allspice_client.requests_patch(self.API_OBJECT.format(**args), data=values)
        self.dirty_fields = {}

    def add_user(self, user: User):
        """https://hub.allspice.io/api/swagger#/organization/orgAddTeamMember"""
        url = f"/teams/{self.id}/members/{user.login}"
        self.allspice_client.requests_put(url)

    def add_repo(self, org: Organization, repo: Repository):
        self.allspice_client.requests_put(Team.ADD_REPO % (self.id, org, repo.name))

    def get_members(self):
        """ Get all users assigned to the team. """
        results = self.allspice_client.requests_get(Team.GET_MEMBERS % self.id)
        return [User.parse_response(self.allspice_client, result) for result in results]

    def get_repos(self):
        """ Get all repos of this Team."""
        results = self.allspice_client.requests_get(Team.GET_REPOS % self.id)
        return [Repository.parse_response(self.allspice_client, result) for result in results]

    def delete(self):
        self.allspice_client.requests_delete(Team.TEAM_DELETE % self.id)
        self.deleted = True

    def remove_team_member(self, user_name: str):
        url = f"/teams/{self.id}/members/{user_name}"
        self.allspice_client.requests_delete(url)


class Content(ReadonlyApiObject):
    FILE = "file"

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Team): return False
        return self.repo == self.repo and self.sha == other.sha and self.name == other.name

    def __hash__(self):
        return hash(self.repo) ^ hash(self.sha) ^ hash(self.name)

Ref = Union[Branch, Commit, str]

class Util:
    @staticmethod
    def convert_time(time: str) -> datetime:
        """ Parsing of strange Gitea time format ("%Y-%m-%dT%H:%M:%S:%z" but with ":" in time zone notation)"""
        try:
            return datetime.strptime(time[:-3] + "00", "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            return datetime.strptime(time[:-3] + "00", "%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def data_params_for_ref(ref: Optional[Ref]) -> Dict:
        """
        Given a "ref", returns a dict with the ref parameter for the API call.

        If the ref is None, returns an empty dict. You can pass this to the API
        directly.
        """

        if isinstance(ref, Branch):
            return {"ref": ref.name}
        elif isinstance(ref, Commit):
            return {"ref": ref.sha}
        elif ref:
            return {"ref": ref}
        else:
            return {}
