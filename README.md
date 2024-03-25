# Feed reader

This is a demo for now.

- frontend: Vue
- backend: FastAPI

use json format as the bridge between frontend and backend

## Run

backend
```sh
poetry run uvicorn backend.app:app --reload --port 10000
```

frontend

```sh
yarn serve
```

## features

- [x] make selected item bold
- [ ] make read item as gray
- [ ] show relative time
- [ ] show item count




content
- not html
  - [ ] render tag by tag with lang in different fonts

- lang
- translation

function
 - starred/unstarred
 - unread/read
 
 - [x] open link
 - save as epub
 - copy as markdown



## Todos

- [ ] figure in huxiu, referring to NiceFeed
