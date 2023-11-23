function bot-compile() {
	local CONTAINER_NAME=$1
	local IMAGE_NAME=$2
	docker stop $CONTAINER_NAME
	docker rm -f $CONTAINER_NAME
	docker image rm -f $IMAGE_NAME
	docker build -t $IMAGE_NAME . && docker run -d -it --name $CONTAINER_NAME $IMAGE_NAME
}

function bot-attach() {
	local CONTAINER_NAME=$1
	docker exec -it $CONTAINER_NAME bash
}
