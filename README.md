## Distributed Systems Project ##

### Run ###
To run simulation (at least the server), use docker compose to build server (and cars):
```
docker-compose -f docker-compose.yml up --build
```

Simulator's dashboard can be seen at: `http://localhost:5000`. Containers can be stopped and removed using the following command:
```
docker-compose -f docker-compose.yml down
```

System Architecture
![](https://github.com/ascalva/Distributed-Cars-Simulator/blob/58699722615c62754c65a588002c808fef69d878/Report/system_architecture.png)

