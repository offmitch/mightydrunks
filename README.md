# Hockey Team Analytics & Management Platform

A full-stack hockey analytics and management platform built to provide a centralized location for team schedules, scores, standings, player statistics, and team information.

## Live Site: https://mightydrunks.onrender.com/ (backend is currently depreciated)

## Features

* **Team Dashboard** — Centralized view of important team and league information.
* **Schedules** — View upcoming and past games.
* **Scores** — Display game results and completed game information.
* **Standings** — View current league standings.
* **Player Statistics** — Track player performance and statistics.
* **Team News** — Display relevant team updates and information.
* **Automated Data Collection** — Collects hockey data from external league sources.
* **Data Caching** — Caches collected data to reduce unnecessary external requests and improve performance.
* **RESTful API** — Backend endpoints provide structured hockey data to the frontend.
* **Responsive Design** — Designed to work across desktop and mobile devices.

## Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* RESTful API

### Data & Integrations

* External hockey league data
* Web scraping
* API integration
* Data caching

### Hosting

* Render

## How It Works

The application uses a Python backend to collect hockey information from external league sources. The backend processes and caches the data before making it available through RESTful API endpoints.

The frontend communicates with these endpoints using JavaScript and dynamically displays the latest available hockey information.

```text
External League Data
        ↓
Python Backend
        ↓
Data Collection / Processing
        ↓
Cached Data
        ↓
RESTful API
        ↓
JavaScript Frontend
        ↓
Schedules / Scores / Standings / Statistics
```


## Data Management

The backend is responsible for retrieving information from external hockey league sources and transforming it into data that can be consumed by the frontend.

Caching is used to avoid repeatedly requesting the same external information, helping improve application performance and reduce unnecessary requests.

## Purpose

The project was created to provide a more convenient way for a hockey team to access important league information in one place.

Instead of manually checking different league pages for schedules, scores, standings, and player statistics, the platform collects and presents the information through a single interface.

## Deployment

The application is deployed using **Render**.

## Author

**Mitchell MacDonald**
