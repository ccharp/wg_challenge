# wg_challenge
Hello, WeaveGrid! I spent about 4.5 hours on this assignment with a lot of context switches. I'm wrapping up the academic quarter and had to fit this in where I could

## Notes 
Some considerations and future improvements:
* Anytime we're exposing the file system to the web, ecurity is a MAJOR concern, and I'm not convinced I got it all right. I'd want a full review from the team and hopefully a security export before I felt comfortable putting this in production. 
  * I was concerned about "`..`" in the input path, but it turns out "`..`" has semantic meanning in HTTP URI resolution. I don't *think* it's possible for 
  * Are symbolic links are security concern? 
* I don't consider race conditions. Multi-user semantics need careful consideration, especially operations that write i.e. PUT, POST, and DELETE. 
* Can we accommodate other pathing schemes?
* This was the first time I've used FastAPI
* Add more expressive file inclusion/exclusion configuration, e.g. patterns and globs. 
* Use smallest possible Docker base image. 
* Setup CI/CD: automatically lints, builds, and tests on each commit. Probably with GitHub Actions?

## Usage
### Initialize: 
```
$ poetry install
```

### Run locally:
```
$ uvicorn app.main:app --reload 
```

### Run Docker
```
$ docker compose build
$ docker compose up
```

### Test
```
$ pytest
```

### Configure root path
Configurable app settings can be found in `./.env`. Specifically, set the value of `active_path` to the path you'd like to use. Note that the application is subject to security constraints imposed by the host environment, so some paths may yeild error. 

