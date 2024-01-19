<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
</p>
<p align="center">
    <h1 align="center">VIDEO_ANALYZER</h1>
</p>
<p align="center">
    <em><code>► INSERT-TEXT-HERE</code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/thomas-chu123/video_analyzer?style=default&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/thomas-chu123/video_analyzer?style=default&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/thomas-chu123/video_analyzer?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/thomas-chu123/video_analyzer?style=default&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<hr>

##  Quick Links

> - [ Overview](#-overview)
> - [ Features](#-features)
> - [ Repository Structure](#-repository-structure)
> - [ Modules](#-modules)
> - [ Getting Started](#-getting-started)
>   - [ Installation](#-installation)
>   - [ Running video_analyzer](#-running-video_analyzer)
>   - [ Tests](#-tests)
> - [ Project Roadmap](#-project-roadmap)
> - [ Contributing](#-contributing)
> - [ License](#-license)
> - [ Acknowledgments](#-acknowledgments)

---

##  Overview

<code>►
The tool is used on Windows platform to monitor the IPTV stream quality (packet loss, jitter, delay, etc) 
by using Tshark (Wireshark command line interface) to capture 60 second RTP data and analysing them.
The tool will also send IGMPv3 join the join the multicast channel before capture the IPTV data.
The GUI interface (tinker module) will help you to configure the required setting.
After the analysing, the analyzed result will be exported to excel file to monitor the long term quality on IPTV channel.</code>

---

##  Features

<code>► INSERT-TEXT-HERE</code>

---

##  Repository Structure

```sh
└── video_analyzer/
    ├── default.txt
    └── video_check.py
```

---

##  Modules

<details closed><summary>.</summary>

| File                                                                                         | Summary                         |
| ---                                                                                          | ---                             |
| [video_check.py](https://github.com/thomas-chu123/video_analyzer/blob/master/video_check.py) | <code>► INSERT-TEXT-HERE</code> |
| [default.txt](https://github.com/thomas-chu123/video_analyzer/blob/master/default.txt)       | <code>► INSERT-TEXT-HERE</code> |

</details>

---

##  Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python**: `version x.y.z`
* 1. Python3
2. Tshark (make sure /tshark is included in the subdirectory)
3. xlsxwriter (python module running with source code)
4. netifaces (python module running with source code)

###  Installation

1. Clone the video_analyzer repository:

```sh
git clone https://github.com/thomas-chu123/video_analyzer
```

2. Change to the project directory:

```sh
cd video_analyzer
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

###  Running video_analyzer

Use the following command to run video_analyzer:

```sh
python main.py
```
1. Use video_check.exe to execute the tool

###  Tests

To execute tests, run:

```sh
pytest
```

---

##  Project Roadmap

- [X] `► INSERT-TASK-1`
- [ ] `► INSERT-TASK-2`
- [ ] `► ...`

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github/thomas-chu123/video_analyzer/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github/thomas-chu123/video_analyzer/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github/thomas-chu123/video_analyzer/issues)**: Submit bugs found or log feature requests for Video_analyzer.

<details closed>
    <summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone https://github.com/thomas-chu123/video_analyzer
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-quick-links)

---

