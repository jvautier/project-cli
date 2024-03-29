#!/usr/bin/env python3

import argparse
import os
import urllib

import requests
import yaml


class GithubCli:
    def __init__(self, **kwargs):
        self._api_url = os.environ.get("GITHUB_API_URL", "https://api.github.com")
        self._username = os.environ.get("GITHUB_API_USERNAME", None)
        self._api_key = os.environ.get("GITHUB_API_TOKEN", None)

    def request(self, method, url, **kwargs):
        request_parameters = {}
        request_parameters["url"] = self._api_url + url.replace("//", "/")
        request_parameters["url"] = request_parameters["url"].format(**kwargs)

        request_parameters["headers"] = {
            "Accept": "application/vnd.github.mercy-preview+json",
            "Content-type": "application/json",
        }

        request_parameters["data"] = kwargs.get("data", None)
        request_parameters["json"] = kwargs.get("json", None)
        request_parameters["timeout"] = kwargs.get("timeout", 30.0)

        if not self._username and not self._api_key:
            return requests.request(method=method, **request_parameters)
        else:
            return requests.request(
                auth=(self._username, self._api_key),
                method=method,
                **request_parameters
            )

    def update_metas(self, **kwargs):
        metas = yaml.load(open(".github.yml"), Loader=yaml.FullLoader)
        project_name = metas["fullname"]

        json = {"description": metas["description"]}

        json.update(metas["github"])
        kwargs["json"] = json
        print(kwargs)
        self.request("PATCH", "/repos/" + project_name, **kwargs)

        json = {"names": metas["tags"]}
        kwargs["json"] = json
        self.request("PUT", "/repos/" + project_name + "/topics", **kwargs)


class GitlabCli:
    def __init__(self, **kwargs):
        self._api_url = os.environ.get("GITLAB_API_URL", "https://gitlab.com/api/v4")
        self._username = os.environ.get("GITLAB_API_USERNAME", None)
        self._api_key = os.environ.get("GITLAB_API_TOKEN", None)

    def request(self, method, url, **kwargs):
        request_parameters = {}
        request_parameters["url"] = self._api_url + url.replace("//", "/")
        request_parameters["url"] = request_parameters["url"].format(**kwargs)

        request_parameters["headers"] = kwargs.get(
            "headers",
            {"Accept": "application/json", "Content-type": "application/json"},
        )

        request_parameters["headers"]["PRIVATE-TOKEN"] = self._api_key
        request_parameters["data"] = kwargs.get("data", None)
        request_parameters["json"] = kwargs.get("json", None)
        request_parameters["timeout"] = kwargs.get("timeout", 30.0)
        request_parameters["stream"] = kwargs.get("stream", False)
        request_parameters["files"] = kwargs.get("files", None)

        return requests.request(method=method, **request_parameters)

    def update_metas(self, **kwargs):
        metas = yaml.load(open(".gitlab.yml"), Loader=yaml.FullLoader)
        project_name = metas["fullname"]
        project_name = urllib.parse.quote_plus(project_name)
        print(metas)
        json = {
            "description": metas["description"],
            "tag_list": metas["tags"],
        }
        json.update(metas["gitlab"])
        kwargs["json"] = json
        self.request("PUT", "/projects/" + project_name, **kwargs)

        if metas.get("avatar", None):
            files = {"avatar": open(metas["avatar"], "rb")}
            kwargs["files"] = files
            kwargs["headers"] = {}
            self.request("PUT", "/projects/" + project_name, **kwargs)


class ProjectCli:
    def call(self, **kwargs):
        if os.path.isfile(".gitlab.yml"):
            cli = GitlabCli()
        if os.path.isfile(".github.yml"):
            cli = GithubCli()

        return cli.update_metas()

    def parse(self):
        self._parser = parser = argparse.ArgumentParser(description="project cli")
        args = parser.parse_args()
        args_for_func = vars(args)
        self.call(**args_for_func)


def main():
    ctl = ProjectCli()
    ctl.parse()


if __name__ == "__main__":
    main()
