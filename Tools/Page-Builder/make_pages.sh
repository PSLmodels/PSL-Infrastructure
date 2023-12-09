#!/bin/bash
pandoc --template=template.html -o ../../Community/contribute.html ../../Community/contribute.md
pandoc --template=template.html -o ../../Community/council.html ../../Community/council.md
pandoc --template=template.html -o ../../Community/roadmap.html ../../Community/roadmap.md
pandoc --template=template.html -o ../../Community/initiatives.html ../../Community/initiatives.md
pandoc --template=template.html -o ../../Catalog/library_criteria.html ../../Catalog/library_criteria.md