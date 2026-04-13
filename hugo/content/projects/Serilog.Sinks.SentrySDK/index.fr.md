---
title: "Serilog.Sinks.SentrySDK"
linkTitle: "Serilog.Sinks.SentrySDK"
date: 2021-09-06T22:42:23+08:00
draft: false
description: "Sink Serilog qui envoie les événements vers Sentry via le SDK Sentry."
tags:
    - Serilog
    - Sentry
    - SentrySDK
---

# Serilog.Sinks.SentrySDK

**Sink Serilog** pour **Sentry** : centraliser logs et erreurs dans Sentry avec le SDK officiel.

S’inspire de [serilog-contrib/serilog-sinks-sentry](https://github.com/serilog-contrib/serilog-sinks-sentry).

## État du projet

[![.NET Core Test](https://github.com/antoinebou12/Serilog.Sinks.SentrySDK/actions/workflows/tests.yml/badge.svg)](https://github.com/antoinebou12/Serilog.Sinks.SentrySDK/actions/workflows/tests.yml)
[![.NET Core CI](https://github.com/antoinebou12/Serilog.Sinks.SentrySDK/actions/workflows/CI.yml/badge.svg)](https://github.com/antoinebou12/Serilog.Sinks.SentrySDK/actions/workflows/CI.yml)
[![CodeQL](https://github.com/antoinebou12/Serilog.Sinks.SentrySDK/actions/workflows/codeql.yml/badge.svg)](https://github.com/antoinebou12/Serilog.Sinks.SentrySDK/actions/workflows/codeql.yml)
[![codecov](https://codecov.io/gh/antoinebou12/Serilog.Sinks.SentrySDK/branch/main/graph/badge.svg?token=DKLJUGCpI4)](https://codecov.io/gh/antoinebou12/Serilog.Sinks.SentrySDK)

## Paquets NuGet

|                                    | Paquet                                                                            | NuGet                                                                                                                                                 |
| ---------------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Serilog.Sinks.SentrySDK            | [Lien](https://www.nuget.org/packages/Serilog.Sinks.SentrySDK/)                    | [![NuGet](https://img.shields.io/nuget/v/Serilog.Sinks.SentrySDK.svg)](https://www.nuget.org/packages/Serilog.Sinks.SentrySDK/)                       |
| Serilog.Sinks.SentrySDK.AspNetCore | [Lien](https://www.nuget.org/packages/Serilog.Sinks.SentrySDK.AspNetCore/)         | [![NuGet](https://img.shields.io/nuget/v/Serilog.Sinks.SentrySDK.AspNetCore.svg)](https://www.nuget.org/packages/Serilog.Sinks.SentrySDK.AspNetCore/) |

## Installation et configuration

Exemples `dotnet add package`, configuration dans `Program.cs` / `appsettings.json`, et options avancées : voir le [README en anglais](https://github.com/antoinebou12/Serilog.Sinks.SentrySDK) sur GitHub.
