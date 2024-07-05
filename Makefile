
.PHONY: shell
shell:
	docker build -t clerk-sdk-python . 
	docker run --rm -it -v $PWD:/app clerk-sdk-python bash
