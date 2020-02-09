.PHONY: preview

preview:
	docker run -it --rm \
		-v "$(shell pwd)":/usr/src/app \
		-p "4000:4000" \
		starefossen/github-pages
