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
![](https://github.com/ascalva/Distributed-Cars-Simulator/blob/92f00a2b71e81800894ab8f790692dfc1b604f1d/Report/System_architecture-WhiteBG.png)

Link to the report on Overleaf:
https://www.overleaf.com/1138417336jjgwpvjxjhkb

