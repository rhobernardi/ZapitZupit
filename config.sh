# For system usage
function bot-install() {
	printf "[*] Creating telebot venv..."
	python3 -m venv ~/telebot
 	
  	printf "[*] Copying files..."
 	cp zapitzupit.py requirements.txt ImageReaderAI.py log.py ~/telebot
 	cd ~/telebot
  	
   	printf "[*] Creating img and log folders..."
  	mkdir -p ./log/
	mkdir -p ./img/
	echo "API_KEY=$1" > .env

   	printf "[*] Installing tesseract and dependencies..."
 	sudo apt update && apt -y install tesseract-ocr libgl1-mesa-glx
	source ./bin/activate
	pip install -r requirements.txt
   	
    	printf "[*] Done!"
}

PID=0
function bot-run() {
 	PID=$(python3 zapitzupit.py & disown)
   	printf "[*] Zapitzupit is now running. You can close this terminal."
}

# For Docker usage
function docker-bot-compile() {
	local CONTAINER_NAME=$1
	local IMAGE_NAME=$2
	docker stop $CONTAINER_NAME
	docker rm -f $CONTAINER_NAME
	docker image rm -f $IMAGE_NAME
	docker build -t $IMAGE_NAME . && docker run -d -it --name $CONTAINER_NAME $IMAGE_NAME
}

function docker-bot-attach() {
	local CONTAINER_NAME=$1
	docker exec -it $CONTAINER_NAME bash
}
