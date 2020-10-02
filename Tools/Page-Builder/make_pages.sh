#!/bin/bash

pandoc -s -o ../../Community/contribute.html ../../Community/contribute.md -H head.html -B nav.html
pandoc -s -o ../../Community/council.html ../../Community/council.md -H head.html -B nav.html
pandoc -s -o ../../Community/roadmap.html ../../Community/roadmap.md -H head.html -B nav.html
pandoc -s -o ../../Catalog/library_criteria.html ../../Catalog/library_criteria.md -H head.html -B nav.html