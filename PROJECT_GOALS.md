# Solar-Analysis: local Fox ESS energy dashboard

Created: 21 October 2026  
Status: goals and proposed approach recorded; implementation has not started.

## Project goal

Build a customisable website running on localhost that uses authenticated Fox ESS data to explain the home's energy flows, track historical performance, and help decide when to use electricity. Extend it with next-day solar and household-consumption forecasts, battery availability estimates, and practical recommendations with clear reasons and uncertainty.

Use this document as the ongoing project reference. At the start of each milestone, review the goal, assumptions and open questions. Update progress and decisions when work changes them.

## Questions the finished dashboard should answer

- What are the panels producing, the home consuming, the battery doing, and the grid importing or receiving right now?
- How much energy have I generated, consumed, imported, exported and stored today?
- How much battery energy can I actually use above my reserve, and how long might it cover the expected household load?
- How much solar generation and consumption should I expect tomorrow, and how uncertain are those estimates?
- When should I run flexible loads such as laundry, a dishwasher or an EV charger?
- Am I likely to fill the battery, export surplus solar, or need grid electricity overnight?
- How accurate were yesterday's predictions, and are generation or consumption patterns unusual?

## Existing foundation

Repository review on 21 October 2026 found:

- Python scripts for monthly totals, hourly patterns, tariff comparisons and savings analysis.
- 365 CSV files in `daily_export/`; the inspected sample has five-minute timestamped PV, grid and load readings in watts.
- Monthly CSV exports in `solar_data/` containing daily production, purchased energy, feed-in and load in kWh.
- Generated aggregate CSVs that may help exploration, but should be regenerated from validated source data for the new application.
- README documentation describing a 6.6 kW panel array and a 5 kW inverter. This may describe an earlier installation and needs confirmation.
- `sungrow_api.py`, a local Modbus register-scanning experiment. No Fox ESS client or web application was found in the reviewed source files.

The user has an existing Fox ESS connection. Its location, authentication method and associated hardware are still to be confirmed; absence of a client here does not mean the connection does not exist elsewhere.

Old tariffs and installation details are historical inputs, not current defaults. Older data may describe a different system or household pattern. Confirm comparability before using it to train or evaluate forecasts.

## Proposed architecture

```text
Fox ESS Cloud -> Python collector -> SQLite history
                         |                |
                         +-> FastAPI <----+
                                |
                         localhost website
                                |
                     React + TypeScript UI

Weather/solar forecast + household history + tariffs + system settings
                                |
                    forecast and advice engine
                                |
                        FastAPI -> website
```

Recommended starting stack: Python/FastAPI for the backend, SQLite for local storage, and React/TypeScript with Vite for the frontend. Keep collection, calculations and visual presentation separate. These are proposed choices, not an existing implementation.

Serve the built frontend and API from the local backend for ordinary use; a separate Vite server can support frontend development. Bind to loopback initially. A background collector must keep running to record new data when the browser is closed; when the computer is off, collection stops and any supported historical backfill runs after restart. Consider an always-on home device later.

### Authentication and collection

- Prefer a personal Fox ESS API key for this single-household application if the account supports it. Reuse a suitable existing integration when found. Investigate OAuth only if required by the existing connection or future scope.
- Store credentials in local environment configuration excluded from Git. Keep credentials and signed Fox requests on the backend; never send Fox secrets to the browser or log them.
- Discover the device and available measurements before designing around assumed variable names. Confirm account region, inverter model, battery support, units, timestamps and direction conventions.
- Begin with one shared collection job every five minutes: approximately 288 snapshot calls per day for a single request per cycle. Budget discovery, reports, retries, backfill and other clients separately.
- Cache readings locally so opening or refreshing dashboard tabs does not multiply Fox API requests. Handle timeouts, API errors, quotas and retries with bounded backoff.
- Store source measurement time and collection time separately. Show last update, stale data and unavailable measurements explicitly; missing is not zero.

Fox's public documentation, checked on 21 October 2026, describes API-key and OAuth authentication, signed timestamped requests, and a limit of 1,440 interface calls per day per inverter under an account. Query endpoints also have per-interface frequency limits. Verify the actual account allowance and other integrations before selecting the final schedule. The current real-time endpoint documented is `POST /op/v1/device/real/query`; the older v0 equivalent is marked deprecated.

Source: [Fox ESS official Open API documentation](https://www.foxesscloud.com/public/i18n/en/OpenApiDocument.html).

### Data and energy accounting

- Store timestamps in UTC and group/display by the installation timezone; provisionally use `Australia/Brisbane` until confirmed.
- Use kW for instantaneous power and kWh for accumulated energy. Store import/export and battery charge/discharge as explicit directions after validating Fox's sign conventions.
- Preserve validated source observations and use a consistent internal schema across Fox data and CSV imports. Deduplicate imports and backfill.
- Prefer reliable source energy counters for daily totals. If integrating power readings, account for actual time intervals and coverage; do not integrate across long gaps or assume a fixed number of readings.
- Check energy balance, allowing for measurement boundaries and conversion losses. Validate totals against Fox's portal for matching periods.
- Mark hardware changes and data coverage so old and new systems are not silently mixed.

## Delivery milestones

### 1. Prove the connection

Confirm the existing Fox integration and local credential setup. Build a small backend client that lists the intended device and retrieves a redacted snapshot of solar, load, grid and battery measurements where available.

Done when: authentication succeeds, device selection is explicit, units/directions are understood, and current values can be compared with the Fox portal. Do not change inverter settings.

### 2. Deliver the first useful local dashboard

Add collection and SQLite persistence. Display an energy-flow view connecting solar, home, battery and grid; battery percentage and reserve; today's totals; an intraday chart; connection status and measurement age. Keep colours, layout and visible cards easy to customise.

Done when: the dashboard runs locally, shows real persisted data, survives restart, and handles stale/missing readings without presenting them as live values. Verify useful calculations and failure handling with focused checks.

### 3. Add historical insight

Import validated exports and backfill what Fox permits. Add daily/weekly/monthly views, typical household load profiles, self-consumption, grid reliance and estimated costs using configurable current tariffs. Keep daily supply charges and feed-in credits distinct.

Done when: imports are repeatable without duplicates, coverage is visible, and sampled totals reconcile with source reports within explained tolerances.

### 4. Forecast tomorrow and battery availability

Start consumption prediction with a transparent baseline: recent comparable weekday/weekend profiles, with recent behaviour weighted more strongly. Start solar prediction with a weather/irradiance-based solar forecast using confirmed location, array orientation, tilt and inverter limits; choose the provider after checking coverage, terms and cost.

Combine forecasts with current battery state, capacity, reserve, efficiency and charge/discharge power limits to simulate the next 24–48 hours. Predict solar output, household load, battery state and grid exchange by interval. Keep battery-free operation supported if no battery is available.

Battery calculations must distinguish energy from power. An initial estimate is:

```text
energy above reserve (kWh) = effective full capacity (kWh)
                            × max(0, current SOC - reserve SOC) / 100
```

Here effective full capacity means the energy represented by the reported 0–100% SOC range, adjusted for known degradation. Do not subtract hidden manufacturer buffers a second time. Estimate energy delivered to the home using discharge losses, and estimate runtime using forecast net demand and power limits. Label all assumptions.

Done when: predictions are saved before their forecast period, uncertainty is visible, and subsequent actuals are compared with the saved predictions. Evaluate on later dates excluded from model fitting and compare with simple baselines before increasing complexity.

### 5. Give proactive, explainable advice

Rank practical appliance-use windows by forecast surplus, available battery energy, tariff periods, feed-in opportunity cost and the user's timing constraints. Account for an appliance's duration and power requirement; a low daily cost alone does not prove a particular hour is suitable.

Show advice in the dashboard, for example: “The strongest forecast surplus is late morning; that is the best window for a two-hour dishwasher cycle.” Any displayed numerical recommendation must come from actual inputs and state its confidence. Update advice as readings and forecasts change. Suppress specific advice when inputs are stale or inadequate.

Done when: each recommendation has an understandable reason, assumptions and an estimated benefit where supported. Dashboard advice is the initial proactive feature; external notifications can be scoped separately.

## Scope boundaries

- Initial scope is a local, single-household, observational application with recommendations.
- Remote access, public hosting, multi-user accounts and automated inverter/appliance control are possible later extensions.
- Inverter writes, battery schedule changes and automated device control require a separate explicit decision and scope.
- An LLM is optional for explaining computed results. Numerical forecasts and energy accounting should remain inspectable and testable.

## Details to confirm before implementation

1. Where does the current Fox ESS connection run, and does it use an API key or OAuth? Do not put secrets in this document or chat.
2. Current inverter, solar array and battery models/capacity; minimum reserve; whether legacy exports represent this setup.
3. Installation timezone and approximate location; panel orientation and tilt when adding solar forecasts.
4. Current import rates, any time-of-use windows, feed-in rates and supply charge.
5. Flexible appliances, approximate power/duration, preferred run windows and backup-reserve preferences.
6. Which machine will run the app, and whether it will remain on for collection.

## Progress and decisions

- 21 October 2026: project goal and phased approach recorded after repository review and checking official Fox API documentation.
- Proposed first joint task: identify the existing Fox connection, then implement and validate an authenticated backend snapshot before building the dashboard around it.
