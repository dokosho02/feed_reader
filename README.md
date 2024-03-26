# Feed reader

![image](/images/three-panel.png)


This is a demo for now.

- frontend: Vue
- backend: FastAPI

use json format as the bridge between frontend and backend

## Run

backend
```sh
cd backend
poetry install    # for the first time
poetry run uvicorn backend.app:app --reload --port 10000
```

frontend

```sh
cd frontend
yarn install    # for the first time
yarn serve
```

## features

### database-independent
- feed
  - [x] make selected item bold
  - [ ] show relative time
  - [ ] show item count
- item
  - [x] open link (core)
  - not html
    - [ ] render tag by tag with lang in different fonts
  - lang
  - translation

### database-dependent
- feed
  - starred/unstarred
  - unread/read
  - [ ] make read item as gray
- item
  - save as epub
  - copy as markdown



## Todos

- [ ] add database support to achieve some features
- [ ] Settings widget
- [ ] OPML import/export
- [ ] figure in huxiu, referring to NiceFeed
