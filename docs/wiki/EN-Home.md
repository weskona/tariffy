[🇩🇪 Deutsch](Home) · 🇬🇧 English

# Tariffy – Contract Management for Home Assistant

Tariffy manages your energy and service contracts in Home Assistant: electricity, gas, water, internet, mobile, streaming, insurance, loan, leasing and other. This wiki explains step by step how to set up and use Tariffy.

## What Tariffy does for you

- Every contract becomes its own Home Assistant device with sensors (costs, balance, forecast and more).
- With a meter sensor Tariffy measures the real consumption and derives the forecast and the recommended payment from it.
- Tariffy reminds you in time before the notice period ends and can take over the next tariff automatically on the switch date.
- The panel in the sidebar shows all contracts, costs and the history, also on a phone, in light and dark design.
- Backup and restore are built in; deleted contracts can be restored for 30 days.

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-overview.png"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-overview-light.png" alt="The Tariffy panel, overview: contracts, costs and notes at a glance" width="100%"></picture></p>

*Figure: the overview in the panel (mock data, date 12 July 2026).*

## Quick start

1. [Getting started](EN-Getting-Started) – install, add the integration, first contract in five minutes.
2. [Creating contracts](EN-Creating-Contracts) – all contract types and their form fields.
3. [Measuring consumption](EN-Measuring-Consumption) – choose a meter sensor so forecasts become real.
4. [The panel](EN-Panel-Overview) – the five views.

## All pages

| Topic | Pages |
|---|---|
| Start | [Getting started](EN-Getting-Started) · [Creating contracts](EN-Creating-Contracts) |
| Contracts by type | [Electricity](EN-Contract-Electricity) · [Gas](EN-Contract-Gas) · [Water](EN-Contract-Water) · [Internet and mobile](EN-Contract-Internet-and-Mobile) · [Streaming](EN-Contract-Streaming) · [Insurance](EN-Contract-Insurance) · [Leasing](EN-Contract-Leasing) · [Loan](EN-Contract-Loan) · [Other](EN-Contract-Other) |
| Consumption | [Measuring consumption](EN-Measuring-Consumption) · [PV self-sufficiency](EN-PV-Self-Sufficiency) |
| Payments and costs | [Payments and costs](EN-Payments-and-Costs) · [Payment history and one-off items](EN-Payment-History-and-One-off-Items) |
| Contract end and switching | [Contract end and switching](EN-Contract-End-and-Switching) · [Next contract or renew](EN-Next-Contract-or-Renew) · [Archive and history](EN-Archive-and-History) |
| Panel | [Overview](EN-Panel-Overview) · [Costs](EN-Panel-Costs) · [Contracts](EN-Panel-Contracts) · [History](EN-Panel-History) · [Backup](EN-Panel-Backup) · [Permissions and design](EN-Panel-Permissions-and-Design) |
| Reference | [Sensors](EN-Sensor-Reference) · [Dashboard examples](EN-Dashboard-Examples) · [Automations](EN-Automations) |
| Operation | [Backup and migration](EN-Backup-and-Migration) · [FAQ](EN-FAQ) · [Troubleshooting](EN-Troubleshooting) |
| Project | [Releases and beta](EN-Releases-and-Beta) · [Development](EN-Development) |

## Version and status

This wiki describes Tariffy **1.32.0** (stable). The sidebar panel exists since 1.27. New features arrive as a beta version first, see [Releases and beta](EN-Releases-and-Beta).

Source code, releases and changelog: [weskona/tariffy](https://github.com/weskona/tariffy) · [Changelog](https://github.com/weskona/tariffy/blob/main/CHANGELOG.md) · [Report a bug](https://github.com/weskona/tariffy/issues)
