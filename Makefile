include config.env

# DOCKER TASKS
# # Build the container
build: ## Build the container
	docker build -t $(REGISTRY)/$(APP_NAME):$(TAG) .

login: ## login to the registry
	@read -p "username : " USERNAME; \
	read -s -p "password : " PASSWORD; \
	docker login $(REGISTRY) -u $${USERNAME} -p $${PASSWORD}


push: ## Push the container
	docker push $(REGISTRY)/$(APP_NAME):$(TAG)

release: build login push

kind-load: build 

lint:
	pytest --pylint -m pylint	
