<a id="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  </a>
  ```
  eee
  ```
  <h3 align="center">SunnyCemetery</h3>
  
,---.                    ,---.               |                   
`---..   .,---.,---.,   .|    ,---.,-.-.,---.|--- ,---.,---.,   .
    ||   ||   ||   ||   ||    |---'| | ||---'|    |---'|    |   |
`---'`---'`   '`   '`---|`---'`---'` ' '`---'`---'`---'`    `---|
                    `---'                                   `---'

  <p align="center">
    A fully featured Unique Domain Crawler with openVAS and nuclei integration for vulnerability scaning!

</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
          <li><a href="#usage">Usage</a></li>
          <li><a href="#roadmap">Roadmap</a></li>
          <li><a href="#contributing">Contributing</a></li>
      </ul>
    </li>
  </ol>
</details>






<!-- GETTING STARTED -->
## Getting Started

After installing the prerequisites follow the installation instructions.

### Prerequisites

install the packages manualy or with requirements.txt
```
requests==2.32.3
beautifulsoup4==4.13.0
urllib3<2.0.0
```
* 
  ```sh
   pip install -r requirements.txt
  ```

## Usage
```sh
positional arguments:
  url                   The starting URL to crawl (optional if using --url_file)

options:
  -h, --help            show this help message and exit
  --url_file URL_FILE   Path to a file containing multiple URLs (one per line)
  --depth DEPTH         Maximum depth to crawl (default: 2)
  --delay DELAY         Delay between requests in seconds (default: 0.1)
  --max_workers MAX_WORKERS
                        Number of concurrent workers for crawling (default: 5)
  --proxy PROXY         Path to the proxy file (e.g., proxies.txt)
  --proxy_rotation_interval PROXY_ROTATION_INTERVAL
                        Number of requests before rotating the proxy (default: 10)
  --timeout_limit TIMEOUT_LIMIT
                        Maximum number of timeouts before skipping a URL (default: 1)
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add roatating proxys
- [ ] Add interactive tree
- [ ] Add following robots.txt 
- [ ] Add distributed crawling across multiple machines
- [ ] Add "components" to easily filter results
- [ ] Web UI Support
    - [ ] OpenVas





<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch 
3. Commit your Changes
4. Push to the Branch 
5. Open a Pull Request


<!-- LICENSE -->
<!-- ## License

Distributed under the MIT License. See `LICENSE.txt` for more information. -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>







