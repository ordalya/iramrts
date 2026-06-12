# What's in this repo? 👀
>IRaMuTeQ + RTS = IRaMRTS

* **data:** well... _data_

  * **iramuteq:** IRaMuTeQ processed data

  * **raw:** raw and semi-IRaMuTeQ-formatted data _(some script shenanigans was used on it)_

    * **comments:** Instagram comments data _(scraped from a sample of @rtsarchives & @rtsinfo posts, a thousand from each)_

    * **descriptions:** Instagram descriptions data _(scraped from a sample of @rtsarchives & @rtsinfo posts, a thousand from each)_

    * **full:** merges of comments and descriptions data _(mainly used to complete the IRaMuTeQ default 'lexique_fr.txt' dictionnary)_

* **scripts:** python scripts to format "raw" scraped data to IRaMuTeQ format

* **config.py:** file path manager for .py scripts _(when it comes to paths, relative > absolute)_
