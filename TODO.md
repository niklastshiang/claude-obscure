# To do

- [ ] **Add my proofreading (Lektorat) skills** (owner, 2026-11-16): move them into `skills/<name>/SKILL.md`, one folder per skill, in the same format as `owner-led-projects`; list each in the README's table. The owner provides them.

- [ ] **Load it as a plugin, like addyosmani/agent-skills** (owner, 2026-11-16): agent-skills can be installed with
  `/plugin marketplace add addyosmani/agent-skills` and `/plugin install agent-skills@addy-agent-skills`,
  through `.claude-plugin/plugin.json` (name, version, licence, `"skills": "./skills"`) and
  `.claude-plugin/marketplace.json` (the marketplace and its plugins, source `github`).
  - Do the same here, so `/plugin marketplace add niklastshiang/claude-skills` installs my skills on any machine.
  - Open: whether my marketplace also lists agent-skills as a second plugin (one `add` installs both) or only mine with a note to add Addy's; how plugin versions are numbered (Day 1 rule of `owner-led-projects`); whether `install.sh` stays for cloud environments or the setup script switches to the plugin.
  - Check the current plugin and marketplace format in the Claude Code docs first, not from memory.
  - Checked 2026-11-16 (code.claude.com/docs/en/plugins/marketplace-reference.md): one repository can be marketplace and plugin at once (plugin source `"./"`); a marketplace can list plugins from other repositories (`{"source": "github", "repo": ..., "sha": <40 characters>}`); `agent-skills` is a reserved marketplace name; without a `version` field every new commit counts as an update; cloud sessions on claude.ai/code do not install plugins from settings, so cloud environments keep using `install.sh`.
  - Open decisions (owner: not now, 2026-11-16), with Claude's recommendation: list agent-skills and clarity in this marketplace, pinned to the commits `install.sh` uses (yes); leave out `version` (yes); keep `install.sh` for cloud environments (yes); names: marketplace `niklastshiang`, plugin `owner-led-projects`.
