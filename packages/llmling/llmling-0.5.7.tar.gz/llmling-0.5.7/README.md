# LLMling

[![PyPI License](https://img.shields.io/pypi/l/llmling.svg)](https://pypi.org/project/llmling/)
[![Package status](https://img.shields.io/pypi/status/llmling.svg)](https://pypi.org/project/llmling/)
[![Daily downloads](https://img.shields.io/pypi/dd/llmling.svg)](https://pypi.org/project/llmling/)
[![Weekly downloads](https://img.shields.io/pypi/dw/llmling.svg)](https://pypi.org/project/llmling/)
[![Monthly downloads](https://img.shields.io/pypi/dm/llmling.svg)](https://pypi.org/project/llmling/)
[![Distribution format](https://img.shields.io/pypi/format/llmling.svg)](https://pypi.org/project/llmling/)
[![Wheel availability](https://img.shields.io/pypi/wheel/llmling.svg)](https://pypi.org/project/llmling/)
[![Python version](https://img.shields.io/pypi/pyversions/llmling.svg)](https://pypi.org/project/llmling/)
[![Implementation](https://img.shields.io/pypi/implementation/llmling.svg)](https://pypi.org/project/llmling/)
[![Releases](https://img.shields.io/github/downloads/phil65/llmling/total.svg)](https://github.com/phil65/llmling/releases)
[![Github Contributors](https://img.shields.io/github/contributors/phil65/llmling)](https://github.com/phil65/llmling/graphs/contributors)
[![Github Discussions](https://img.shields.io/github/discussions/phil65/llmling)](https://github.com/phil65/llmling/discussions)
[![Github Forks](https://img.shields.io/github/forks/phil65/llmling)](https://github.com/phil65/llmling/forks)
[![Github Issues](https://img.shields.io/github/issues/phil65/llmling)](https://github.com/phil65/llmling/issues)
[![Github Issues](https://img.shields.io/github/issues-pr/phil65/llmling)](https://github.com/phil65/llmling/pulls)
[![Github Watchers](https://img.shields.io/github/watchers/phil65/llmling)](https://github.com/phil65/llmling/watchers)
[![Github Stars](https://img.shields.io/github/stars/phil65/llmling)](https://github.com/phil65/llmling/stars)
[![Github Repository size](https://img.shields.io/github/repo-size/phil65/llmling)](https://github.com/phil65/llmling)
[![Github last commit](https://img.shields.io/github/last-commit/phil65/llmling)](https://github.com/phil65/llmling/commits)
[![Github release date](https://img.shields.io/github/release-date/phil65/llmling)](https://github.com/phil65/llmling/releases)
[![Github language count](https://img.shields.io/github/languages/count/phil65/llmling)](https://github.com/phil65/llmling)
[![Github commits this week](https://img.shields.io/github/commit-activity/w/phil65/llmling)](https://github.com/phil65/llmling)
[![Github commits this month](https://img.shields.io/github/commit-activity/m/phil65/llmling)](https://github.com/phil65/llmling)
[![Github commits this year](https://img.shields.io/github/commit-activity/y/phil65/llmling)](https://github.com/phil65/llmling)
[![Package status](https://codecov.io/gh/phil65/llmling/branch/main/graph/badge.svg)](https://codecov.io/gh/phil65/llmling/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyUp](https://pyup.io/repos/github/phil65/llmling/shield.svg)](https://pyup.io/repos/github/phil65/llmling/)

[Read the documentation!](https://phil65.github.io/llmling/)


```yaml
# Root level: Config
version: "1.0"
global_settings:  # GlobalSettings
  timeout: 30
  max_retries: 3
  temperature: 0.7

context_processors:  # dict[str, ProcessorConfig]
  processor1:
    type: function
    import_path: "utils.clean_text"
  processor2:
    type: template
    template: "{{ content }}\n---"

resources:  # dict[str, Resource(PathResource | TextResource | CLIResource)]
  guidelines:
    type: path  # PathResource
    path: "./guide.md"
    description: "Guide"
    processors:  # list[ProcessingStep]
      - name: processor1
        keyword_args: {key: "value"}

  prompt:
    type: text  # TextResource
    content: "System prompt"
    description: "Basic prompt"

  git_diff:
    type: cli  # CLIResource
    command: "git diff"
    description: "Changes"

resource_groups:  # dict[str, list[str]]
  review_resources:
    - guidelines
    - prompt
