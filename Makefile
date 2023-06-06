
docker-build:
	docker build -t standmup .

docker-run:
	docker run --name standmup \
 			-it --rm -p 5000:5000 \
			-e FLASK_DB_PASS="$(FLASK_DB_PASS)" \
			-e FLASK_DB_HOST="$(FLASK_DB_HOST)" \
			-e FLASK_DB_USER=$(FLASK_DB_USER) \
			-e FLASK_YOUTUBE_API_KEY=$(FLASK_YOUTUBE_API_KEY) \
			-e FLASK_YOUTUBE_PLAYLIST=$(FLASK_YOUTUBE_PLAYLIST) \
			standmup

install-requirements:
	python3 -m pip install -r requirements.txt

freeze-requirements:
	python3 -m pip  freeze > requirements.txt

create-venv:
	python3 -m venv venv
	. venv/bin/activate

run:
	python3 application.py