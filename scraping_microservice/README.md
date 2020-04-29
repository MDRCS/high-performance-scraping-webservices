

    + Download RabbitMQ Docker image:
    - docker pull rabbitmq:3-management
    - docker images (Check image)
    + Run RabbitMQ
    - docker run -d -p 15673:15673 -p 5672:5672 rabbitmq:3-management
    - docker ps (Check running image)
    - Login guest:guest

    + Download ElasticSearch Docker image:
    - docker pull docker.elastic.co/elasticsearch/elasticsearch:6.1.1
    - docker images
    - docker run -e ELASTIC_PASSWORD=MagicWord -p 9200:9200 -p 9300:9300 docker.elastic.co/elasticsearch/elasticsearch:6.1.1
    - curl localhost:9200 (Check running image)

    + run microservice
    - nameko run scraper_microservice

    + Nameko shell
    - nameko shell
    - n.rpc.hello_microservice.hello(name='Mike')


    + To get our containers to communicate with each other,
      let's create a new bridge network named scraper-net.

    - docker network ls
    - docker network create --driver bridge scraper-net

    + Now when we start a container, we attach it to scraper-net using the --network parameter:
    - docker stop 8975ce18ba12 (rabbitmq)
    - docker container rm rabbitmq
    - docker run -d --name rabbitmq --network scraper-net -p 15672:15672 -p 5672:5672 rabbitmq:3-management

    + Run Docker microservice
    - docker build ../.. -f Dockerfile  -t scraping-microservice
    - docker run --network scraper-net scraping-microservice

    + Run Restful API:
    - docker build ../.. -f Dockerfile -t scraper-rest-api
    - docker run -d -p 8080:8080 --network scraper-net scraper-rest-api
    - docker ps

    + Request API
    - curl localhost:8080/joblisting/122517

    + We can also use docker-compose to scale the services.
      If we want to add more microservice containers
      to increase the amount of requests that can be handled,
      we can tell Compose to increase the number of scraper service containers.
      The following increases the number of scraper containers to 3:

    - docker-compose up --scale scraper=3

    + Clean up Docker Containers
    - docker-compose stop
    - docker-compose ps
    - docker-compose rm -f
    - docker rmi -f $(docker images -qf dangling=true)
    - docker rmi social-network-platform_web --force
    - docker rmi 502d06d3bfdf --force
    - docker rmi $(docker images --filter dangling=true -q --no-trunc) --force
    - docker kill 29b49da748cf
    - docker system prune
    - docker volume prune
    - docker rmi $(docker images -a -q) # delete all images
