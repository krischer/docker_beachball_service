# Beachball Plotting Service

A Docker based service to serve beachballs over HTTP. This is really really
overkill for just plotting beachballs but it was easy to do and it is very easy
to set up.

Launch it with:

```bash
$ docker build -t beachball-service ./beachball-service
$ docker run --rm -p 12345:12345 beachball-service python3 launch_server.py
```

Example URLs:

```
http://localhost:12345/mt?m_rr=1.0&m_tt=1.0&m_pp=1.0&m_rt=1.0&m_rp=1.0&m_tp=1.0&size=200&color=blue
http://localhost:12345/mt?m_rr=1.0&m_tt=1.0&m_pp=1.0&m_rt=1.0&m_rp=1.0&m_tp=1.0&size=450&color=D0344E
```
