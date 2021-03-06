#!/bin/bash
pandoc -s -o ../../Community/contribute.html ../../Community/contribute.md -H head.html -B nav.html -A footer.html --css ../../CSS/page.css
pandoc -s -o ../../Community/council.html ../../Community/council.md -H head.html -B nav.html -A footer.html --css ../../CSS/page.css
pandoc -s -o ../../Community/roadmap.html ../../Community/roadmap.md -H head.html -B nav.html -A footer.html --css ../../CSS/page.css
pandoc -s -o ../../Community/initiatives.html ../../Community/initiatives.md -H head.html -B nav.html -A footer.html --css ../../CSS/page.css
pandoc -s -o ../../Catalog/library_criteria.html ../../Catalog/library_criteria.md -H head.html -B nav.html -A footer.html --css ../../CSS/page.css
