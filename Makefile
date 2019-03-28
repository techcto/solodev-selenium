clean:
	rm -rf build build.zip
	rm -rf __pycache__

fetch:
	mkdir -p bin/
	curl -SL https://chromedriver.storage.googleapis.com/2.32/chromedriver_linux64.zip > drivers/chromedriver.zip
	unzip drivers/chromedriver.zip -d bin/
	curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-29/stable-headless-chromium-amazonlinux-2017-03.zip > drivers/headless-chromium.zip
	unzip drivers/headless-chromium.zip -d bin/
	rm -rf headless-chromium.zip chromedriver.zip

docker-build:
	docker-compose build

build: clean fetch
	mkdir build
	cp -r src build/.
	cp -r bin build/.
	cp -r lib build/.
	pip install -r requirements.txt -t build/lib/.
	cd build; zip -9qr build.zip .
	cp build/build.zip .
	rm -rf build

run: docker-build
	docker-compose run lambda src.lambda_function.lambda_handler