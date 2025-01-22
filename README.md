run Dockerfile with:

```
docker build -t studienarbeit .
docker run -d -v ./downloads/:/app/downloads/ studienarbeit
```
